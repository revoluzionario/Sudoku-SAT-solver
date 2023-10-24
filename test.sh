#!/bin/bash

# List of solver names
solver_names=("Minisat22" "Cadical153" "Glucose42")

# List of encodings
encodings=("Binomial encoding" "Product encoding")

# Iterate over solver names
for solver_name in "${solver_names[@]}"; do
    # Iterate over encodings
    for encoding in "${encodings[@]}"; do
        # Run sudoku_cmd.py with foldername, solver-name, and encoding
        python sudoku_cmd.py puzzles --solver-name "$solver_name" --encoding "$encoding"


    done
done

# Run output_process.py
for solver_name in "${solver_names[@]}"; do
    for encoding in "${encodings[@]}"; do
    	echo "$solver_name, $encoding"
    	
python output_process.py

