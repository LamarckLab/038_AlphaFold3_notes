## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### 该文档用于记录 server 上跑 AF3 的命令
---

> **01 蛋白质结构预测 -- |单任务|不指定模板|默认参数|**
```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs\
  --volume /data/lmk/alphafold3_parameters:/af3_parameters\
  --volume /data/lmk/alphafold3_databases:/af3_databases\
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --json_path=/af3_inputs/LMK1.json \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases\
    --output_dir=/af3_outputs
```

> **02 蛋白质结构预测 -- |批量任务|不指定模板|默认参数|**
```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs \
  --volume /data/lmk/alphafold3_parameters:/af3_parameters \
  --volume /data/lmk/alphafold3_databases:/af3_databases \
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --input_dir=/af3_inputs \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases \
    --output_dir=/af3_outputs
```

> **03 蛋白质结构预测 -- |批量任务|不指定模板|仅 Data Pipeline|**
```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs \
  --volume /data/lmk/alphafold3_parameters:/af3_parameters \
  --volume /data/lmk/alphafold3_databases:/af3_databases \
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --input_dir=/af3_inputs \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases \
    --output_dir=/af3_outputs \
    --norun_inference
```

> **04 蛋白质结构预测 -- |批量任务|不指定模板|仅 Inference|**
```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs \
  --volume /data/lmk/alphafold3_parameters:/af3_parameters \
  --volume /data/lmk/alphafold3_databases:/af3_databases \
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --input_dir=/af3_inputs \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases \
    --output_dir=/af3_outputs \
    --norun_data_pipeline
```

> **05 蛋白质结构预测 -- |批量任务|不指定模板|自定义每个种子 sample 数|**
```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs \
  --volume /data/lmk/alphafold3_parameters:/af3_parameters \
  --volume /data/lmk/alphafold3_databases:/af3_databases \
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --input_dir=/af3_inputs \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases \
    --output_dir=/af3_outputs \
    --num_diffusion_samples=3
```

> **06 蛋白质结构预测 -- |批量任务|指定模板|仅 Inference|**

本流程涉及的所有示例文件见仓库 [custom template pipeline](custom%20template%20pipeline/)

##### 流程总览

```
2PV7.cif + 2PV7.json
       │
       │  ① 服务器跑 data pipeline (功能 03)
       ▼
2PV7_data.json  (含 MSA + 自动搜到的模板)
       │
       │  ② 本地用 extract_single_chain.py 抽链
       ▼
2PV7_single.cif  (单链模板，含发布日期)
       │
       │  ③ 本地用 add_custom_template.py 注入
       ▼
2PV7_data_custom_template.json  (推理输入)
       │
       │  ④ 服务器跑仅 inference
       ▼
最终结构 + 置信度文件
```

##### ① 准备原始输入（本地两个文件）

- `2PV7.cif`：从 RCSB 下载的多链原始 cif，作模板用
  ```bash
  wget https://files.rcsb.org/download/2PV7.cif
  ```
- `2PV7.json`：AF3 的初始 JSON，只含 `name` / `sequences` / `modelSeeds` / `dialect` / `version`，不带模板。格式见 [AlphaFold3_JSON_Format.md](AlphaFold3_JSON_Format.md)

##### ② 服务器跑 data pipeline 拿到 `_data.json`

把 `2PV7.json` 上传到 `/data/lmk/alphafold3_inputs/`，跑功能 03 的命令（`--norun_inference`）。

产出 `/data/lmk/alphafold3_outputs/2pv7/2pv7_data.json`，把它下载回本地 `Todo_Template` 文件夹（重命名为 `2PV7_data.json` 便于辨识）。该文件包含 AF3 自动搜到的 MSA 和模板。

##### ③ 本地抽单链 cif

把 `2PV7.cif` 放进 `C:\Users\Lamarck\Desktop\Todo_Template\`，运行：

```bash
python extract_single_chain.py
```

脚本做的事：
- 删除原 cif 里除 A 链外的所有链
- 自动从 `_pdbx_audit_revision_history.revision_date` 读 PDB 发布日期，写进新 cif（让 AF3 的 `--max_template_date` 默认 `2021-09-30` 过滤能放行）
- 输出 `2PV7_single.cif` 到同目录

##### ④ 本地把自定义模板写入 `_data.json`

确保 `2PV7_data.json` 和 `2PV7_single.cif` 都在 `Todo_Template` 文件夹，运行：

```bash
python add_custom_template.py
```

脚本做的事：
- 从 `2PV7_single.cif` 的 `_entity_poly_seq` 读完整 polymer 序列（含 missing residues）
- 从结构里读已解析残基的 0-based 位置（自动剔除 missing）
- 对 query 序列与 template 序列做 BLOSUM62 全局对齐
- 取对齐对里 template 端已解析的位置，作为 `queryIndices` / `templateIndices`
- 把 `2PV7_data.json` 里 `templates` 字段替换为这份自定义模板

输出 `2PV7_data_custom_template.json` 到同目录。

##### ⑤ 服务器跑仅 Inference

把 `2PV7_data_custom_template.json` 和 `2PV7_single.cif` **一起**上传到 `/data/lmk/alphafold3_inputs/`（必须同目录，因为 JSON 里 `mmcifPath` 是相对路径）。

确保该目录下没有别的 `*.json` 文件，否则 `--input_dir` 模式会一并尝试。

```bash
docker run -it --rm \
  --volume /data/lmk/alphafold3_inputs:/af3_inputs \
  --volume /data/lmk/alphafold3_outputs:/af3_outputs \
  --volume /data/lmk/alphafold3_parameters:/af3_parameters \
  --volume /data/lmk/alphafold3_databases:/af3_databases \
  --gpus '"device=3"' \
  -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
  alphafold3 \
  python run_alphafold.py \
    --input_dir=/af3_inputs \
    --model_dir=/af3_parameters \
    --db_dir=/af3_databases \
    --output_dir=/af3_outputs \
    --norun_data_pipeline
```

##### [AlphaFold3官方文档](https://github.com/google-deepmind/alphafold3)
