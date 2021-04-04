import socket, sys, os, subprocess
from env import *

from utils import *

# Checks the path provided for MIDSI
if not os.path.exists(MIDSI_PATH):
  print('Midsi path not found')
  print(' => '+ MIDSI_PATH)
  exit()

# Checks if MIDSI was found on the path provided
try:
  sys.path.append(MIDSI_PATH)
  from wsmlparser.parser import *
  from service.config import *
except:
  print('Midsi was not found on the path provided')
  print(' => '+ MIDSI_PATH)
  exit()

#try:
#  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#            
#  # Ping with the server
#  sock.sendto('ping'.encode('utf-8'), (UDP_IP, UDP_PORT))
#  sock.settimeout(2)
#  data, server = sock.recvfrom(4096)
#except:
#  print('Midsi server not running in '+str(UDP_IP)+':'+str(UDP_PORT))
#  print('Plese run in a new terminal:')
#  print(' cd '+MIDSI_PATH+'/service && python3 midsi-service.py')
#  exit()

# Comandos que devo validar
# show - exibir as informações dos pacotes
# depends - exibir as dependencias dos pacotes
# install

reasoner = Reasoner()

# Curl dependencys
package = 'accountsservice'
#
#start = time.time()
reasoner.load('./Repository/Packages/'+package+'.wsml')
#finish = time.time()
#countTime = (finish-start)*1000
#
print(reasoner.execute('?z [package hasValue ?h] memberOf DependencyAtom and depends(?x,?y,?z)'))
#print(reasoner.executeProlog("depends(X,Y,Z),memberOf(Z,'DependencyAtom'),hasValue(Z,'package',H)"))