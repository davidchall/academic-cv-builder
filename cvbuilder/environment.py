from jinja2 import Environment, PackageLoader
from pybtex.style.formatting.unsrt import Style
from pybtex.backends import latex, html
import re

def get_jinja_env(template_data):
    env = Environment(loader=PackageLoader('cvbuilder', 'templates'))

    # Change start/end strings if necessary
    # For TEX templates, this is _always_ necessary
    if "strings" in template_data or "tex" in template_data["language"]:
        try:
            strings = template_data["strings"]
        except KeyError:
            print "\nWarning: Start/end strings are necessary in TEX templates"
            exit()

        if "variable_start" in strings:
            env.variable_start_string = strings["variable_start"]
        elif "variable_begin" in strings:
            env.variable_start_string = strings["variable_begin"]
        if "variable_end"   in strings:
            env.variable_end_string   = strings["variable_end"]

        if "block_start" in strings:
            env.block_start_string = strings["block_start"]
        elif "block_begin" in strings:
            env.block_start_string = strings["block_begin"]
        if "block_end"   in strings:
            env.block_end_string   = strings["block_end"]

        if "comment_start" in strings:
            env.comment_start_string = strings["comment_start"]
        elif "comment_begin" in strings:
            env.comment_start_string = strings["comment_begin"]
        if "comment_end"   in strings:
            env.comment_end_string   = strings["comment_end"]

    if "html" in template_data["language"]:
        env.autoescape = True

    env.filters['datetimeformat'] = datetimeformat
    env.filters['escape_tex']     = escape_tex
    env.filters['bibtex']         = bibtex

    return env

def datetimeformat(value, format='%b %Y'):
    return value if value == "Present" else value.strftime(format)

def escape_tex(value):
    result = value
    for pattern, replacement in LATEX_SUBS:
        result = pattern.sub(replacement, result)
    return result

def bibtex(value, format):
    if format == "latex":
        result = []
        for ref in Style().format_entries(value):
            result.append(ref.text.render(latex.Backend()))
        return result
    elif format == "html":
        print "test"
        for ref in Style().format_entries(value):
            print ref.text.render(html.Backend())
    else:
        raise Exception("Unrecognised output format given to bibtex filter")

LATEX_SUBS = (
    (re.compile(r'\\'),            r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'),   r'\\\1'),
    (re.compile(r'~'),             r'\~{}'),
    (re.compile(r'\^'),            r'\^{}'),
    (re.compile(r'"'),             r"''"),
    (re.compile(r'\.\.\.+'),       r'\\ldots'),
    (re.compile(r'LaTeX'),         r'\LaTeX'),
    (re.compile(r'\[([^\]]*)\]\(([^)]*)\)'), r'\href{\2}{\1}'),
)

