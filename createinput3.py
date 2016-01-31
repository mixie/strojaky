from collections import defaultdict
import pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

druh={'S':1,'A':2,'P':3,'N':4,'V':5,'D':6,'E':7,'O':8,'T':9,'J':10} #druhy 1-10 standartne
druh=defaultdict(lambda:0,druh)
rod={'m':1,'i':1,'f':2,'n':3,'h':4,'o':4} #muzsky z/n -1,zensky -2, stredny-3 , 4 - neurceny,vseobnecny
rod=defaultdict(lambda:0,rod)
cislo={'s':1,'p':2} #1 - jednotne, 2 -mnozne
cislo=defaultdict(lambda:0,cislo)
osoba={'a':1,'b':2,'c':3}
osoba=defaultdict(lambda:0,osoba)
morfvectors=set()
f = open("morf.txt")
i=0
words2=list(pickle.load(open("commonwords.p", "rb")))
for l in f:
	i+=1
	if i%100000==0:
		print i,' ',len(morfvectors)
	line = l.strip().split()
	if line[1] in words2:
		morf=line[2]
		try:
			if druh[morf[0]]==5:
				morfvectors.add((line[1],(druh[morf[0]],rod[morf[5]],cislo[morf[3]],0,osoba[morf[4]])))
			elif druh[morf[0]]>0 and druh[morf[0]]<5:
				morfvectors.add((line[1],(druh[morf[0]],rod[morf[2]],cislo[morf[3]],int(morf[4]),0)))
			else:
				morfvectors.add((line[1],(druh[morf[0]],0,0,0,0)))
		except:
			pass
morfvecsort=list(morfvectors)
morfvecsort.sort()
for (s1,(s2,s3,s4,s5,s6)) in morfvecsort:
	print s1,' ',s2,' ',s3,' ',s4,' ',s5,' ',s6