import logic
import argparse
import os

def check_range(value, valid_range):
    if value not in valid_range:
        raise argparse.ArgumentTypeError(f"Invalid value: {value}. Must be one of {valid_range}")
    return value

parser = argparse.ArgumentParser(description="Sudoku SAT Batch-solver", prog="sudoku_cmd")

parser.add_argument("foldername")
parser.add_argument("--solver-name", "-s", default="Minisat22", type=lambda value: check_range(value, ["Minisat22", "Cadical153", "Glucose42"]))
parser.add_argument("--encoding", "-e", default="Binomial encoding", type=lambda value: check_range(value, ["Binomial encoding", "Product encoding"]))
args = parser.parse_args()
target_folder = args.foldername

if not os.path.isdir(target_folder):
    print("Folder doesn't exist!")
    raise SystemExit(1)

output_folder = os.path.join(target_folder, "output")
os.makedirs(output_folder, exist_ok=True)

def get_unique_filename(file_path):
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    new_file_name = file_name + "_output"
    counter = 1
    while os.path.exists(os.path.join(output_folder, new_file_name + file_ext)):
        new_file_name = file_name + "_output_" + str(counter)
        counter += 1
    return new_file_name + file_ext

def export_file(filename, solver_name, encoding):
    slogic = logic.SudokuLogic([solver_name, encoding, filename])
    slogic.readFile()
    slogic._solve()
    board = slogic.export_board()
    output_stats = slogic.export_stats()
    output_filename = get_unique_filename(filename)
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, "w") as f:
        for row in board:
            line = ' '.join(str(element) for element in row)
            f.write(line + '\n')        
        f.write("Time: " + str(output_stats[0]) + "\n")
        f.write("Number of variables: " + str(output_stats[1]) + "\n")
        f.write("Number of clauses: " + str(output_stats[2]) + "\n")

# Iterate over each file in the folder
for filename in os.listdir(target_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(target_folder, filename)
        export_file(file_path, solver_name=args.solver_name, encoding=args.encoding)