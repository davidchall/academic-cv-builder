from optparse import OptionParser

def get_cmd_line_args():
    desc = """cv-writer turns your personal information stored in a YAML file into a CV, 
    according to a template of your choice."""

    parser = OptionParser(version='%prog version 1.0',
                          description=desc)

    parser.add_option('-i', "--input", 
                      dest="input", default="data/cv.yaml",
                      help="YAML file containing CV data")

    parser.add_option('-o', "--output",
                      dest="output", default="cv",
                      help="Output file")

    parser.add_option('-t', "--template",
                      dest="template", default="/Users/David/Documents/code/academic-cv-builder/templates/stylish.yaml",
                      help="YAML file containing template data")

    (opts, args) = parser.parse_args()

    return opts
