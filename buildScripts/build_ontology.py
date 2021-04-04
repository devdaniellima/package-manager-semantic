import subprocess, os, re
import package_utils as Utils

database = Utils.Database()
packagesName = []

print("Get all packages from sources list...")

print("Step 1/2 # Get package informations")
packageListInfo = open('./package_list_info.txt', 'r')
packagesCache = []
packageActual = None
sourceActual = None
linesTotal = 2150438
count = 0
for line in packageListInfo:
  count += 1
  lineStrip = line.strip()
  if (lineStrip == '@@@'):
    for package in packagesCache:
      package.source = sourceActual
      database.packages.append(package)
    packagesCache = []
    packageActual = None
    sourceActual = None
  if 'Package: ' == lineStrip[0:9]:
    packagesCache.append(Utils.Package())
    packagesCache[-1].name = lineStrip.replace('Package: ', '')
    #print('('+str(round(count*100/linesTotal, 2))+ '%)' + packagesCache[-1].name)
  if 'Priority: ' in lineStrip:
    packagesCache[-1].priority = lineStrip.replace('Priority: ', '')
  if 'Section: ' in lineStrip:
    packagesCache[-1].section = lineStrip.replace('Section: ', '')
  if 'Installed-Size: ' in lineStrip:
    packagesCache[-1].installedSize = lineStrip.replace('Installed-Size: ', '')
  if 'Maintainer: ' in lineStrip:
    packagesCache[-1].maintainer = lineStrip.replace('Maintainer: ', '')
  if 'Architecture: ' in lineStrip:
    packagesCache[-1].architecture = lineStrip.replace('Architecture: ', '')
  if 'Version: ' in lineStrip:
    packagesCache[-1].version = lineStrip.replace('Version: ', '')
    #print(' => ' + packagesCache[-1].version)
  if 'Replaces: ' in lineStrip:
    packagesCache[-1].replaces = lineStrip.replace('Replaces: ', '')
  if 'Provides: ' in lineStrip:
    packagesCache[-1].provides = lineStrip.replace('Provides: ', '')
  if 'Depends: ' in lineStrip:
    packagesCache[-1].depends = lineStrip.replace('Depends: ', '')
  if 'Conflicts: ' in lineStrip:
    packagesCache[-1].conflicts = lineStrip.replace('Conflicts: ', '')
  if 'Filename: ' in lineStrip:
    packagesCache[-1].fileName = lineStrip.replace('Filename: ', '')
  if 'Size: ' in lineStrip:
    packagesCache[-1].size = lineStrip.replace('Size: ', '')
  if 'MD5sum: ' in lineStrip:
    packagesCache[-1].md5sum = lineStrip.replace('MD5sum: ', '')
  if 'SHA1: ' in lineStrip:
    packagesCache[-1].sha1 = lineStrip.replace('SHA1: ', '')
  if 'SHA256: ' in lineStrip:
    packagesCache[-1].sha256 = lineStrip.replace('SHA256: ', '')
  if 'SHA512: ' in lineStrip:
    packagesCache[-1].sha512 = lineStrip.replace('SHA512: ', '')
  if 'Description: ' in lineStrip:
    packagesCache[-1].description = lineStrip.replace('Description: ', '')
  if 'Description-pt_BR: ' in lineStrip:
    packagesCache[-1].description = lineStrip.replace('Description-pt_BR: ', '')
  if 'Description-md5: ' in lineStrip:
    packagesCache[-1].descriptionMd5 = lineStrip.replace('Description-md5: ', '')
  if 'Description-md5: ' in lineStrip:
    packagesCache[-1].descriptionMd5 = lineStrip.replace('Description-md5: ', '')
  if 'Homepage: ' in lineStrip:
    packagesCache[-1].homepage = lineStrip.replace('Homepage: ', '')

  if 'APT-Sources: ' in lineStrip:
    sourceString = lineStrip.replace('APT-Sources: ', '')
    for sourceBlock in sourceString.split(' '):
      if 'http' in sourceBlock:
        sourceActual = database.getSource(sourceBlock)

#countTotalPackages = len(database.packages)

print("Step 2/2 # Create ontologys files")

#subprocess.run("rm -Rf ../Repository/Packages/*", shell=True)

