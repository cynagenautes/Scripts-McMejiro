# Scripts

[McMejiro](https://github.com/AndroPlus-org/McMejiro) をビルドするためのスクリプトです。

| スクリプト | 生成物 | 必要なもの |
|:---|:---|:---|
| `mejiro.py` | 静的フォント `mejiro/McMejiro*-*.ttf` (6 ウェイト) | FontForge |
| `mejiro_vf.py` | バリアブルフォント `mejiro/McMejiro*[wght].ttf` | Python 3, fontTools |

和文部分の元にする M+ は M+ 1 / M+ 2 / M+ 3 から選べます。欧文部分はいずれも Roboto です。

| 指定 | 元にする M+ | 生成するファミリー | 静的フォント | バリアブルフォント |
|:---:|:---|:---|:---|:---|
| `1` (省略時) | M+ 1 | McMejiro | `McMejiro-*.ttf` | `McMejiro[wght].ttf` |
| `2` | M+ 2 | McMejiro2 | `McMejiro2-*.ttf` | `McMejiro2[wght].ttf` |
| `3` | M+ 3 | McMejiro3 | `McMejiro3-*.ttf` | `McMejiro3[wght].ttf` |
| `all` | 上の 3 つすべて | | | |

各スクリプトの引数に指定します。複数並べることもできます (例: `2 3`)。

## 使い方

```
git clone https://github.com/AndroPlus-org/Scripts-McMejiro make_mejiro
```

```
cd make_mejiro
```

M+ 1 / M+ 2 / M+ 3 と Roboto (静的フォント・バリアブルフォント) を `mplus/`、`roboto/` にダウンロードします。`wget`、`unzip`、fontTools (`pip install fonttools`) が必要です。Roboto の静的フォントはバリアブルフォントから切り出します。

```
bash setup.sh
```

#### Ubuntu / WSL での fontTools の導入

apt の `python3-fonttools` は古く、`fonttools varLib.instancer: error: unrecognized arguments: --static` などのエラーになります。venv を作って pip で最新版を入れてください (Ubuntu 23.04 以降はシステムへの `pip install` が拒否されるため)。

```
sudo apt install python3-venv
python3 -m venv ~/.venv/mejiro
source ~/.venv/mejiro/bin/activate
pip install fonttools
```

以降は `source ~/.venv/mejiro/bin/activate` してから `setup.sh` や `mejiro_vf.py` を実行します。apt 版が入っている場合は `sudo apt remove python3-fonttools fonttools` で削除しておくと混同しません。

### 静的フォント

FontForge interactive console で実行します。

```
fontforge -lang=py -script mejiro.py        # M+ 1 版 (McMejiro)
fontforge -lang=py -script mejiro.py 2      # M+ 2 版 (McMejiro2)
fontforge -lang=py -script mejiro.py all    # 3 種類すべて
```

| McMejiro | M+ 1 / 2 / 3 | Roboto |
|:---:|:---:|:---:|
| **Thin** | Thin | Thin |
| **Light** | Light | Light |
| **Regular** | Regular | Regular |
| **Semibold** | Medium | Medium |
| **Bold** | Bold | Bold |
| **Extrabold** | Black | Black |

### バリアブルフォント (wght 100-900)

M+ (`MPLUS1[wght].ttf` / `MPLUS2[wght].ttf` / `MPLUS3[wght].ttf`) と Roboto (`Roboto[wdth,wght].ttf`) のバリアブルフォントから `mejiro/McMejiro[wght].ttf` / `McMejiro2[wght].ttf` / `McMejiro3[wght].ttf` を生成します。1 種類あたり数分かかります。

```
pip install fonttools
```

```
python3 mejiro_vf.py        # M+ 1 版 (McMejiro)
python3 mejiro_vf.py 3      # M+ 3 版 (McMejiro3)
python3 mejiro_vf.py all    # 3 種類すべて
```

- ウェイト軸 `wght` 100-900 (デフォルト 400)
- Roboto の幅軸 `wdth` は 100 で固定
- 100 刻みの 9 ウェイトでそれぞれ合成したものをマスターにしてまとめ直すため、元のバリアブルフォントの形状をそのまま再現します
- 名前付きインスタンス: Thin (100) / ExtraLight (200) / Light (300) / Regular (400) / Medium (500) / SemiBold (600) / Bold (700) / ExtraBold (800) / Black (900)

インスタンス名は標準的なウェイト名に合わせているため、静的フォントとは対応が異なります (静的フォントの Semibold は Medium から作っているので wght 500 相当)。
