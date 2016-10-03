import re

newcommand_re = re.compile(r"""
        ^\\newcommand       # starts with the newcommand
        {                   # followed by the macro definition within {}
          \s* (\S*?) \s*
        }
        {                   # followed by the command definition within {}
          \s* (\S*?) \s*
        }""",
        re.VERBOSE
    )


def parse_newcommand(exp):

    reg = newcommand_re

    m = reg.search(exp)
    if m:
        macro = m.group(1)
        command = m.group(2)
        return macro, command



def sub_newcommand(newc, text):

    macro, command = parse_newcommand(newc)
    pattern = re.compile(r'%s' % re.escape(macro))

    return re.sub(pattern, command, text)

