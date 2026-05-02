"""
从多链 cif 抽出 A 链，存成单链 cif 供 AF3 当模板。
所有文件路径硬编码在下面的常量里，换文件就改这几行。

依赖：gemmi (pip install gemmi)
"""

from pathlib import Path
import sys
import gemmi

WORK_DIR = Path(r"C:\Users\Lamarck\Desktop\Todo_Template")
INPUT_CIF = WORK_DIR / "2PV7.cif"
OUTPUT_CIF = WORK_DIR / "2PV7_single.cif"
KEEP_CHAIN = "A"


def read_release_date(cif_path: Path) -> str:
    """从原始 cif 读初次发布日期，避免手工查 PDB 网站。"""
    doc = gemmi.cif.read(str(cif_path))
    block = doc.sole_block()
    dates = block.find_values("_pdbx_audit_revision_history.revision_date")
    if not dates or len(dates) == 0:
        sys.exit(
            f"{cif_path.name} 里没有 _pdbx_audit_revision_history.revision_date，"
            "无法确定模板发布日期"
        )
    return str(dates[0]).strip("'\"")


def main():
    if not INPUT_CIF.exists():
        sys.exit(f"找不到输入文件：{INPUT_CIF}")

    release_date = read_release_date(INPUT_CIF)

    structure = gemmi.read_structure(str(INPUT_CIF))
    for model in structure:
        for name in [chain.name for chain in model]:
            if name != KEEP_CHAIN:
                model.remove_chain(name)

    remaining = [chain.name for model in structure for chain in model]
    if KEEP_CHAIN not in remaining:
        sys.exit(f"原文件里没有 {KEEP_CHAIN} 链，只有：{remaining}")

    doc = structure.make_mmcif_document()
    block = doc.sole_block()

    revision_loop = block.init_loop(
        "_pdbx_audit_revision_history.",
        ["ordinal", "data_content_type", "major_revision",
         "minor_revision", "revision_date"],
    )
    revision_loop.add_row(["1", "'Structure model'", "1", "0", release_date])

    doc.write_file(str(OUTPUT_CIF))

    result = gemmi.read_structure(str(OUTPUT_CIF))
    chains = [chain.name for model in result for chain in model]
    print("完成")
    print(f"  输入:     {INPUT_CIF}")
    print(f"  输出:     {OUTPUT_CIF}")
    print(f"  保留链:   {chains}")
    print(f"  发布日期: {release_date}")


if __name__ == "__main__":
    main()
