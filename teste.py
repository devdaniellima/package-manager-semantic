import sys
import time

sys.path.append('../')
from wsmlparser.parser import *
reasoner = Reasoner()
print("== Teste.py")
#reasoner.load('wsmlcodes/ont1-ShipmentOntology/ShipmentOntology.wsml')
start = time.time()
reasoner.load('./Repository/Packages/teste.wsml')
finish = time.time()
countTime = (finish-start)*1000
print()
#print(str(round(countTime, 2)) + ' ms')
#print(str(round(countTime, 2) / 1000) + ' s')
#print(str(round(countTime, 2) / 1000 / 60) + ' min')
#print()
#print(reasoner.executeProlog('depends(X,Y,Z)'))
#print(reasoner.execute('packageDependences("code",?dependency)'))
#print(reasoner.execute('packageUri("code",?repo,?package)'))
#print(reasoner.execute("?x memberOf Package"))
print(reasoner.executeProlog('concept(X)'))
#print(reasoner.executeProlog('relationType(X,Y)'))
