"""
Program 2: Candidate-Elimination Algorithm
--------------------------------------------
Outputs a description of the set of ALL hypotheses consistent with the
training examples, represented by the Specific boundary (S) and the
General boundary (G) of the version space.

Dataset: enjoysport.csv (same as FIND-S)
"""

import numpy as np
import pandas as pd


def learn(concepts, target):
    # Step 1: Initialize S to the first training instance (most specific)
    specific_h = concepts[0].copy()
    # Initialize G to the most general hypotheses (one '?' hypothesis per attribute)
    general_h = [["?" for _ in range(len(specific_h))] for _ in range(len(specific_h))]

    print("Initial Specific Hypothesis (S0):", specific_h)
    print("Initial General Hypothesis (G0):", general_h, "\n")

    for i, h in enumerate(concepts):
        print(f"--- Example {i + 1}: {list(h)}  Label: {target[i]} ---")

        if target[i].strip().lower() == "yes":
            # Positive example: generalize S, remove inconsistent hypotheses from G
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'

        elif target[i].strip().lower() == "no":
            # Negative example: specialize G, S stays the same
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'

        print("S:", specific_h)
        print("G:", [g for g in general_h if g != ['?'] * len(specific_h)], "\n")

    # Remove the fully general ('?','?',...,'?') placeholder hypotheses from G
    indices = [i for i, val in enumerate(general_h) if val == ['?'] * len(specific_h)]
    for i in indices[::-1]:
        general_h.remove(['?'] * len(specific_h))

    return specific_h, general_h


if __name__ == "__main__":
    data = pd.read_csv("enjoysport.csv")
    print("Training data:\n", data, "\n")

    concepts = np.array(data.iloc[:, 0:-1])
    target = np.array(data.iloc[:, -1])

    s_final, g_final = learn(concepts, target)

    print("=" * 50)
    print("Final Specific Boundary S:")
    print(s_final)
    print("\nFinal General Boundary G:")
    print(g_final)
