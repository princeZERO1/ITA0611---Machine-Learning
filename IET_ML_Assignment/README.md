# ITA0611 Machine Learning IET Assignment
## Crop Disease and Yield Risk Early-Warning System

Folders: `code/`, `data/`, `figures/`, `results/`, `tests/`.

The included CSV is a **synthetic educational dataset** generated with fixed seed 42 for reproducibility; it is not field-measured data.

### Run
```bash
pip install -r requirements.txt
python code/main.py
python code/candidate_elimination.py
python code/genetic_feature_selection.py
pytest
```

`code/main.py` implements KNN and Locally Weighted Regression from first principles and uses standard scikit-learn implementations for Decision Tree, Gaussian Naive Bayes and MLP. It generates validation/metric files and six figures.
