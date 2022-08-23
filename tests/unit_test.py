#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import Mock

from .. import translate
from .. translate import Segment

import pytest
import deepl
from environs import Env


# Need to use absolute paths in some of the below tests. Specifically,
# those tests using Document and Env. Therefore need the full path to this
# 'unit_test.py' file to build those absolute paths.
BASE_DIR = current_dir = os.path.dirname(os.path.realpath(__file__))


class MockDeeplGlossary():
    def __init__(self, glossary_name, source_lang, target_lang, entries):
        self.usage = Mock()
        self.glossary_name = glossary_name
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.entries = entries

    @property
    def name(self):
        return self.glossary_name

    @property
    def source_lang(self):
        return self.source_lang

    @property
    def target_lang(self):
        return self.target_lang

    @property
    def entry_count(self):
        return self.entries


@pytest.fixture
def mock_deepl_glossary():
    return MockDeeplGlossary()


class MockDeeplTranslator:
    def __init__(self):
        self.usage = Mock()
        self.usage.character.count = 300000

    def get_usage(self):
        return self.usage

    def translate_text(self, source_text, source_lang, target_lang):
        return "mock_target_string"

    def create_glossary(self, glossary_name, source_lang, target_lang, entries):
        return MockDeeplGlossary(glossary_name, source_lang, target_lang, entries)


@pytest.fixture
def mock_deepl_translator():
    return MockDeeplTranslator()


@pytest.fixture
def mock_glossary_file():
    return "coding/python/kikai_to_tmx/tests/docs/test-glossary-file.docx"


@pytest.fixture
def mock_glossary_entries():
    entries = {
        "明細書": "Description",
        "発明の名称": "Title of the invention",
        "情報処理装置": "information processing device",
        "技術分野": "Technical Field",
        "に関する": "relates to",
        "近年": "in recent years",
        "ＡＲ技術": "AR technology",
        "特許文献": "Patent Documents",
        "発明の概要": "Summary of the Invention",
        "発明が解決しようとする課題": "Problem to be Solved by the Invention",
        "表示部": "display unit",
        "制御部": "control unit",
    }
    return entries


@pytest.fixture
def segment_object():
    segment = Segment(
        source_text="正孔輸送層12は、無機材料を含んでいてもよい。",
        target_text="The positive hole transport layers 12 may include an inorganic material.",
    )
    return segment


@pytest.fixture
def list_of_segment_objects():
    segments = []
    for i in range(10):
        segment = Segment(
            source_text="正孔輸送層12は、無機材料を含む。",
            target_text="",
        )
        segments.append(segment)
    return segments


@pytest.fixture
def list_of_segment_objects_from_file():
    test_file_path = "docs/test-source-text.docx"
    full_file_path = BASE_DIR + "/" + test_file_path
    segments = translate.get_source_segments(full_file_path)
    return segments


def test_segment_constructor(segment_object):
    assert isinstance(segment_object, Segment)


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


def test_segment_object_source_text(segment_object):
    assert segment_object.source_text == "正孔輸送層12は、無機材料を含んでいてもよい。"


def test_segment_object_target_text(segment_object):
    assert segment_object.target_text == "The positive hole transport layers 12 may include an inorganic material."


def test_setup_deepl_translator_constructor():
    output = translate.setup_deepl_translator()
    assert isinstance(output, deepl.Translator)


def test_setup_deepl_auth_key_retrieval_from_env_file():
    test_file_path = "docs/.env.test"
    full_file_path = BASE_DIR + "/" + test_file_path
    expected = "lskdjf84u9f8oroifjoidjfo8u8eu98ufoidjiof8u984u"
    env = Env()
    env.read_env(full_file_path, recurse=False)
    assert env("KEY") == expected


