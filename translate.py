#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
x create sample translation file
x create github repository
x check user input
- get text from document to translate
- split text into segments
- get translation for each segment from deepl, one by one
- save as list of segments, each segment containing source and target strings
- build tmx file from list of segment pairs
'''

import sys
import deepl
from environs import Env


def check_user_input(user_input):
    """
    Checks user input.
    Returns - True/False regarding whether user input is valid/invalid.
            - The file to be translated.
            - A glossary file if given.
    """

    format_message = (
        "Expected input: python3 translate.py translation.docx glossary.txt\n"
        "(glossary.txt is optional)\n"
    )

    # Should be 2 or 3 args
    if len(user_input) < 2 or len(user_input) > 3:
        print("\nError: Incorrect number of arguments.")
        print(format_message)
        return False, None, None

    # 2nd arg should be a docx file
    translation_file = user_input[1]
    if not translation_file.lower().endswith('.docx'):
        print("\nError: Second argument should be a docx file.")
        print(format_message)
        return False, None, None

    # 3rd arg, if present, should be a txt file
    if len(user_input) == 3:
        glossary_file = user_input[2]
        if not glossary_file.lower().endswith('.txt'):
            print("\nError: Third argument should be a txt file.")
            print(format_message)
            return False, None, None
    else:
        glossary_file = None

    return True, translation_file, glossary_file


if __name__ == "__main__":

    valid, translation_file, glossary_file = check_user_input(sys.argv)

    if valid:

        # Get DeepL auth key from env file.
        env = Env()
        env.read_env()
        auth_key = env.str("AUTH_KEY")

        translator = deepl.Translator(auth_key)

        source_text = "情報処理装置"
        source_lang = "JA"
        target_lang = "en-US"

        result = translator.translate_text(
            source_text,
            source_lang=source_lang,
            target_lang=target_lang
        )

        print("\nEngine output: ")
        print(result.text + "\n")

        usage = translator.get_usage()

        print(str(usage) + "\n")
