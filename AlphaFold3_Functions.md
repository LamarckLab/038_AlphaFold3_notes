## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### 该文档用于记录 server 上跑 AF3 的命令
---

> **01 单个蛋白质无模板结构预测（默认参数）**
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

> **02 批量蛋白质无模板结构预测（默认参数）**
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

> **03 批量蛋白质无模板结构预测 - 仅运行 Data Pipeline**
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

> **04 批量蛋白质无模板结构预测 - 仅运行 Inference**
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