def test_get_source_segments(list_of_segment_objects_from_file):
    expected = [
        "明細書",
        "発明の名称 : 情報処理装置、情報処理方法及びプログラム",
        "技術分野",
        "[0001]",
        "本技術は、自己位置を推定する情報処理装置等の技術に関する。",
        "背景技術",
        "[0002]",
        "近年、視覚を通じて仮想空間に存在するように知覚させるＶＲ（Virtual Reality）技術や、現実世界における実物体に仮想オブジェクトを重畳表示するＡＲ（Augmented Reality）技術が広く知られるようになってきている。",
        "ＶＲ技術、ＡＲ技術は、例えば、ヘッドマウントディスプレイや、スマートフォン等の各種の情報処理装置に搭載されている。",
        "[0003]",
        "ＡＲ技術や、ＶＲ技術においては、情報処理装置における自己位置を正確に推定する必要がある（例えば、下記特許文献１参照）。",
        "先行技術文献",
        "特許文献",
        "[0004]",
        "特許文献1 : 特開２０１７－０７２５６０号公報",
        "発明の概要",
        "発明が解決しようとする課題",
        "[0005]",
        "しかしながら、情報処理装置（ヘッドマウントディスプレイ等）を付帯するユーザが、車、電車等の乗り物に乗っているような特定の状況下にある場合、自己位置の推定の精度が低下してしまうといった問題がある。",
        "[0034]",
        "表示部３は、シースルータイプの表示部であり、グラス部１５の表面に設けられている。",
        "表示部３は、制御部１の制御に応じて、仮想オブジェクト２０（図１０参照）を表示することで、グラス部１５を介してユーザが見ている実空間上に仮想オブジェクト２０が配置されているようにユーザに認識させる。",
        "なお、表示部３は、非シースルータイプの表示部であってもよい。",
        "この場合、撮像部４により撮像された画像が表示部３上に表示される。",
    ]
    output = [seg_obj.source_text for seg_obj in list_of_segment_objects_from_file]
    assert output == expected


def test_get_source_char_count(list_of_segment_objects_from_file):
    output = translate.get_source_char_count(list_of_segment_objects_from_file)
    expected_char_count = 686
    assert output == expected_char_count


def test_check_deepl_usage_success(mock_deepl_translator):
    source_char_count = 500
    output = translate.check_deepl_usage(source_char_count, mock_deepl_translator)
    assert output is True


def test_check_deepl_usage_fail(mock_deepl_translator):
    source_char_count = 200000
    output = translate.check_deepl_usage(source_char_count, mock_deepl_translator)
    assert output is False


def test_translate_segments(mock_deepl_translator, list_of_segment_objects):
    segments = translate.translate_segments(mock_deepl_translator, list_of_segment_objects, None)
    for segment in segments:
        assert segment.target_text == "mock_target_string"


def test_extract_glossary_entries_success():
    expected = {
        "明細書": "Description",
        "発明の名称": "Title of the invention",
        "情報処理装置": "information processing device",
        "技術分野": "Technical Field",
        "に関する": "relates to",
        "近年": "in recent years",
        "ＡＲ技術": "AR technology",
        "特許文献": "Patent Documents",
        "発明の概要": "Summary of the Invention",
        "発明が解決しようとする課題": "Problem to be Solved by the Invention",
        "表示部": "display unit",
        "制御部": "control unit",
    }
    test_file_path = "docs/test-glossary-1.txt"
    full_file_path = BASE_DIR + "/" + test_file_path
    output = translate.extract_glossary_entries(full_file_path)
    assert output == expected


def test_extract_glossary_entries_fail_1():
    # Test SystemExit is raised when attempting to read non-existent glossary file.
    with pytest.raises(SystemExit):
        test_file_path = "docs/test-glossary.txt"
        full_file_path = BASE_DIR + "/" + test_file_path
        translate.extract_glossary_entries(full_file_path)


def test_extract_glossary_entries_fail_2():
    # Test improperly formatted glossary lines are ignored
    expected = {"特許文献": "Patent Documents"}
    test_file_path = "docs/test-glossary-3.txt"
    full_file_path = BASE_DIR + "/" + test_file_path
    output = translate.extract_glossary_entries(full_file_path)
    assert output == expected


def test_extract_glossary_entries_fail_3():
    # Test SystemExit is raised when nothing has been read from the user glossary file.
    with pytest.raises(SystemExit):
        test_file_path = "docs/test-glossary-4.txt"
        full_file_path = BASE_DIR + "/" + test_file_path
        translate.extract_glossary_entries(full_file_path)


def test_create_deepl_glossary_success():
    pass


def test_build_glossary_name():
    pass


def test_output_deepl_usage():
    pass
