import csv
import math
import os

BASE = "/scratch/la3g22/chem6090/wln_conversion"
INPUT_CSV = f"{BASE}/input/compound_dataset_1m_cleaned.csv"
WRITEWLN = "/scratch/la3g22/wiswesser/build/writewln"

TASKFARM_DIR = f"{BASE}/taskfarm_files"
SLURM_DIR = f"{BASE}/slurm_files"
RESULTS_DIR = f"{BASE}/results"

os.makedirs(TASKFARM_DIR, exist_ok=True)
os.makedirs(SLURM_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CHUNK_SIZE = 100000   # 25k rows per job

# ----------------------------
# STEP 1 — Load input CSV
# ----------------------------
rows = []
with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

num_chunks = math.ceil(len(rows) / CHUNK_SIZE)
print(f"Loaded {len(rows)} rows.")
print(f"Generating {num_chunks} taskfarm chunks...")

# ----------------------------
# STEP 2 — Build taskfarm command files
# ----------------------------
for i in range(num_chunks):
    start = i * CHUNK_SIZE
    end = min(start + CHUNK_SIZE, len(rows))
    chunk_rows = rows[start:end]

    task_file = f"{TASKFARM_DIR}/wln_commands_{i+1}.txt"
    output_file = f"{RESULTS_DIR}/chunk_{i+1}.csv"

    with open(task_file, "w") as tf:
        for row in chunk_rows:
            smiles = row["connectivity_smiles"].replace('"', '')  # safety
            cmd = (
                f'{WRITEWLN} -ismi "{smiles}" '
                f'| awk \'{{print "{smiles}," $0}}\' '
                f'>> {output_file}\n'
            )
            tf.write(cmd)

    print(f"Created task file: {task_file}")

    # ----------------------------
    # STEP 3 — Create SLURM file for this chunk
    # ----------------------------
    slurm_file = f"{SLURM_DIR}/wln_taskfarm_{i+1}.slurm"
    with open(slurm_file, "w") as sf:
        sf.write(f"""#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --partition=batch
#SBATCH --output={SLURM_DIR}/%j_wln_{i+1}.out

module load gcc/13.2.0

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

staskfarm {task_file}
""")




    print(f"Created SLURM file: {slurm_file}")

print("All taskfarm files and SLURM jobs generated successfully.")
