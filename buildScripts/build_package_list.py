import subprocess

packagesName = []

subprocess.run("apt-cache search '' > temp.txt", shell=True)
f = open('temp.txt', 'r')
for line in f:
  packagesName.append(line.strip().split(' ')[0])
f.close()

print(str(len(packagesName)) + ' packages.')

packageListFile = open('package_list.txt', 'w')
for packageName in packagesName:
  packageListFile.write(packageName + '\n')

packageListFile.close()

subprocess.run("rm temp.txt", shell=True)