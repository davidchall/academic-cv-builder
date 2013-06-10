#!/usr/bin/env python

import os
from cvbuilder import environment, cmdline
from cvbuilder.parser import YamlParser
from yaml.constructor import ConstructorError

if __name__ == '__main__':
    options = cmdline.get_cmd_line_args()

    parser = YamlParser()
    try:
        cv_data       = parser.parse_file(options.input)
        template_data = parser.parse_file(options.template)
    except ConstructorError:
        raise

    env = environment.get_jinja_env(template_data)
    template = env.get_template(template_data["file"])

    outfile = open(options.output + ".tex", 'w')
    outfile.write(template.render(cv_data).encode('utf8'))
    outfile.close()

    command = template_data["language"] + " -interaction=batchmode -output-directory=output " + options.output + ".tex"
    os.system(command)

