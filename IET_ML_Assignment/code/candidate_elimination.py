
from itertools import product
domains=[["Low","High"],["Absent","Present"],["Absent","Present"]]
examples=[(("High","Present","Present"),"Yes"),(("High","Present","Absent"),"Yes"),(("Low","Absent","Absent"),"No"),(("Low","Present","Present"),"No")]
H=list(product(*[d+["?"] for d in domains]))
def covers(h,x): return all(a=="?" or a==b for a,b in zip(h,x))
vs=[h for h in H if all(covers(h,x)==(y=="Yes") for x,y in examples)]
print("Final Version Space:"); [print(h) for h in vs]
