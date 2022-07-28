#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from .. import translate


@pytest.mark.parametrize(
    'user_input,expected', [
        # Just translation file given.
        (['translate.py', 'source.docx'], (True, 'source.docx', None)),
        # Translation file and glossary file given.
        (['translate.py', 'source.docx', 'glossary.txt'], (True, 'source.docx', 'glossary.txt')),
        # No files given.
        (['translate.py'], (False, None, None)),
        # Too many args.
        (['translate.py', 'source.docx', 'glossary.txt', 'random.pdf'], (False, None, None)),
        # Incorrect translation file type.
        (['translate.py', 'source.doc'], (False, None, None)),
        # Incorrect glossary file type.
        (['translate.py', 'source.docx', 'glossary.docx'], (False, None, None)),
        # Just glossary file given.
        (['translate.py', 'glossary.txt'], (False, None, None)),
    ]
)
def test_user_input_check(user_input, expected):
    assert translate.check_user_input(user_input) == expected
