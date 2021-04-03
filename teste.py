import sys
import time

MIDSI_PATH = '/home/daniel/Documentos/midsi'

sys.path.append(MIDSI_PATH)
from wsmlparser.parser import *

reasoner = Reasoner()

# Curl dependencys
package = 'curl'

start = time.time()
reasoner.load('./Repository/Packages/'+package+'.wsml')
finish = time.time()
countTime = (finish-start)*1000

print(reasoner.execute('depends(?x,?y,?z)'))