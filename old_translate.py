#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Uses the DeepL API to translate a single document in one go.
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


def translate_document(translation_file, glossary_file):
    """
    Translates user specified document using the DeepL API.
    """

    auth_key = get_auth_key()
    translator = deepl.Translator(auth_key)
    output_path = "small-PCT-EN.docx"  # Better to build new filename from source file

    try:
        translator.translate_document_from_filepath(
            translation_file,
            output_path,
            source_lang="JA",
            target_lang="en-US",
        )

        print("\nDocument translation downloaded.")
        usage = translator.get_usage()
        print(str(usage) + "\n")

    except deepl.DocumentTranslationException as error:
        # If an error occurs during document translation after the document was
        # already uploaded, a DocumentTranslationException is raised. The
        # document_handle property contains the document handle that may be used to
        # later retrieve the document from the server, or contact DeepL support.
        doc_id = error.document_handle.id
        doc_key = error.document_handle.key
        print("Error after upload.")
        print(error)
        print("ID: " + doc_id)
        print("Key: " + doc_key)

    except deepl.DeepLException as error:
        # Errors during upload raise a DeepLException
        print("Error during upload.")
        print(error)


def get_auth_key():
    """
    Gets the DeepL auth key from env file.
    """
    env = Env()
    env.read_env()
    auth_key = env.str("AUTH_KEY")
    return auth_key


if __name__ == "__main__":

    valid, translation_file, glossary_file = check_user_input(sys.argv)

    if valid:
        translate_document(translation_file, glossary_file)
