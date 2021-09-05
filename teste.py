import sys, os
from env import *
from operator import itemgetter
from utils import *

args = sys.argv[1:]

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

reasoner = Reasoner()
# reasoner.printLogLoading = True
# reasoner.printFacts = True
# reasoner.printAxioms = True
# reasoner.printQueryProlog = True

if args[0] == 'show' and len(args) == 2:
  # package = 'accountsservice'
  package = args[1]

  reasoner.load('./Repository/Packages/'+package+'.wsml')

  # Get latest version from choosed package
  packages = reasoner.execute('?packageInstance [version hasValue ?version, package hasValue "' + package + '", packageSource hasValue ?packageSource] memberOf Package and ?packageSource [uri hasValue ?uri] memberOf Source')
  if isinstance(packages, dict) and packages['error'] and 'existence_error' in packages['error']:
    print('Package ' + package + ' not found!')
    exit()
  
  packagesOrdered = sorted(packages, key=itemgetter('Version'), reverse=True)

  packageToInstall = packagesOrdered[0]

  packageProps = reasoner.execute(packageToInstall['Packageinstance'] + ' [?prop hasValue ?value] memberOf Package')
  
  excludeProps = ['package', 'version', 'packageSource']
  print('| = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ')
  print('| Package => ' + package)
  print('| Version => ' + getString(packageToInstall['Version']))
  print('| Source => ' + getString(packageToInstall['Uri']))
  for data in packageProps:
    if data['Prop'] not in excludeProps:
        print('| '+ data['Prop'].capitalize() + ' => ' + getString(data['Value']))
  print('| = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ')

if args[0] == 'depends' and len(args) == 2:
  print('DEPENDS')
  #print('?instance memberOf Package')
  #print(packageToInstall)
  #print(reasoner.execute('?z [package hasValue ?h] memberOf DependencyAtom and depends(?x,?y,?z)'))
  #print(reasoner.executeProlog("depends(X,Y,Z),memberOf(Z,'DependencyAtom'),hasValue(Z,'package',H)"))
