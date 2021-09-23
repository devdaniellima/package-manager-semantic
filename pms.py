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
  print('Midsi was not found or not configured on the path provided')
  print(' => '+ MIDSI_PATH)
  print('Check the midsi installation process in the README.md of midsi')
  exit()

reasoner = Reasoner()
packageDependencyControlArray = []
# reasoner.printLogLoading = True
# reasoner.printFacts = True
# reasoner.printAxioms = True
# reasoner.printQueryProlog = True
if len(args) == 0:
  print('* show [package]')
  print('* depends [package]')
  print('* depends [package] --all')
  exit()

pwd = '/Users/danieldev/Documents/package-manager-semantic'

def dependencyOf(package, level, header, allDependencys):
  
  reasoner.load(pwd + '/Repository/Packages/'+package+'.wsml')

  #for countPipe in range(level):
  #  pipeHeader += '│ '
  
  # Get latest version from choosed package
  packages = reasoner.execute('?packageInstance [version hasValue ?version, package hasValue "' + package + '", packageSource hasValue ?packageSource] memberOf Package and ?packageSource [uri hasValue ?uri] memberOf Source')
  if isinstance(packages, dict) and packages['error'] and 'existence_error' in packages['error'] or len(packages) == 0:
    line = 'Package ' + package + ' not found!'
    print(header + line)
    return
  

  packagesOrdered = sorted(packages, key=itemgetter('Version'), reverse=True)

  packageToInstall = packagesOrdered[0]
  
  packageNameVersion = str(package)
  if getString(packageToInstall['Version']) != '':
    packageNameVersion += '@' + str(getString(packageToInstall['Version']))
  
  if packageNameVersion in packageDependencyControlArray:
    print(header + ' Dependency satisfied!')
    return

  packageDependencyControlArray.append(packageNameVersion)
  

  depends = reasoner.execute('depends('+packageToInstall['Packageinstance']+',?order,?orderDisjuntion,?depAtom) and ?depAtom [package hasValue ?package, comparison hasValue ?comparison, version hasValue ?version] memberOf DependencyAtom')
  if (level == 0):
    print('─┬ ' + packageNameVersion)

  orderPrinted = None
  for dep in depends:
    if (orderPrinted != dep['Order']):
      changeHeader = header[0:-2]
      changeHeader += '└─'
      line = ' Dependency ' + str(dep['Order'] + 1)
      print(changeHeader + line)
    
    dependency = str(getString(dep['Package']))
    dependencyNameVersion = dependency
    if getString(dep['Comparison']).strip() != '' or getString(dep['Version']).strip() != '':
      dependencyNameVersion += '@'
    if getString(dep['Comparison']).strip() != '' and getString(dep['Version']).strip() != '':
      dependencyNameVersion += str(getString(dep['Comparison']))
    if getString(dep['Version']).strip() != '':
      dependencyNameVersion += str(getString(dep['Version']))
    
    line = ' ' + dependencyNameVersion
    
    print(header + line)
    
    if dependencyNameVersion in packageDependencyControlArray:
      print(header + ' Dependency satisfied!')
      return
    
    if allDependencys:
      dependencyOf(dependency, level + 1, header + ' │ ', True)

    orderPrinted = dep['Order']

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
  # print('| = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ')
  print('| Package => ' + package)
  print('| Version => ' + getString(packageToInstall['Version']))
  print('| Source => ' + getString(packageToInstall['Uri']))
  for data in packageProps:
    if data['Prop'] not in excludeProps:
        print('| '+ data['Prop'].capitalize() + ' => ' + getString(data['Value']))
  # print('| = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ')

elif args[0] == 'depends' and len(args) == 2:
  packageToDependency = args[1]
  dependencyOf(packageToDependency, 0, ' │ ', False)

elif args[0] == 'depends' and len(args) == 3 and args[2] == '--all':
  packageToDependency = args[1]
  dependencyOf(packageToDependency, 0, ' │ ', True)

else:
  print('* show [package]')
  print('* depends [package]')
  print('* depends [package] --all')
  exit()