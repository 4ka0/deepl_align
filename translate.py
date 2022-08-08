#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
x create sample translation file
x create github repository
x check user input
x get text from document to translate
- split text into segments
- get translation for each segment from deepl, one by one
- save as list of segments, each segment containing source and target strings
- build tmx file from list of segment pairs
'''

import sys
import deepl
from docx import Document
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
        "(glossary.txt is optional.)\n"
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


def get_source_segments(source_file):
    """
    Reads in text from user-specified docx file.
    File is already split into paragraphs by Document module.
    Text is further split into sentences if a paragraph contains multiple sentences.
    """

    document = Document(source_file)
    source_segments = []  # A list of strings, each representing a segment of source text.

    for para in document.paragraphs:
        # Split again if paragraph contains multiple sentences.
        if para.text.count("。") >= 2:
            sentences = para.text.split("。")
            for sentence in sentences:
                # Add each single sentence to source_segments list.
                # However, if "。" appears at the end of a string, split() creates an empty string
                # representing the substring that follows "。". Using "if sentence" skips such
                # empty strings. Also, split() removes the "。" delim, so have to add this back on.
                if sentence:
                    source_segments.append(sentence + "。")
        else:
            source_segments.append(para.text)

    return source_segments


def translate_segments(source_segments, glossary_file):

    # Get the DeepL auth key from env file
    env = Env()
    env.read_env()
    auth_key = env.str("AUTH_KEY")

    # Get translation from DeepL
    translator = deepl.Translator(auth_key)

    for segment in source_segments:
        print("\n" + segment)
        result = translator.translate_text(segment, source_lang="JA", target_lang="en-US",)
        print(result.text)

    usage = translator.get_usage()
    print("\n" + str(usage) + "\n")


if __name__ == "__main__":

    valid, source_file, glossary_file = check_user_input(sys.argv)

    if valid:

        source_segments = get_source_segments(source_file)

        target_segments = translate_segments(source_segments, glossary_file)
