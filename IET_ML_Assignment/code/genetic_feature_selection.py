
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
ROOT=Path(__file__).resolve().parents[1]; df=pd.read_csv(ROOT/"data/crop_risk_dataset.csv")
features=["temperature_c","rainfall_mm","humidity_pct","soil_moisture","soil_n_mgkg","soil_p_mgkg","soil_k_mgkg","soil_ph","leaf_spot","wilting","pest_damage","previous_yield_tpha"]
Xtr,Xte,ytr,yte=train_test_split(df[features],df.disease_risk,test_size=.25,random_state=42,stratify=df.disease_risk)
def fitness(mask):
    sel=[f for f,m in zip(features,mask) if m]
    if not sel:return 0
    m=Pipeline([("s",StandardScaler()),("t",DecisionTreeClassifier(max_depth=4,random_state=42))]); m.fit(Xtr[sel],ytr); p=m.predict(Xte[sel])
    return f1_score(yte,p,average="weighted")-.01*sum(mask)/len(mask)
rng=np.random.default_rng(7); pop=rng.integers(0,2,(20,len(features)))
for _ in range(15):
    sc=np.array([fitness(x) for x in pop]); elite=pop[np.argsort(sc)[-4:]]; new=[e.copy() for e in elite]
    while len(new)<20:
        a,b=elite[rng.integers(4)],elite[rng.integers(4)]; cut=rng.integers(1,len(features)); child=np.r_[a[:cut],b[cut:]]
        mut=rng.random(len(features))<.08; child[mut]=1-child[mut]; new.append(child)
    pop=np.array(new)
sc=np.array([fitness(x) for x in pop]); best=pop[np.argmax(sc)]; selected=[f for f,m in zip(features,best) if m]
pd.DataFrame({"selected_feature":selected}).to_csv(ROOT/"results/ga_selected_features.csv",index=False)
(ROOT/"results/ga_summary.txt").write_text(f"Best fitness: {sc.max():.4f}\nSelected features ({len(selected)}): {selected}\n")
print(selected,sc.max())
