<p align="left">
  <a href="./README_EN.md">Homepage</a>
</p>
<p align="right">
  <strong>English</strong> | <a href="../AlphaFold3_Functions.md">中文</a>
</p>

## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### Command reference for running AlphaFold3 on the server
---

*Path configuration*
```bash
Input dir:      /data/lmk/alphafold3_inputs       # JSON input files
Output dir:     /data/lmk/alphafold3_outputs      # predictions (cif + confidence)
Parameters dir: /data/lmk/alphafold3_parameters   # model weights af3.bin
Databases dir:  /data/lmk/alphafold3_databases    # MSA databases (~627GB)
```
Inside the container these are mounted at `/af3_inputs`, `/af3_outputs`, `/af3_parameters` and `/af3_databases`.

---

> **01 Protein structure prediction -- |single job|no custom template|default settings|**
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

> **02 Protein structure prediction -- |batch job|no custom template|default settings|**
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

> **03 Protein structure prediction -- |batch job|no custom template|data pipeline only|**
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

Serial execution is impractical for large batches; split the work across several containers instead (see 03b).

> **03b Protein structure prediction -- |batch job|data pipeline only|parallel containers|**

**Input**: the pending JSON files, tens to hundreds of them, in `alphafold3_inputs/`.

`scripts/af3_msa_split_parallel.py` distributes the jobs round-robin across N groups, one container per group. Set `GROUPS` at the top of the script to control the degree of parallelism; on completion the script prints the corresponding launch command.

```bash
python /data/lmk/alphafold3_scripts/af3_msa_split_parallel.py
```

Example:
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

`2>&1 | sed` prefixes each line with `[gN]`, keeping the eight interleaved logs distinguishable. The trailing `&` and the closing `wait` run all eight groups concurrently.

> **03c Inspecting and stopping the parallel containers -- |batch job|parallel containers|operations|**

List the running containers:
```bash
docker ps
```

Stop all running AF3 containers. `docker ps -q` emits container IDs only, which `$()` passes to `stop`:
```bash
docker stop $(docker ps -q --filter name=af3_g)
```

These two commands cover routine use: the launch command in 03b passes `--rm`, so each container is removed on exit.

> **04 Protein structure prediction -- |batch job|no custom template|inference only|**
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

> **05 Protein structure prediction -- |batch job|no custom template|custom sample count per seed|**
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

> **06 Protein structure prediction -- |batch job|no custom template|template date cutoff|**
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

> **07 Protein structure prediction -- |batch job|custom template|inference only|**

The example files for this workflow are in [custom template pipeline](../custom%20template%20pipeline/).

##### Workflow overview

```
2PV7.json
    │
    │  ① run the data pipeline on the server
    ▼
2PV7_data.json  (MSA + the templates it found automatically)

2PV7.cif
    │
    │  ② extract the chain locally with extract_single_chain.py
    ▼
2PV7_single.cif + 2PV7_data.json
    │
    │  ③ inject it locally with add_custom_template.py
    ▼
2PV7_data_custom_template.json + 2PV7_single.cif
    │
    │  ④ run inference only on the server
    ▼
final structure + confidence files
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

##### [AlphaFold3 official documentation](https://github.com/google-deepmind/alphafold3)
