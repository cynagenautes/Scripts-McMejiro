#!/bin/bash

bldblu=${txtbld}$(tput setaf 4)

mkdir -p mejiro mplus roboto
cd roboto
wget "https://github.com/google/fonts/raw/main/ofl/roboto/Roboto%5Bwdth,wght%5D.ttf" -O "Roboto[wdth,wght].ttf"
# 静的フォントはバリアブルフォントから切り出す (Google Fonts の ZIP 配布は終了)
for w in Thin:100 Light:300 Regular:400 Medium:500 Bold:700 Black:900; do
    fonttools varLib.instancer "Roboto[wdth,wght].ttf" wght=${w#*:} wdth=100 --static -o "Roboto-${w%%:*}.ttf"
done
cd ../

cd mplus
wget https://github.com/coz-m/MPLUS_FONTS/archive/refs/heads/master.zip -O mplus.zip
# M+ 1 / M+ 2 / M+ 3 の静的フォントとバリアブルフォントだけを展開する
unzip -j -o mplus.zip "*/fonts/MPLUS[123]/ttf/*.ttf" "*/fonts/MPLUS[123]/variable/*.ttf"
cd ../

echo "McMejiro を生成するには FontForge をインストールし、以下を実行してください"
echo "fontforge -lang=py -script mejiro.py [1|2|3|all]"
echo "バリアブルフォントを生成するには fontTools をインストールし、以下を実行してください"
echo "python3 mejiro_vf.py [1|2|3|all]"
tput sgr0
