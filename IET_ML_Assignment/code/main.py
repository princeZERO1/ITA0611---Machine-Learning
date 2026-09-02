
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,mean_absolute_error,mean_squared_error
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data/crop_risk_dataset.csv"; FIG=ROOT/"figures"; RES=ROOT/"results"
FIG.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
df=pd.read_csv(DATA)

features=["temperature_c","rainfall_mm","humidity_pct","soil_moisture","soil_n_mgkg","soil_p_mgkg","soil_k_mgkg","soil_ph","crop_type","leaf_spot","wilting","pest_damage","previous_yield_tpha"]
num=[c for c in features if c!="crop_type"]; cat=["crop_type"]
X=df[features]; y=df["disease_risk"]
Xtr0,Xte0,ytr,yte=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
prep=ColumnTransformer([("num",StandardScaler(),num),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat)])
Xtr=np.asarray(prep.fit_transform(Xtr0)); Xte=np.asarray(prep.transform(Xte0))

def knn_predict(X_train,y_train,X_test,k=5):
    X_train=np.asarray(X_train,float); X_test=np.asarray(X_test,float); y_train=np.asarray(y_train)
    out=[]
    for q in X_test:
        d=np.sqrt(np.sum((X_train-q)**2,axis=1)); idx=np.argsort(d)[:k]
        lab,cnt=np.unique(y_train[idx],return_counts=True); out.append(lab[np.argmax(cnt)])
    return np.array(out)

ks=[1,3,5,7,9,11,15,21]; rows=[]
for k in ks:
    p=knn_predict(Xtr,ytr.values,Xte,k)
    rows.append([k,accuracy_score(yte,p),precision_score(yte,p,average="weighted",zero_division=0),recall_score(yte,p,average="weighted",zero_division=0),f1_score(yte,p,average="weighted",zero_division=0)])
knn=pd.DataFrame(rows,columns=["k","accuracy","precision","recall","f1"]); knn.to_csv(RES/"knn_validation.csv",index=False)
best_k=int(knn.loc[knn.f1.idxmax(),"k"]); knn_pred=knn_predict(Xtr,ytr.values,Xte,best_k)
plt.figure(figsize=(7,4.5)); plt.plot(knn.k,knn.accuracy,"o-",label="Accuracy"); plt.plot(knn.k,knn.f1,"s-",label="Weighted F1"); plt.xlabel("K"); plt.ylabel("Score"); plt.title("KNN Validation Curve"); plt.grid(alpha=.25); plt.legend(); plt.tight_layout(); plt.savefig(FIG/"01_knn_validation_curve.png",dpi=180); plt.close()

def locally_weighted_regression_predict(X_train,y_train,Xq,tau=1.0,ridge=1e-5):
    X_train=np.asarray(X_train,float); y_train=np.asarray(y_train,float); Xq=np.asarray(Xq,float)
    xb=np.c_[np.ones(len(X_train)),X_train]; I=np.eye(xb.shape[1]); I[0,0]=0; out=[]
    for q in Xq:
        q_b=np.r_[1.,q]; d2=np.sum((X_train-q)**2,axis=1); w=np.exp(-d2/(2*tau*tau)); W=np.diag(w)
        theta=np.linalg.pinv(xb.T@W@xb+ridge*I)@(xb.T@W@y_train); out.append(q_b@theta)
    return np.array(out)

yf=["temperature_c","rainfall_mm","humidity_pct","soil_moisture","soil_n_mgkg","soil_p_mgkg","soil_k_mgkg","soil_ph","previous_yield_tpha"]
Xa=df[yf].values; ya=df.expected_yield_tpha.values
Xa_tr,Xa_te,ya_tr,ya_te=train_test_split(Xa,ya,test_size=.20,random_state=42)
ss=StandardScaler(); Xa_tr=ss.fit_transform(Xa_tr); Xa_te=ss.transform(Xa_te)
taus=[.1,.25,.5,.75,1,1.5,2,3]; lr=[]
for t in taus:
    p=locally_weighted_regression_predict(Xa_tr,ya_tr,Xa_te,t); lr.append([t,mean_absolute_error(ya_te,p),np.sqrt(mean_squared_error(ya_te,p))])
