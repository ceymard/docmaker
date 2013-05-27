
import re
import os.path

# Format is (open, close)
MULTI_COMMENTS = dict(
    python = (
        ('"""!', '"""'),
        ("'''!", "'''")
    ),
    javascript = ('/**', '*/'),
    cpp = ('/**', '*/'),
    caml = ('(**', '*)')
)

SINGLE_COMMENTS = dict(
    python = '##',
    javascript = '//!',
    cpp = '//!'
)

COMMENTS_RE = dict()

for language, tokens in MULTI_COMMENTS.iteritems():
    if not language in COMMENTS_RE:
        COMMENTS_RE[language] = []

    begin, end = tokens
    COMMENTS_RE[language].append('{0}(?P<content>(?!{1}).)*{1}'.format(begin, end))

for language, starter in SINGLE_COMMENTS.iteritems():
    if not language in COMMENTS_RE:
        COMMENTS_RE[language] = []

    COMMENTS_RE[language].append('{0}\s*(?P<content>.*?)\s*\n'.format(starter))

for language, re_list in COMMENTS_RE:
    COMMENTS_RE[language] = re.compile('|'.join(map(lambda e: re.escape(e), re_list)))

def parse(contents, language):
    '''!
        Arguments:
            file_contents|str: A string
        Returns|Dict:
            The parsed contents of the file
    '''

    comments_re = re.compile(comment)