#!/usr/bin/env fontforge -lang=py -script
# -*- coding: utf-8 -*-
#
# 使い方: fontforge -lang=py -script mejiro.py [1|2|3|all ...]
# 引数を省略すると M+ 1 版 (McMejiro) のみを生成する

import sys
import fontforge
import psMat
from datetime import date

# Roboto のあるディレクトリのパス
roboto_path = "./roboto"

# M+ のあるディレクトリのパス
mplus_path = "./mplus"

# Mejiro を生成するディレクトリのパス
# 同じディレクトリに一時ファイルも生成される
mejiro_path = "./mejiro"

# 元にする M+ のファミリー
# 指定名, M+ ファイル名の接頭辞, 生成するフォントのファミリー名
variants = [
    ("1", "MPLUS1", "McMejiro"),
    ("2", "MPLUS2", "McMejiro2"),
    ("3", "MPLUS3", "McMejiro3"),
]
default_variants = ["1"]

# フォントリスト
# Roboto ファイル名, M+ ウェイト, Mejiro ウェイト
font_list = [
    ("Roboto-Thin.ttf", "Thin", "Thin"),
    ("Roboto-Light.ttf", "Light", "Light"),
    ("Roboto-Regular.ttf", "Regular", "Regular"),
    ("Roboto-Medium.ttf", "Medium", "Semibold"),
    ("Roboto-Bold.ttf", "Bold", "Bold"),
    ("Roboto-Black.ttf", "Black", "Extrabold"),
]

def select_variants(args):
    names = [v[0] for v in variants]
    if not args:
        args = default_variants
    if "all" in args:
        args = names
    unknown = [a for a in args if a not in names]
    if unknown:
        sys.exit("Unknown variant: {0} (choose from 1, 2, 3, all)".format(" ".join(unknown)))
    return [v for v in variants if v[0] in args]

def main():
    # 縦書き対応
    fontforge.setPrefs('CoverageFormatsAllowed', 1)

    today = date.today()

    for (_, mp_prefix, family) in select_variants(sys.argv[1:]):
        # バージョンを今日の日付から生成する
        version = "{0}-{1}".format(family, today.strftime("%Y%m%d"))

        for (rb, mp_weight, weight) in font_list:
            rb_path = "{0}/{1}".format(roboto_path, rb)
            mp_path = "{0}/{1}-{2}.ttf".format(mplus_path, mp_prefix, mp_weight)
            ko_path = "{0}/{1}-{2}.ttf".format(mejiro_path, family, weight)
            print("Generating: {0}".format(ko_path))
            generate_mejiro(rb_path, mp_path, ko_path, family, weight, version)

def mejiro_sfnt_names(family, weight, version):
    return (
        ('English (US)', 'Copyright',
         '''\
         McMejiro: Copyright (c) 2022- AndroPlus.

         Roboto: Copyright (c) 2012- Google.
         M+ FONTS: Copyright (C) 2021- M+ FONTS PROJECT.'''),
        ('English (US)', 'Family', '{0} {1}'.format(family, weight)),
        ('English (US)', 'SubFamily', weight),
        ('English (US)', 'Fullname', '{0}-{1}'.format(family, weight)),
        ('English (US)', 'Version', version),
        ('English (US)', 'PostScriptName', '{0}-{1}'.format(family, weight)),
        ('English (US)', 'Vendor URL', 'https://mejiro.andro.plus'),
        ('English (US)', 'Preferred Family', family),
        ('English (US)', 'Preferred Styles', weight),
        ('Japanese', 'Preferred Family', family),
        ('Japanese', 'Preferred Styles', weight),
    )

def mejiro_gasp():
    return (
        (8, ('antialias',)),
        (13, ('antialias', 'symmetric-smoothing')),
        (65535, ('antialias', 'symmetric-smoothing')),
    )

def generate_mejiro(rb_path, mp_path, ko_path, family, weight, version):
    # M+ を開く
    font = fontforge.open(mp_path)

    # EMの大きさを2048に設定する
    font.em = 2048

    # Roboto を開く
    rbfont = fontforge.open(rb_path)

    # Roboto に含まれるグリフを削除する
    font.selection.none()
    rbfont.selection.all()
    for glyph in rbfont.selection.byGlyphs:
        if glyph.glyphname in font:
            font.selection.select(("more",), glyph.glyphname)
    font.clear()

    # Roboto をマージする
    font.mergeFonts(rb_path)
    for gs in font.gpos_lookups:
        li = font.getLookupInfo(gs)
        if li[2][0][0] == 'kern':
            font.removeLookup(gs)

    # ”fancy colon” U+EE01 を U+A789 にコピー
    font.selection.select(0xee01)
    font.copy()
    font.selection.select(0xa789)
    font.paste()

    # フォント情報の設定
    font.sfnt_names = mejiro_sfnt_names(family, weight, version)
    font.os2_vendor = "andp"

    # Grid Fittingの設定
    font.gasp = mejiro_gasp()

    # TTF の生成
    # Roboto のヒンティング命令は参照先の fpgm/cvt/prep が無く掠れの原因になるので出力しない
    font.generate(ko_path, '', ('short-post', 'opentype', 'PfEd-lookups', 'omit-instructions'))

if __name__ == '__main__':
    main()
