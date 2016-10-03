import re
from latex_macros import replace_macros


def test_newcommand_re():

    # GIVEN a newcommand macro
    newc = '\\newcommand{\sig}{\sigma}'

    # WHEN parsing using the re
    reg = replace_macros.newcommand_re

    # THEN 2 groups should be found
    m = reg.search(newc)
    assert m.group(1) == r'\sig'
    assert m.group(2) == r'\sigma'

    macro, command = replace_macros.parse_newcommand(newc)
    assert macro == r'\sig'
    assert command == r'\sigma'

def test_macro_substitution():

    # GIVEN a macro command and a replacement command
    macro = r'\sig'
    replacement = r'\sigma'

    # WHEN making a pattern and substituting in a string
    pattern = re.compile(r'%s' % re.escape(macro))
    text = r'\sig'
    out = re.sub(pattern, replacement, text)

    # THEN we expect the replacement command as output
    assert out == r'\sigma'


def test_single_sub():

    newc = '\\newcommand{\sig}{\sigma}'
    text = r'\sig'
    out = replace_macros.sub_newcommand(newc, text)
    assert out == r'\sigma'

    text = r'An inline expression $\sig$.'
    out = replace_macros.sub_newcommand(newc, text)
    assert out == r'An inline expression $\sigma$.'


def test_multiple_sub():
    newc = '\\newcommand{\stuff}{\word}'

    text = r'\stuff and some math $\stuff$ $\stuff$.'
    out = replace_macros.sub_newcommand(newc, text)
    assert out == r'\word and some math $\word$ $\word$.'




