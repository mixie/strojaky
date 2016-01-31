import pickle
from collections import Counter
from sklearn.datasets import make_multilabel_classification
from sklearn import tree
from sklearn import svm
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import sys

morftrainingfile = open(sys.argv[1]) #trainingfile
morftestingfile = open(sys.argv[2]) #testingfile
vectorfile = open(sys.argv[3]) #vectorfile

dtrain=defaultdict(list)
for l in morftrainingfile:
	line = l.strip().split()
	dtrain[line[0]].append(tuple(map(int,line[1:])))
dtest=defaultdict(list)
for l in morftestingfile:
	line = l.strip().split()
	dtest[line[0]].append(tuple(map(int,line[1:])))
dvector=defaultdict(list)
for l in vectorfile:
	line = l.strip().split()
	dvector[line[0]]=tuple(line[1:])
test=[]
train=[]
for k,v in dtrain.items():
	for val in v:
		train.append((dvector[k],val))
for k,v in dtest.items():
	for val in v:
		test.append((dvector[k],val))
trengramkat=sys.argv[4]
if int(trengramkat)==0:
	train=[(x,y[0]) for(x,y) in train if y[0]!=0]
	test=[(x,y[0]) for(x,y) in test if y[0]!=0]
else:
	trengramkat2= sys.argv[5]
	train=[(x,y[int(trengramkat2)]) for (x,y) in train if y[0]==int(trengramkat)]
	test=[(x,y[int(trengramkat2)]) for (x,y) in test if y[0]==int(trengramkat)]
train=list(set(train))
test=list(set(test))

Xtrain=[i[0] for i in train]
Ytrain=[i[1] for i in train]
Xtest=[i[0] for i in test]
Ytest=[i[1] for i in test]

method = sys.argv[6]
if method=='svm':
	clf = svm.SVC(decision_function_shape='ovo',probability=True)
elif method=='forest':
	clf=RandomForestClassifier()
elif method=='multiclass':
	clf=OneVsRestClassifier(svm.SVC(kernel='linear'))
	Xtrain=list(set(Xtrain))
	Ytrain=[]
	for xt in Xtrain:
		Ytrain.append([y for (x,y) in train if x==xt])
	print Ytrain
	Ytrain=MultiLabelBinarizer().fit_transform(Ytrain)
	Xtest=list(set(Xtest))
	Ytest=[]
	for xt in Xtest:
		Ytest.append([y for (x,y) in test if x==xt])
	Ytest=MultiLabelBinarizer().fit_transform(Ytest)


clf.fit(Xtrain,Ytrain)
print "train score: ",clf.score(Xtrain,Ytrain)
print "test score: ",clf.score(Xtest,Ytest)
X=Xtrain+Xtest
Y=Ytest+Ytrain
count=len(Counter(Y))
if sys.argv[7]==1:
	predictedY=clf.predict_proba(X)
	oldelem=0
	if trengramkat!=0:
		for el in X:
			if el!=oldelem:
				indexes=[i for i,x in enumerate(X) if x == el]
				res=[]
				for i in indexes:
					res.append(Y[i])
				resS=set(res)
				bad=False
				for y in predictedY[indexes[0]]:
					if y in 
				for r in resS:
					if predictedY[indexes[0]][int(r)-1]<(1.0/count):
						bad=True
				if bad:
					wrong+=1
				else:
					good+=1
				oldelem=el

	print "wrong ",wrong
	print "good ",good