countPackage = 0
countVersion = 0
countDependency = 0
for package in database.packages:
  countPackage += 1

  #if (countPackage == 10):
  #  exit()

  fileName = package.name
  filePath = '../Repository/Packages/'+fileName+'.wsml'

  if not os.path.exists(filePath):
    countVersion = 0
    countDependency = 0
    ontologyName = package.name.replace('-','_').replace('+','Plus').replace('.','Dot')

    fileOntology = open(filePath, 'a')

    fileOntology.write('// Variant\n')
    fileOntology.write('wsmlVariant _"http://www.wsmo.org/wsml/wsml-syntax/wsml-rule"\n\n')

    fileOntology.write('// Namespace\n')
    fileOntology.write('namespace {\n')
    fileOntology.write('\t_"br.com.devdaniellima/RepositoryOntology/Packages"\n')
    fileOntology.write('}\n\n')

    fileOntology.write('// Definition\n')
    fileOntology.write('ontology '+ ontologyName +'\n')
    fileOntology.write('\tnfp\n')
    fileOntology.write('\t\tdc#title hasValue "Repository Packages"\n')
    fileOntology.write('\t\tdc#contributor hasValue "Daniel Lima"\n')
    #fileOntology.write('\t\tdc#date hasValue _date(2021,03,21)\n')
    fileOntology.write('\t\tdc#format hasValue "text/plain"\n')
    fileOntology.write('\t\tdc#language hasValue "en-US" \n')
    fileOntology.write('\tendnfp\n\n')

    fileOntology.write('importsOntology {\n')
    fileOntology.write('\t_"../Repository.wsml"')
    if package.depends != '':
      for conjunction in package.depends.split(','):
        for disjunction in conjunction.split('|'):
          fileOntology.write(',\n')
          importName = disjunction.strip().split(' ')[0]
          fileOntology.write('\t_"' + importName + '.wsml"')

    fileOntology.write('\n}\n\n')

    if package.source is not None:
      fileOntology.write('// Sources instances\n\n')
      fileOntology.write("instance " + package.source.name + " memberOf Source\n")
      fileOntology.write('\turi hasValue "' + package.source.uri + '"\n')
    

    fileOntology.write('\n')

    fileOntology.write('// Packages instances\n')
    
  fileOntology.write('\n')

  instanceName = 'P' + str(countVersion) + '__' + package.name.replace('-','_').replace('+','Plus').replace('.','Dot')
  fileOntology.write("instance " + instanceName + ' memberOf Package\n')

  fileOntology.write('\tpackage hasValue "' + package.name + '"\n')
  
  if package.source is not None:
    fileOntology.write('\tpackageSource hasValue ' + package.source.name + '\n')

  if package.priority != '' :
    fileOntology.write('\tpriority hasValue "' + package.priority + '"\n')

  if package.section != '' :
    fileOntology.write('\tsection hasValue "' + package.section + '"\n')

  if package.installedSize != '' :
    fileOntology.write('\tinstalledSize hasValue "' + package.installedSize + '"\n')

  if package.maintainer != '' :
    fileOntology.write('\tmaintainer hasValue "' + package.maintainer.replace('"', '\\"') + '"\n')

  if package.architecture != '' :
    fileOntology.write('\tarchitecture hasValue "' + package.architecture + '"\n')

  if package.version != '' :
    fileOntology.write('\tversion hasValue "' + package.version + '"\n')

  if package.replaces != '' :
    fileOntology.write('\treplaces hasValue "' + package.replaces + '"\n')

  if package.provides != '' :
    fileOntology.write('\tprovides hasValue "' + package.provides.replace('"',"'") + '"\n')

  if package.conflicts != '' :
    fileOntology.write('\tconflicts hasValue "' + package.conflicts + '"\n')

  if package.fileName != '' :
    fileOntology.write('\tfileName hasValue "' + package.fileName + '"\n')

  if package.size != '' :
    fileOntology.write('\tsize hasValue "' + package.size + '"\n')

  if package.md5sum != '' :
    fileOntology.write('\tmd5sum hasValue "' + package.md5sum + '"\n')

  if package.sha1 != '' :
    fileOntology.write('\tsha1 hasValue "' + package.sha1 + '"\n')

  if package.sha256 != '' :
    fileOntology.write('\tsha256 hasValue "' + package.sha256 + '"\n')

  if package.sha512 != '' :
    fileOntology.write('\tsha512 hasValue "' + package.sha512 + '"\n')

  if package.description != '' :
    fileOntology.write('\tdescription hasValue "' + package.description.replace('"', '\\"') + '"\n')

  if package.descriptionMd5 != '' :
    fileOntology.write('\tdescriptionMd5 hasValue "' + package.descriptionMd5.replace('"', '\\"') + '"\n')

  if package.homepage != '' :
    fileOntology.write('\thomepage hasValue "' + package.homepage.replace('"', '\\"') + '"\n')

  if package.depends != '' :
    fileOntology.write('\tdepends hasValue "' + package.depends + '"\n\n')
    dependsArrString = package.depends.split(',')
    order = 0
    for dependString in dependsArrString:
      disjunctionArrString = dependString.split('|')
      for disjunction in disjunctionArrString:
        dependencyArr = disjunction.strip().split(' ')
        depPackage = dependencyArr[0]
        depComparison = ""
        depVersion = ""
        if (len(dependencyArr) > 1):
          depComparison = dependencyArr[1]
          if depComparison[0] == "(":
            depComparison = depComparison[1:]
        if (len(dependencyArr) > 2):
          depVersion = dependencyArr[2]
          if depVersion[-1] == ")":
            depVersion = depVersion[:-1]

        dependenceInstance = "DepAtom__" + str(countDependency)
        fileOntology.write("instance " + dependenceInstance + " memberOf DependencyAtom\n")
        fileOntology.write('\tpackage hasValue "' + depPackage + '"\n')
        fileOntology.write('\tcomparison hasValue "' + depComparison + '"\n')
        fileOntology.write('\tversion hasValue "' + depVersion + '"\n')
        fileOntology.write('\n')

        fileOntology.write("relationInstance depends("+ instanceName + "," + str(order) + "," + dependenceInstance + ")\n")
        fileOntology.write('\n')
      
        countDependency += 1

      order += 1
  
  countVersion += 1