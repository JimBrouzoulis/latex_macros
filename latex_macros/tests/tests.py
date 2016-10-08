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
    assert m.group(4) == r'\sigma'

    (macro, command, _) = replace_macros.parse_newcommand(newc)
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


def test_arg_sub():

    nc = '\\newcommand{\\mupp}[3]{#1 #2 #3#3}'

    macro, command, num_args = replace_macros.parse_newcommand(nc)

    # WHEN making a pattern and substituting in a string
    #re_string = r'%s' % re.escape(macro) + r'{}'

    arg_pattern = r'\{\s*(\S*?)\s*\}\s*'*int(num_args)

    pattern = re.compile(r'%s%s' % (re.escape(macro), arg_pattern))
    print(arg_pattern)
    print(pattern)

    #text = '\\mupp{ a  }{b }{  \\alpha}'
    text = r'\mupp{ a  }{b }{  \alpha}'

    m = pattern.match(text)
    assert m.group(1) == r'a'
    assert m.group(2) == r'b'
    assert m.group(3) == r'\alpha'

    patterns = [(r'#%s' % i, re.escape(m.group(i))) for i in range(1, int(num_args)+1)]
    print('patterns: {p}'.format(p=patterns))
    print('pattern: {p}'.format(p=pattern))

    print('command before: {c}'.format(c=command))
    for p in patterns:
        command = command.replace(p[0], p[1])

    print('command after: {c}'.format(c=command))
    print('sample text: {t}'.format(t=text))

    out = re.sub(pattern, command, text)

    print('out: {o}'.format(o=out))
    assert out == r'a b \alpha\alpha'




def test_single_arg():

    # GIVEN a new command
    nc = '\\newcommand{\\mean}[1]{\\bar #1 }'

    # WHEN expanding the macro
    text = r'\mean{a} word \mean{\alpha}'
    out = replace_macros.expand_macro(nc, text)

    # THEN we expect
    assert out == r'\bar a word \bar \alpha'


def test_single_arg_duplicate_macro():

    # GIVEN a new command
    nc = r'\newcommand{\mean}[1]{\bar{ #1 } }'

    # WHEN expanding the macro
    text = r'\mean{a} word \mean{\alpha}'
    out = replace_macros.expand_macro(nc, text)

    # THEN we expect
    assert out == r'\bar{ a } word \bar{ \alpha }'



def test_two_args():

    # GIVEN a newcommand
    nc = '\\newcommand{\\my_macro}[2]{\\foo{#1} \\bar{#2} }'

    # WHEN expanding the macro
    text = r'\my_macro{a}{b}'
    out = replace_macros.expand_macro(nc, text)

    # THEN we expect
    assert out == r'\foo{a} \bar{b}'



def test_two_commands():

    # GIVEN two newcommands
    commands = [
        '\\newcommand{\\my_macro_1}{\\foo}',
        '\\newcommand{\\my_macro_2}[1]{\\bar{#1}}'
    ]

    # WHEN expanding the macros
    text = r'\my_macro_1 some text \my_macro_2{a}'
    text = replace_macros.expand_macros(commands, text)

    # THEN we expect
    assert text == r'\foo some text \bar{a}'


def test_nested_commands():

    # GIVEN two dependent newcommands
    commands = [
        '\\newcommand{\\macro1}{\\foo}',
        '\\newcommand{\\macro2}{\\macro1 \\bar}',
    ]
    # WHEN expanding the macros
    text = r'\macro1 \macro2'
    text = replace_macros.expand_macros(commands, text)

    # THEN we expect
    assert text == r'\foo \foo \bar'


def test_read_commands():

    # GIVEN a text containing definitions of new commands
    command_text = """
        \\newcommand{\\macro1}{\\foo}
        \\newcommand{\\macro2}{\\macro1 \\bar}
        # a python comment that will be ignored
        % a tex comment that will be ignored
        \\newcommand{\\macro3}{\\macro1 \\macro2}
    """

    re_comment = re.compile(r'\s*\#|\%.*')
    re_newcommand = re.compile(r'\s*(\\newcommand.*)\s*')
    commands = []
    for line in command_text.splitlines():
        if not re_comment.match(line):
            m = re_newcommand.match(line)
            if m:
                commands.append(m.group(1))

    print(commands)
    assert len(commands) == 3
    assert commands[0] == '\\newcommand{\\macro1}{\\foo}'
    assert commands[1] == '\\newcommand{\\macro2}{\\macro1 \\bar}'
    assert commands[2] == '\\newcommand{\\macro3}{\\macro1 \\macro2}'







