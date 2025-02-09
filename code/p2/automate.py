import subprocess

# Path to the Bash script
bash_script = "./start.sh"
python_script = "client.py"

# List of concurrent client counts to test
client_counts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Store execution times
execution_times = {}

for count in client_counts:
    print(f"Running benchmark with {count} clients...")
    result = subprocess.run(["bash", bash_script, python_script, str(count)], capture_output=True, text=True)
    print(result.stdout)
    execution_times[count] = result.stdout

# Print collected execution times
print("\nExecution Times:")
for count, time in execution_times.items():
    print(f"{count} clients: {time}")
with open("multithread_host.txt", "w") as f:
    for count, time in execution_times.items():
        f.write(f"{count} clients: {time}\n")
