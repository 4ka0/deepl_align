#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

from .. import translate
from .. translate import Segment


def test_constructor():
    '''
    Test instantiation
    '''
    s = Segment('なお、正孔輸送層12は、NiO、（またはMoO3）等の無機材料を'
                '含んでいてもよい。',
                'moreover, the positive  hole transport layers 12 may '
                'include an inorganic material such as NiO (or MoO3].',
                '', '', [], [], False, {}, {}, False, False, False, False,
                False, False, [], False, [], False, False, [])
    assert isinstance(s, Segment)


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


def test_get_source_segments():

    # Need to give Document the absolute path to the test docx file.
    # Therefore need the full path to this 'unit_test.py' file.
    # Then need to add the location of the test docx file to the path.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_file_path = "source_docs/small-PCT-JP.docx"
    full_file_path = current_dir + "/" + test_file_path

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
    output = translate.get_source_segments(full_file_path)

    assert output == expected
