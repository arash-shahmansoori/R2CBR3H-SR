import json
import os


def main():
    dir_name = "results"
    dir_name_baseline = "results_baseline"

    costs, delays, status = [], [], []
    # Loop through the directory and its subdirectories
    for root, _, files in os.walk(dir_name):
        # Loop through the files
        for file in files:
            # Check if the file is a json file
            if file.endswith(".json"):
                # Get the full path of the file
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    results = json.load(f)
                    for result in results:
                        for key, _ in result.items():
                            if key.startswith("cost"):
                                costs.append(result[key])
                            elif key.startswith("elapsed"):
                                delays.append(result[key])
                            elif key.startswith("satisficed"):
                                status.append(result[key])

    costs_baseline, delays_baseline, status_baseline = [], [], []
    # Loop through the directory and its subdirectories
    for root_baseline, _, files_baseline in os.walk(dir_name_baseline):
        # Loop through the files
        for file_baseline in files_baseline:
            # Check if the file is a json file
            if file_baseline.endswith(".json"):
                # Get the full path of the file
                file_path_baseline = os.path.join(root_baseline, file_baseline)

                with open(file_path_baseline, "r") as f_baseline:
                    results_baseline = json.load(f_baseline)
                    for result_baseline in results_baseline:
                        for key_baseline, _ in result_baseline.items():
                            if key_baseline.startswith("cost"):
                                costs_baseline.append(result_baseline[key_baseline])
                            elif key_baseline.startswith("elapsed"):
                                delays_baseline.append(result_baseline[key_baseline])
                            elif key.startswith("satisficed"):
                                status_baseline.append(result_baseline[key_baseline])

    avg_cost = sum(costs) / len(costs)
    avg_delay = sum(delays) / len(delays)

    avg_cost_baseline = sum(costs_baseline) / len(costs_baseline)
    avg_delay_baseline = sum(delays_baseline) / len(delays_baseline)

    if all(status):
        overall_status = "satisfied"

    if all(status_baseline):
        overall_status_baseline = "satisfied"

    print(
        f"avg-cost:{avg_cost:.5f}$, avg-delay:{avg_delay:.2f}[sec], status:{overall_status}"
    )
    print(
        f"avg-cost:{avg_cost_baseline:.5f}$, avg-delay:{avg_delay_baseline:.2f}[sec], status:{overall_status_baseline}"
    )


if __name__ == "__main__":
    main()
