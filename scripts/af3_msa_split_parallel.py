#!/usr/bin/env python3
"""把 /data/lmk/alphafold3_inputs/ 里的 JSON 轮转切分到 N 组，供多容器并行跑 data pipeline。

只做切分，不启动容器；跑完会打印可直接复制的启动命令。
"""
import os, shutil

# ══ 改这里 ═════════════════════════════════════════════════════════════════
GROUPS = 8            # 切成几组（= 打算起几个容器）
JACKHMMER_CPU = 8     # 每个 jackhmmer 用几个核，仅用于生成命令
# ══════════════════════════════════════════════════════════════════════════
#
# 怎么调 GROUPS：4 个 jackhmmer 并行启动但耗时悬殊（bfd ~2min / uniref90 ~11min /
# uniprot ~15min / mgy_clusters ~40min），约 6 成时间只剩 MGnify 一个在跑，此时每个
# 容器只占 JACKHMMER_CPU 个核。所以 GROUPS × JACKHMMER_CPU ≈ 总核数只是**下限** ——
# jackhmmer 不会真吃满分给它的核（读库、建 profile、去重是单线程，还有磁盘等待）。
#   load 远低于核数 且 top 里 wa ≈ 0  → 加 GROUPS
#   load 上不去 或 wa 明显 >0         → 磁盘 IO 到顶，减 GROUPS

IN = "/data/lmk/alphafold3_inputs"
OUT = "/data/lmk/alphafold3_outputs"
SPLIT = "/data/lmk/af3_inputs_split"
PARAMS = "/data/lmk/alphafold3_parameters"
DBS = "/data/lmk/alphafold3_databases"

jobs = sorted(f for f in os.listdir(IN) if f.endswith(".json"))
shutil.rmtree(SPLIT, ignore_errors=True)
for i, f in enumerate(jobs):
    d = os.path.join(SPLIT, f"g{i % GROUPS}")
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(IN, f), d)

print(f"{len(jobs)} 个任务 → {GROUPS} 组:",
      [len(os.listdir(os.path.join(SPLIT, f"g{g}"))) for g in range(GROUPS)])
print(f"\n切分完成 → {SPLIT}\n\n启动命令（前台实时输出，每行带 [gN] 前缀）：\n")
print(f"""for g in {' '.join(str(g) for g in range(GROUPS))}; do
  docker run --rm --name af3_g$g \\
    --volume {SPLIT}/g$g:/af3_inputs \\
    --volume {OUT}:/af3_outputs \\
    --volume {PARAMS}:/af3_parameters \\
    --volume {DBS}:/af3_databases \\
    -e XLA_PYTHON_CLIENT_PREALLOCATE=false \\
    alphafold3 \\
    python run_alphafold.py \\
      --input_dir=/af3_inputs \\
      --model_dir=/af3_parameters \\
      --db_dir=/af3_databases \\
      --output_dir=/af3_outputs \\
      --jackhmmer_n_cpu={JACKHMMER_CPU} \\
      --norun_inference 2>&1 | sed "s/^/[g$g] /" &
done
wait

（先 tmux new -s af3 再跑，断线不丢；Ctrl+B 然后 D 脱离）""")
