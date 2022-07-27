#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from .. import translate


@pytest.mark.parametrize(
    'user_input,expected', [
        # Just translation file given.
        (['translate.py', 'source.docx'], True),
        # Translation file and glossary file given.
        (['translate.py', 'source.docx', 'glossary.txt'], True),
        # No files given.
        (['translate.py'], False),
        # Too many args.
        (['translate.py', 'source.docx', 'glossary.txt', 'random.pdf'], False),
        # Incorrect translation file type.
        (['translate.py', 'source.doc'], False),
        # Just glossary file given.
        (['translate.py', 'glossary.txt'], False),
    ]
)
def test_user_input_check(user_input, expected):
    assert translate.check_user_input(user_input) == expected
