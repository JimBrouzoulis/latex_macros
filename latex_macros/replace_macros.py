import re
from collections import namedtuple
newcommand_re = re.compile(r"""
        ^\\newcommand       # starts with the newcommand
        {                   # followed by the macro definition within {}
          \s* (\S*?) \s*
        }
        \s*
        (\[ \s* (\d) \s* \])?
        \s*
        {                   # followed by the command definition within {}
          \s* ([\S\s]*?) \s*
        }""",
        re.VERBOSE
    )


NewCommand = namedtuple('new_command', ['macro', 'command', 'num_args'])

def parse_newcommand(raw_command):
    """ Tokenize the raw command
    '\newcommand{macro}[num_args]{command}' -> (macro, num_args, command)"""

    reg = newcommand_re
    m = reg.search(raw_command)
    if m:
        return NewCommand(macro=m.group(1), command=m.group(4), num_args=m.group(3))


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


def expand_macro(raw_command, text):

    nc = parse_newcommand(raw_command)
    command = nc.command
    pattern = generate_pattern(nc)

    matches = pattern.finditer(text)
    for m in matches:
        patterns = [(r'#{arg}'.format(arg=i), re.escape(m.group(i))) for i in range(1, int(nc.num_args)+1)]

        for p in patterns:
            command = command.replace(*p)
            text = text.replace(m.group(), command)

    return text
