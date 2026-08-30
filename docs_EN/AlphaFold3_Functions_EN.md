<p align="left">
  <a href="./README_EN.md">← Back to home</a>
</p>
<p align="right">
  <strong>English</strong> | <a href="../AlphaFold3_Functions.md">中文</a>
</p>

## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### This document records the commands for running AlphaFold3 on the server
---

*Path configuration*
```bash
Input dir:      /data/lmk/alphafold3_inputs       # JSON input files
Output dir:     /data/lmk/alphafold3_outputs      # predictions (cif + confidence)
Parameters dir: /data/lmk/alphafold3_parameters   # model weights af3.bin
Databases dir:  /data/lmk/alphafold3_databases    # MSA databases (~627GB)
```
Inside the container they are mounted at `/af3_inputs`, `/af3_outputs`, `/af3_parameters` and `/af3_databases`

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

Running many jobs serially is too slow; split them across several containers instead — see 03b

> **03b Protein structure prediction -- |batch job|data pipeline only|parallel containers|**

**Input**: put the dozens or hundreds of pending JSONs in `alphafold3_inputs/`

Use `scripts/af3_msa_split_parallel.py` to deal the jobs round-robin into N groups, then start N containers, one per group. Edit `GROUPS` at the top of the script to change the degree of parallelism; when it finishes it prints the matching launch command.

```bash
python /data/lmk/alphafold3_scripts/af3_msa_split_parallel.py
```

For example
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

`2>&1 | sed` prefixes every line with `[gN]`, so eight interleaved logs stay readable; the trailing `&` plus the final `wait` keeps all eight running at once.

> **03c Inspecting and stopping the parallel containers -- |batch job|parallel containers|operations|**

List the running docker containers
```bash
docker ps
```

Stop every running AF3 container. `docker ps -q` prints only the container IDs, and `$()` hands them to `stop`
```bash
docker stop $(docker ps -q --filter name=af3_g)
```

These two are enough day to day — the launch command in 03b passes `--rm`, so a container is removed as soon as it exits

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

All the example files for this workflow are in the repo under [custom template pipeline](../custom%20template%20pipeline/)

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
