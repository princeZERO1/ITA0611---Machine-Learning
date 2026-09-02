
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"code"))
import main
def test_knn():
    p=main.knn_predict(np.array([[0,0],[1,1],[0,1]]),np.array(["A","B","A"]),np.array([[.1,.1]]),1)
    assert p[0]=="A"
def test_lwr():
    p=main.locally_weighted_regression_predict(np.array([[0.],[1.],[2.]]),np.array([0.,1.,2.]),np.array([[1.]]),1)
    assert np.isfinite(p[0])
def test_data(): assert main.DATA.exists()
