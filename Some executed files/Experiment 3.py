"""
Program 3: ID3 Decision Tree Algorithm
-----------------------------------------
Builds a decision tree from training data using Information Gain
(based on Entropy), then uses the tree to classify a new sample.

Dataset: playtennis.csv
Attributes: Outlook, Temperature, Humidity, Wind
Target:     PlayTennis (Yes/No)
"""

import math
import pprint
from collections import Counter

import pandas as pd



# ---------- Core math: entropy & information gain ----------

def entropy(values):
    """Entropy of a list of class labels."""
    counts = Counter(values)
    total = len(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def information_gain(df, split_attribute, target_attribute):
    """Information gain from splitting df on split_attribute."""
    total_entropy = entropy(df[target_attribute])

    weighted_entropy = 0.0
    for value, subset in df.groupby(split_attribute):
        weight = len(subset) / len(df)
        weighted_entropy += weight * entropy(subset[target_attribute])

    return total_entropy - weighted_entropy


# ---------- ID3 tree construction ----------

def id3(df, target_attribute, attribute_names, default_class=None):
    class_counts = Counter(df[target_attribute])

    # Base case 1: all examples have the same class -> return that class (leaf)
    if len(class_counts) == 1:
        return next(iter(class_counts))

    # Base case 2: no data left or no attributes left -> return majority/default class
    if df.empty or not attribute_names:
        return default_class

    # Majority class here, used as default for empty branches
    default_class = max(class_counts, key=class_counts.get)

    # Choose the attribute with the highest information gain
    gains = {attr: information_gain(df, attr, target_attribute) for attr in attribute_names}
    best_attr = max(gains, key=gains.get)

    print(f"Chosen split attribute: {best_attr}  (Information Gain = {gains[best_attr]:.4f})")

    tree = {best_attr: {}}
    remaining_attrs = [a for a in attribute_names if a != best_attr]

    # Recurse for each value of the best attribute
    for value, subset in df.groupby(best_attr):
        subtree = id3(subset, target_attribute, remaining_attrs, default_class)
        tree[best_attr][value] = subtree

    return tree


# ---------- Classification using the learned tree ----------

def classify(tree, sample):
    """Traverse the tree dict to classify a new sample (a dict of attribute:value)."""
    if not isinstance(tree, dict):
        return tree  # reached a leaf node

    attribute = next(iter(tree))
    value = sample.get(attribute)

    subtree = tree[attribute].get(value)
    if subtree is None:
        return "Unknown (value not seen during training)"

    return classify(subtree, sample)


if __name__ == "__main__":
    data = pd.read_csv("playtennis.csv")
    print("Training data:\n", data, "\n")

    target_attr = "PlayTennis"
    attributes = [c for c in data.columns if c != target_attr]

    print("Building the decision tree using ID3...\n")
    decision_tree = id3(data, target_attr, attributes)

    print("\nLearned Decision Tree (nested dict form):")
    pprint.pprint(decision_tree)

    # Classify a new, unseen sample
    new_sample = {
        "Outlook": "Sunny",
        "Temperature": "Cool",
        "Humidity": "High",
        "Wind": "Strong",
    }

    prediction = classify(decision_tree, new_sample)

    print("\nNew sample to classify:", new_sample)
    print("ID3 Prediction -> PlayTennis =", prediction)

