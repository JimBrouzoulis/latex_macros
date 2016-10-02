import re
from latex_macros import replace_macros


def test_newcommand_re():

    # GIVEN a newcommand macro
    command = '\\newcommand{\sig}{\sigma}'

    # WHEN parsing using the re
    reg = replace_macros.newcommand_re

    # THEN 2 groups should be found
    m = reg.search(command)
    assert m.group(1) == r'\sig'
    assert m.group(2) == r'\sigma'


def test_macro_substitution():

    # GIVEN a macro command and a replacement command
    command = r'\sig'
    replacement = r'\sigma'

    # WHEN making a pattern and substituting in a string
    pattern = re.compile(r'%s' % re.escape(command))
    text = r'\sig'
    out = re.sub(pattern, replacement, text)

    # THEN we expect the replacement command as output
    assert out == r'\sigma'

