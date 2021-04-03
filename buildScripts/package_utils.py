# For the build moment
class Source:
  def __init__(self, uri, name):
    self.memberOf = 'Source'
    self.uri = uri
    self.name = name

class Package:
  def __init__(self):
    self.memberOf = 'Package'
    self.name = ''
    self.priority = ''
    self.section = ''
    self.installedSize = ''
    self.maintainer = ''
    self.architecture = ''
    self.version = ''
    self.replaces = ''
    self.provides = ''
    self.depends = ''
    self.conflicts = ''
    self.fileName = ''
    self.size = ''
    self.md5sum = ''
    self.sha1 = ''
    self.sha256 = ''
    self.sha512 = ''
    self.description = ''
    self.descriptionMd5 = ''
    self.homepage = ''
    self.source = ''

class Dependency:
  def __init__(self, packageOrigin, package, comparison, version, order):
    self.packageOrigin = packageOrigin
    self.package = package
    self.comparison = comparison
    self.version = version
    self.order = order

class Database:
  def __init__(self):
    self.sources = []
    self.packages = []
    self.dependencyAtoms = []
    self.depends = []
    self.sourceNextId = 0
    self.packageNextId = 0
  
  def getSource(self, uri):
    for source in self.sources:
      if (source.uri == uri):
        return source

    source = Source(uri, 'Source__S' + str(len(self.sources) + 1))
    self.sources.append(source)
    return source
