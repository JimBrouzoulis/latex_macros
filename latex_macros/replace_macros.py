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