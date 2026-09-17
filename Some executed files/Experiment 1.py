"""
Program 1: FIND-S Algorithm
----------------------------
Finds the most specific hypothesis that fits all the POSITIVE training
examples in the given training data.

Dataset: enjoysport.csv
Each row = one training instance with attributes describing weather
conditions, and a target label EnjoySport (Yes/No).
"""

import pandas as pd


def find_s_algorithm(csv_file):
    # Load the training data
    data = pd.read_csv(csv_file)
    print("Training data:\n", data, "\n")

    # Separate attributes (all columns except last) and target (last column)
    attributes = data.iloc[:, :-1].values
    target = data.iloc[:, -1].values

    num_attributes = attributes.shape[1]

    # Step 1: Initialize hypothesis to the most specific one possible
    hypothesis = ['0'] * num_attributes

    # Step 2: Loop over every training example
    for i, row in enumerate(attributes):
        if target[i].strip().lower() == "yes":       # consider only positive examples
            if hypothesis == ['0'] * num_attributes:
                # First positive example -> hypothesis becomes that example
                hypothesis = list(row)
            else:
                # Generalize hypothesis just enough to include this example
                for j in range(num_attributes):
                    if hypothesis[j] != row[j]:
                        hypothesis[j] = '?'
            print(f"After example {i + 1} (positive) -> hypothesis: {hypothesis}")
        else:
            print(f"After example {i + 1} (negative) -> ignored, hypothesis unchanged: {hypothesis}")

    return hypothesis


if __name__ == "__main__":
    final_hypothesis = find_s_algorithm("enjoysport.csv")
    print("\nFinal Maximally Specific Hypothesis found by FIND-S:")
    print(final_hypothesis)
