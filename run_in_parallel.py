import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

INPUT_DIR = "input"
OUTPUT_DIR = "output"
SCRIPT_NAME = "bort.py"
NUM_CORES = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_script(input_file):
    input_path = os.path.join(INPUT_DIR, input_file)
    output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(input_file)[0]}.out")
    
    try:
        result = subprocess.run(
            ["python", SCRIPT_NAME, input_path],
            capture_output=True,
            text=True,
            check=True
        )
        with open(output_path, 'w') as f:
            f.write(result.stdout)
        return f"{input_file} ✔"
    except subprocess.CalledProcessError as e:
        return f"{input_file} ✖ Error: {e.stderr}"

def main():
    input_files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]

    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        futures = {executor.submit(run_script, f): f for f in input_files}
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()
