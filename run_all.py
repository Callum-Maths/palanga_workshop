import os
import subprocess
from time import sleep
import csv

#Attempt to make numpy only use a single thread!
os.environ["MKL_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 
os.environ["OMP_NUM_THREADS"] = "1"


# creates a folder in the current working directory
def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
        

if __name__ == "__main__":

    line_vals = [line for line in range(1, 73104)]  # Example line values
    cuda_devices = [None]
    num_commands = 8

    runfile = "run_job"

    jobname = "Data_category"

    # Run files
    processes = {device: [] for device in cuda_devices}
    device_index = 0

    csv_filename = "genres_output1.csv"
    print(f"Creating CSV file: {os.path.abspath(csv_filename)}")
    with open(csv_filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["line", "Name" , "genres"])
    print(f"CSV file created at: {os.path.abspath(csv_filename)}")

    for line in line_vals:
        
        filename = jobname
        
        #Loop over all, not just the best hyperparameters
        paramname = f"line_{line:.0f}"

        # Find an available CUDA device
        while True:
            cuda_device = cuda_devices[device_index]
            device_index = (device_index + 1) % len(cuda_devices)

            if len(processes[cuda_device]) < num_commands:
                break

            # Check if any process has finished
            for p in processes[cuda_device]:
                if p.poll() is not None:  # Process finished
                    processes[cuda_device].remove(p)
            sleep(1)  # Wait a bit before checking again

        runfile_path = os.path.join(os.path.dirname(__file__), f"{runfile}.py")
                            # Adjust the CUDA parameter for CPU
        if cuda_device is None:
            params = " --line {}"
            params = params.format(line)
        else:
            params = " --line {}"
            params = params.format(line)

        command = f"python {runfile_path} {params}"
        print("running command:", command)

        # Start a new process
        p = subprocess.Popen(command, shell=True)
        processes[cuda_device].append(p)

    # Wait for all remaining processes to finish
    for device in cuda_devices:
        for p in processes[device]:
            p.wait()