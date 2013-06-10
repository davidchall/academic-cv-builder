#!/usr/bin/env python

import os
import yaml
from pybtex.database.input import bibtex

class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)
        Loader.add_constructor('!import',  Loader.include)
    
    def include(self, node):
        if   isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result += self.extractFile(filename)
            return result

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k,v in self.construct_mapping(node).iteritems():
                result[k] = self.extractFile(v)
            return result

        else:
            raise yaml.constructor.ConstructorError("Unrecognised YAML node type in !include statement")

    def extractFile(self, filename):
        filepath = os.path.join(self._root, filename)
        fileExtension = os.path.splitext(filename)[1]

        if   fileExtension in ( ".yaml", ".yml" ):
            return yaml.load(open(filepath, 'r'), Loader)

        elif fileExtension in ( ".bib" ):
            parser = bibtex.Parser()
            return parser.parse_file(filepath).entries.values()

        else:
            raise yaml.constructor.ConstructorError("Unrecognised file type in !include statement")
