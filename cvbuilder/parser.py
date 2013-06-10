import os.path
import yaml
from pybtex.database.input import bibtex, BaseParser



class YamlParser(BaseParser):
    suffixes = ['.yaml', '.yml']

    def parse_stream(self, stream):
        """Returns a python object (scalar, list or dictionary) with the contents
        of the YAML input file"""
        self.data = yaml.load(stream, Loader=Loader)
        return self.data



class BibtexParser(bibtex.Parser):
    suffixes = ['.bib']

    def parse_file(self, filename):
        """Returns a list of bibliography entries"""
        super(BibtexParser, self).parse_file(filename)
        return self.data.entries.values()  



class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)
    
    def include(self, node):
        if   isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            filenames = self.construct_sequence(node)
            if not self.sameExtension(filenames):
                raise yaml.constructor.ConstructorError("!include sequence must be of same type")
            else:
                result = []
                for f in filenames:
                    result += self.extractFile(f)
                return result

        elif isinstance(node, yaml.MappingNode):
            extensions = [getExtension(x) for x in self.construct_mapping(node).values()]
            if any(x in extensions for x in BibtexParser.suffixes):
                raise yaml.constructor.ConstructorError("!include mapping may not contain BibTeX files")
            else:
                result = {k: self.extractFile(v) for (k, v) in self.construct_mapping(node).iteritems()}
                return result

    def extractFile(self, filename):
        filepath = os.path.join(self._root, filename)
        extension = getExtension(filename)

        for parser in [ YamlParser(), BibtexParser() ]:
            if extension in parser.suffixes:
                return parser.parse_file(filepath)
        else:
            raise yaml.constructor.ConstructorError("Unrecognised file type in !include statement: " + filename)

    def sameExtension(self, filenames):
        extensions = [getExtension(x) for x in filenames]
        for parser in [ YamlParser, BibtexParser ]:
            if all(x in parser.suffixes for x in extensions):
                return True
        else:
            return False



def getExtension(filename):
    return os.path.splitext(filename)[1]

