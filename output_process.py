import os

output_folder = "puzzles/output"

# Dictionary to store total time and count for each group of filenames
filename_stats = {}

# Iterate over each file in the output folder
for filename in os.listdir(output_folder):
    if filename.endswith(".txt"):
        parts = filename.split("_")
        if parts[-1].split(".")[0].isdigit():
            group_name = "_".join(parts[0:2], parts[-1].split(".")[0])
        else:
            group_name = "_".join(parts[0:2])
        if group_name not in filename_stats:
            filename_stats[group_name] = {"total_time": 0, "count": 0}
        with open(os.path.join(output_folder, filename)) as puzzle_file:
            lines = puzzle_file.readlines()
            time_line = lines[-3]
            time = float(time_line.split(":")[1])
            filename_stats[group_name]["total_time"] += time
            filename_stats[group_name]["count"] += 1

# Calculate average solving time for each group of filenames
average_times = {}
for group_name, stats in filename_stats.items():
    average_time = stats["total_time"] / stats["count"]
    average_times[group_name] = average_time

# Print average solving time for each group of filenames
for group_name, average_time in average_times.items():
    print(f"Average solving time for {group_name}: {average_time}")