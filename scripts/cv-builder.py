#!/usr/bin/env python

import yaml
import os
from cvbuilder import environment, cmdline
from cvbuilder.Loader import Loader

if __name__ == '__main__':
    options = cmdline.get_cmd_line_args()

    try:
        cv_data       = yaml.load(open(options.input,    'r'), Loader=Loader)
        template_data = yaml.load(open(options.template, 'r'), Loader=Loader)
    except yaml.constructor.ConstructorError:
        raise

    env = environment.get_jinja_env(template_data)
    template = env.get_template(template_data["file"])

    outfile = open(options.output + ".tex", 'w')
    outfile.write(template.render(cv_data).encode('utf8'))
    outfile.close()

    command = template_data["language"] + " -interaction=batchmode -output-directory=output " + options.output + ".tex"
    os.system(command)

