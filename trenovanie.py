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

#volanie programu python trenovanie.py <trenovaci subor> <testovaci subor> <subor s vektormi>
#<slovny druh, pre ktory sa trenuje - 0 pri trenovani slovnych druhov, inak 1-10> <trenovany parameter rod/cislo... 1-4>
#<metoda svm/forest/multilabel> <1/0 ci chceme zistovat multiclass skore>
 
morftrainingfile = open(sys.argv[1]) #trainingfile
morftestingfile = open(sys.argv[2]) #testingfile
vectorfile = open(sys.argv[3]) #vectorfile

#nacitanie suborov
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
#predpriprava vstupu a vystupu pre trenovanie, vyber vystupneho stlpca 
#a zbavenie sa duplicitnych dat
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

#samotne trenovanie, vyber metody
method = sys.argv[6]
if method=='svm':
	clf = svm.SVC(decision_function_shape='ovo',probability=True)
elif method=='forest':
	clf=RandomForestClassifier()
elif method=='multilabel':
	#trenovanie multilabel, tj. viac vystupov pre jedne vstup
	clf=OneVsRestClassifier(svm.SVC(decision_function_shape='ovo'))
	Xtrain=list(set(Xtrain))
	Ytrain=[]
	for xt in Xtrain:
		Ytrain.append(tuple([y for (x,y) in train if x==xt]))
	Ytrain=MultiLabelBinarizer().fit_transform(Ytrain)
	Xtest=list(set(Xtest))
	Ytest=[]
	for xt in Xtest:
		Ytest.append(tuple([y for (x,y) in test if x==xt]))
	Ytest=MultiLabelBinarizer().fit_transform(Ytest)


clf.fit(Xtrain,Ytrain)
print "train score: ",clf.score(Xtrain,Ytrain)
print "test score: ",clf.score(Xtest,Ytest)

#vyhodnocovanie multiclass skore, ako definovane v popise projektu
testpr=zip(Xtest+Xtrain,Ytest+Ytrain)
testprob=list(set(testpr))
Xtest=list(set([x for (x,y) in testprob]))
score=0
if int(sys.argv[7])==1:
	predictedY=clf.predict_proba(Xtest)
	for i in range(len(Xtest)):
		res=[y for (x,y) in testprob if x==Xtest[i]]
		resS=set(res)
		realres=predictedY[i]
		points=0
		for i in range(len(realres)):
			if i in resS and realres[i]>1.0/len(realres):
				points+=1
			if i not in resS and realres[i]>1.0/len(realres):
				points-=0.5
		if points<0:
			points=0
		score+=float(points)/len(resS)
	score = score/len(Xtest)
	print 'multilabel score:',score


