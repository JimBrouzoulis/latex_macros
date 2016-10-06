import re
from collections import namedtuple
newcommand_re = re.compile(r"""
        ^\\newcommand           # starts with the newcommand
        {                       # followed by the macro definition within {}
          \s* (\S*?) \s*
        }
        \s*
        (\[ \s* (\d) \s* \])?   # number of arguments in the command
        \s*
        {                       # followed by the command definition within {}
          \s* ([\S\s]*?) \s*
        }
        \s*$
        """,
        re.VERBOSE
    )


NewCommand = namedtuple('new_command', ['macro', 'command', 'num_args'])

def parse_newcommand(raw_command):
    """ Tokenize the raw command
    '\newcommand{macro}[num_args]{command}' -> (macro, num_args, command)"""

    reg = newcommand_re
    m = reg.search(raw_command)
    if m:
        return NewCommand(macro=m.group(1), command=m.group(4).strip(), num_args=m.group(3))


def sub_newcommand(newc, text):
    """ Use this to simply substitute a macro when it does not depend on any arguments, e.g.
        '\newcommand{macro}{command}'
    """

    nc = parse_newcommand(newc)
    pattern = re.compile(r'%s' % re.escape(nc.macro))

    return re.sub(pattern, nc.command, text)


def generate_pattern(nc):
    """Generate regex pattern for the macro"""

    arg_pattern = r'\{\s*(\S*?)\s*\}' * int(nc.num_args)  # TODO should remove capturing of trailing spaces
    pattern = re.compile(r'%s%s' % (re.escape(nc.macro), arg_pattern))
    return pattern

def get_replacement_command(nc, match_obj):
    """ Return the command that should replace the matched macro in the text"""

    expanded_command = nc.command
    for arg in range(int(nc.num_args)):
        # replace the command argument with that found in the text

        expanded_command = re.sub(
            pattern=r'#{arg}'.format(arg=arg + 1),
            repl=re.escape(match_obj.group(arg + 1)),
            string=expanded_command
        )
    return expanded_command


def expand_macro(raw_command, text):
    """ Expand all the instances of a given macro used in a text"""

    nc = parse_newcommand(raw_command)
    pattern = generate_pattern(nc)  # the pattern to search for in the text
    matches = pattern.finditer(text)
    for m in matches:  # for each use of the macro
        expanded_command = get_replacement_command(nc, m)
        text = text.replace(m.group(), expanded_command)

    return text
