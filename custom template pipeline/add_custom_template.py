"""
把单链 cif 当作自定义模板写入 _data.json，自动算 indices。
所有文件路径硬编码在下面的常量里，换文件就改这几行。

工作流程：
  1. 从 cif 的 _entity_poly_seq 读完整 polymer 序列（含缺失残基）
  2. 从结构里读已解析残基的 label_seq_id，映射为完整序列里的 0-based 位置
  3. 把 query 序列与完整 polymer 序列做 BLOSUM62 全局对齐
  4. 取对齐对里 template 位置已解析的，作为 (queryIndices, templateIndices)
  5. 写出 OUTPUT_JSON，templates 字段替换为该自定义模板

依赖：gemmi, biopython
    pip install gemmi biopython
"""

from pathlib import Path
import json
import re
import sys
import gemmi
from Bio import Align
from Bio.Align import substitution_matrices

WORK_DIR = Path(r"C:\Users\Lamarck\Desktop\Todo_Template")
INPUT_DATA_JSON = WORK_DIR / "2PV7_data.json"
TEMPLATE_CIF = WORK_DIR / "2PV7_single.cif"
OUTPUT_JSON = WORK_DIR / "2PV7_data_custom_template.json"
REPLACE_AUTO_TEMPLATES = True  # True: 替换；False: 追加在末尾


def read_template_info(cif_path: Path):
    """返回 (full_polymer_seq, resolved_positions, chain_name)。
    full_polymer_seq    : 完整 polymer 1-letter 序列（含缺失残基）
    resolved_positions  : 已解析残基在 full_polymer_seq 里的 0-based 位置
    """
    doc = gemmi.cif.read(str(cif_path))
    block = doc.sole_block()
    table = block.find("_entity_poly_seq.", ["num", "mon_id"])

    full_seq_chars = []
    label_seq_to_full_pos = {}
    for row in table:
        try:
            label_seq = int(str(row[0]))
        except ValueError:
            continue
        mon_id = str(row[1]).strip("'\"")
        info = gemmi.find_tabulated_residue(mon_id)
        if info and info.is_amino_acid():
            label_seq_to_full_pos[label_seq] = len(full_seq_chars)
            full_seq_chars.append(info.one_letter_code.upper())

    if not full_seq_chars:
        sys.exit(f"{cif_path.name} 的 _entity_poly_seq 里没读到氨基酸残基")

    full_seq = "".join(full_seq_chars)

    structure = gemmi.read_structure(str(cif_path))
    chains = list(structure[0])
    if len(chains) != 1:
        names = [c.name for c in chains]
        sys.exit(f"{cif_path.name} 不是单链，找到 {len(chains)} 条：{names}")
    chain = chains[0]

    resolved_positions = sorted({
        label_seq_to_full_pos[r.label_seq]
        for r in chain
        if r.label_seq is not None and r.label_seq in label_seq_to_full_pos
    })
    if not resolved_positions:
        sys.exit(f"{cif_path.name} 里没找到已解析的氨基酸残基")
    return full_seq, resolved_positions, chain.name


def align_and_filter(query: str, template: str, resolved_positions):
    """全局对齐 query 与 template，过滤掉 template 端 missing 的对齐对。"""
    aligner = Align.PairwiseAligner()
    aligner.mode = "global"
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5

    alignment = aligner.align(query, template)[0]
    resolved = set(resolved_positions)

    qi, ti = [], []
    matches = 0
    for q_block, t_block in zip(alignment.aligned[0], alignment.aligned[1]):
        qs, qe = int(q_block[0]), int(q_block[1])
        ts = int(t_block[0])
        for offset in range(qe - qs):
            q_pos = qs + offset
            t_pos = ts + offset
            if t_pos in resolved:
                qi.append(q_pos)
                ti.append(t_pos)
                if query[q_pos] == template[t_pos]:
                    matches += 1

    identity = matches / len(qi) * 100 if qi else 0.0
    return qi, ti, identity


def af3_style_dump(obj, indent=2):
    """对象多行展开，纯数字数组保持单行（仿 AF3 默认输出风格）。"""
    text = json.dumps(obj, indent=indent, ensure_ascii=False)

    def collapse(match):
        nums = re.findall(r"-?\d+", match.group(1))
        return "[" + ", ".join(nums) + "]"

    return re.sub(
        r"\[\s*((?:-?\d+\s*,\s*)*-?\d+)\s*\]",
        collapse,
        text,
    )


def main():
    if not INPUT_DATA_JSON.exists():
        sys.exit(f"找不到 _data.json：{INPUT_DATA_JSON}")
    if not TEMPLATE_CIF.exists():
        sys.exit(f"找不到模板 cif：{TEMPLATE_CIF}")

    print(f"输入 _data.json:       {INPUT_DATA_JSON}")
    print(f"自定义模板 cif:        {TEMPLATE_CIF}")
    print(f"输出文件:              {OUTPUT_JSON}")
    print()

    with INPUT_DATA_JSON.open(encoding="utf-8") as f:
        data = json.load(f)

    query_seq = data["sequences"][0]["protein"]["sequence"]
    full_template, resolved, chain_name = read_template_info(TEMPLATE_CIF)

    print(f"Query 长度:            {len(query_seq)}")
    print(f"Template 全长(含缺失): {len(full_template)}")
    print(f"Template 已解析残基:   {len(resolved)} (链 {chain_name})")
    print()

    qi, ti, identity = align_and_filter(query_seq, full_template, resolved)
    print(f"对齐位置数(过滤缺失):  {len(qi)}")
    print(f"序列一致性:            {identity:.1f}%")
    print(f"queryIndices    范围:  [{min(qi)}, {max(qi)}]")
    print(f"templateIndices 范围:  [{min(ti)}, {max(ti)}]")
    print()

    protein = data["sequences"][0]["protein"]
    old_count = len(protein.get("templates", []))
    new_template = {
        "mmcifPath": TEMPLATE_CIF.name,
        "queryIndices": qi,
        "templateIndices": ti,
    }
    if REPLACE_AUTO_TEMPLATES:
        protein["templates"] = [new_template]
        action = f"替换原 {old_count} 个模板"
    else:
        protein.setdefault("templates", []).append(new_template)
        action = f"追加到原 {old_count} 个模板之后"

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        f.write(af3_style_dump(data))

    print("完成")
    print(f"  操作:     {action}")
    print(f"  cif 名:   {TEMPLATE_CIF.name}（AF3 跑的时候要跟 JSON 同目录）")


if __name__ == "__main__":
    main()
