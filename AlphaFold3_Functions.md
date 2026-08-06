## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### 该文档用于记录 server 上跑 AlphaFold3 的各种命令
---

*路径配置*
```bash
输入目录:   /data/lmk/alphafold3_inputs       # JSON 输入文件
输出目录:   /data/lmk/alphafold3_outputs      # 预测结果 (cif + 置信度)
参数目录:   /data/lmk/alphafold3_parameters   # 模型权重 af3.bin
数据库目录: /data/lmk/alphafold3_databases    # MSA 数据库 (~627GB)
```
容器内挂载点分别为 `/af3_inputs`、`/af3_outputs`、`/af3_parameters`、`/af3_databases`

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

任务多时串行太慢，可拆成多个容器并行 —— 详见 03b

> **03b 蛋白质结构预测 -- |批量任务|仅 Data Pipeline|多容器并行|**

**输入**：`alphafold3_inputs/` 放几十上百个待跑 JSON

用 `scripts/af3_msa_split_parallel.py` 把任务轮转切分到 N 组，再起 N 个容器各跑一组。改脚本顶部的 `GROUPS` 即可调并行度，跑完它会打印配套的启动命令。

```bash
python /data/lmk/alphafold3_scripts/af3_msa_split_parallel.py
```

例如
```bash
for g in 0 1 2 3 4 5 6 7; do
  docker run --rm --name af3_g$g \
    --volume /data/lmk/alphafold3_inputs_split/g$g:/af3_inputs \
    --volume /data/lmk/alphafold3_outputs:/af3_outputs \
    --volume /data/lmk/alphafold3_parameters:/af3_parameters \
    --volume /data/lmk/alphafold3_databases:/af3_databases \
    -e XLA_PYTHON_CLIENT_PREALLOCATE=false \
    alphafold3 \
    python run_alphafold.py \
      --input_dir=/af3_inputs \
      --model_dir=/af3_parameters \
      --db_dir=/af3_databases \
      --output_dir=/af3_outputs \
      --jackhmmer_n_cpu=8 \
      --norun_inference 2>&1 | sed "s/^/[g$g] /" &
done
wait
```

`2>&1 | sed` 给每行加 `[gN]` 前缀，8 路日志交错也分得清；行尾 `&` 加最后 `wait` 让 8 路同时跑。

> [!NOTE]
> **同序列的 MSA 在同一容器进程内复用。** 

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

> **06 蛋白质结构预测 -- |批量任务|不指定模板|限定模板日期|**
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
    --max_template_date=2018-01-01
```

> **07 蛋白质结构预测 -- |批量任务|指定模板|仅 Inference|**

本流程涉及的所有示例文件见仓库 [custom template pipeline](custom%20template%20pipeline/)

##### 流程总览

```
2PV7.json
    │
    │  ① 服务器跑 data pipeline
    ▼
2PV7_data.json  (含 MSA + 自动搜到的模板)

2PV7.cif
    │
    │  ② 本地用 extract_single_chain.py 抽链
    ▼
2PV7_single.cif + 2PV7_data.json
    │
    │  ③ 本地用 add_custom_template.py 注入
    ▼
2PV7_data_custom_template.json + 2PV7_single.cif
    │
    │  ④ 服务器跑仅 inference
    ▼
最终结构 + 置信度文件
```

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