lwr=pd.DataFrame(lr,columns=["tau","MAE","RMSE"]); lwr.to_csv(RES/"lwr_tau_analysis.csv",index=False)
best_tau=float(lwr.loc[lwr.RMSE.idxmin(),"tau"]); lwr_pred=locally_weighted_regression_predict(Xa_tr,ya_tr,Xa_te,best_tau)
plt.figure(figsize=(7,4.5)); plt.plot(lwr.tau,lwr.RMSE,"o-"); plt.xlabel("Weighting parameter tau"); plt.ylabel("RMSE (t/ha)"); plt.title("LWR Sensitivity to Weighting Parameter"); plt.grid(alpha=.25); plt.tight_layout(); plt.savefig(FIG/"02_lwr_tau_curve.png",dpi=180); plt.close()

tree=Pipeline([("prep",prep),("model",DecisionTreeClassifier(max_depth=5,criterion="gini",random_state=42))]); tree.fit(Xtr0,ytr); tree_pred=tree.predict(Xte0)
(RES/"decision_tree_rules.txt").write_text(export_text(tree.named_steps["model"],feature_names=list(prep.get_feature_names_out())))

nb=Pipeline([("prep",prep),("model",GaussianNB())]); nb.fit(Xtr0,ytr); nb_pred=nb.predict(Xte0)
mlp=Pipeline([("prep",prep),("model",MLPClassifier(hidden_layer_sizes=(32,16),activation="relu",solver="adam",alpha=.0005,max_iter=800,random_state=42))]); mlp.fit(Xtr0,ytr); mlp_pred=mlp.predict(Xte0)

def met(name,t,p): return [name,accuracy_score(t,p),precision_score(t,p,average="weighted",zero_division=0),recall_score(t,p,average="weighted",zero_division=0),f1_score(t,p,average="weighted",zero_division=0)]
comparison=pd.DataFrame([met("KNN",yte,knn_pred),met("Decision Tree",yte,tree_pred),met("Gaussian Naive Bayes",yte,nb_pred),met("MLP",yte,mlp_pred)],columns=["model","accuracy","precision","recall","f1"])
comparison.to_csv(RES/"classification_comparison.csv",index=False)
pd.DataFrame([["LWR",best_tau,mean_absolute_error(ya_te,lwr_pred),np.sqrt(mean_squared_error(ya_te,lwr_pred))]],columns=["model","tau","MAE","RMSE"]).to_csv(RES/"lwr_final_metrics.csv",index=False)

plt.figure(figsize=(7,4.5)); df.groupby("disease_risk").yield_loss_pct.mean().reindex(["Low","Medium","High"]).plot(kind="bar"); plt.ylabel("Mean yield loss (%)"); plt.title("Average Yield Loss by Disease-Risk Category"); plt.tight_layout(); plt.savefig(FIG/"03_risk_vs_yield_loss.png",dpi=180); plt.close()
plt.figure(figsize=(7,4.5)); plt.scatter(df.humidity_pct,df.yield_loss_pct,alpha=.55); plt.xlabel("Humidity (%)"); plt.ylabel("Yield loss (%)"); plt.title("Humidity vs Yield Loss"); plt.grid(alpha=.2); plt.tight_layout(); plt.savefig(FIG/"04_humidity_vs_yield_loss.png",dpi=180); plt.close()
plt.figure(figsize=(7,4.5)); df.crop_type.value_counts().plot(kind="bar"); plt.xlabel("Crop type"); plt.ylabel("Samples"); plt.title("Dataset Distribution by Crop Type"); plt.tight_layout(); plt.savefig(FIG/"05_crop_distribution.png",dpi=180); plt.close()
plt.figure(figsize=(7,4.5)); comparison.set_index("model")[["accuracy","precision","recall","f1"]].plot(kind="bar"); plt.ylabel("Score"); plt.ylim(0,1); plt.title("Classification Model Comparison"); plt.xticks(rotation=20); plt.tight_layout(); plt.savefig(FIG/"06_model_comparison.png",dpi=180); plt.close()

def integrated_warning(record):
    x=pd.DataFrame([record]); disease=tree.predict(x)[0]
    q=ss.transform(np.array([[record[c] for c in yf]],float)); pred_y=locally_weighted_regression_predict(Xa_tr,ya_tr,q,best_tau)[0]
    if disease=="High": action="High alert: inspect immediately; verify irrigation/drainage and follow crop-specific disease-management guidance."
    elif disease=="Medium": action="Warning: increase monitoring; inspect leaves/pests and correct moisture or nutrient stress."
    else: action="Routine watch: maintain balanced irrigation and soil management."
    return disease,float(pred_y),action

if __name__=="__main__":
    print("Best K:",best_k); print("Best tau:",best_tau); print(comparison.round(3).to_string(index=False)); print(lwr.round(3).to_string(index=False))
