# 卒業論文の執筆手順

VS Code で書き，困ったときは Claude（アプリ版）に聞く．
規則と書き方の詳細は `README.md` にある．

## 1. 準備（最初に1回）

1. TeX Live をインストールする（Mac は MacTeX）．
2. VS Code に拡張機能「LaTeX Workshop」をインストールする．
3. 雛形をダウンロードする．
   - <https://github.com/kazumichiINOUE/irlab-thesis-template/archive/refs/heads/main.zip> を開くと，zip がダウンロードされる．
   - zip を展開し，`main.tex` が直下にあるフォルダ（`irlab-thesis-template-main`）を取り出す．
   - フォルダ名を苗字のローマ字の小文字に変える（例：`saitama`）．
   - フォルダの置き場所のパスに，日本語や空白を含めない（例：`C:\thesis\saitama`，`~/thesis/saitama`）．
4. VS Code の「ファイル」→「フォルダーを開く」で，このフォルダを開く．
   - ファイル単体ではなく，フォルダごと開く（フォルダ内の `.vscode` の設定を使うため）．
5. `main.tex` を開き，右上の ▷（Build LaTeX project）を押す．
   - 右上の PDF のアイコン（View LaTeX PDF）で PDF が表示されれば準備完了．
   - PDF は `build/main.pdf` にできる．

## 2. 書く

| 書くもの | ファイル |
|---|---|
| 題目，氏名，コース（中学校・小学校） | `meta.tex` |
| Abstract，要旨 | `abstract_en.tex`，`abstract_ja.tex` |
| 本文 | `chapters/` の各ファイル（章を増やすときは `chapters.tex` にも足す） |
| 謝辞 | `acknowledgments.tex` |
| 付録 | `appendix.tex` |
| 参考文献 | `references.bib` |
| 図，プログラム | `fig/`，`src/` に置く |

- 保存するたびに自動でコンパイルされ，PDF が更新される．
- 図・表・数式・引用の書き方は，記入例の `sample/` を見る．仕上がりは `sample/sample.pdf`．
- 次の3つを守る．詳しくは `README.md` の「書き方の規則」．
  - `main.tex` と `irlthesis.sty` は編集しない．
  - 図は `fig/overview.png` のようにフォルダから書く．ファイル名は半角英数字にする．
  - 参考文献は `references.bib` に書き，本文で `\cite{キー}` と引用する．

## 3. 困ったとき：Claude に聞く

1. Claude で新しいチャットを始める．
2. `README.md` と，エラーの出たファイル（例：`chapters/02_method.tex`）を添付する．
3. VS Code の下の「問題」タブに出たエラーをコピーし，次のように頼む．

   ```
   卒業論文を LaTeX で書いている．添付の README.md に従って，
   次のエラーの原因と直し方を教えてほしい．

   （ここにエラーを貼る）
   ```

4. 示された修正を，自分で VS Code のファイルに反映して保存する．

- Claude は本文を書かない．聞けるのは LaTeX の書き方とエラーの直し方である．
- 新しいチャットでは前の内容が引き継がれない．`README.md` をそのたびに添付する．

## 4. 提出

1. VS Code の「ターミナル」→「新しいターミナル」で，形式をチェックする．

   ```
   python3 tools/check.py     （Windows では py tools\check.py）
   ```

   - ERROR がなくなるまで直す．WARN は内容を確かめる．
   - Python が入っていない場合は，指導教員に伝える．
2. `build` フォルダを削除し，フォルダ全体を zip にして提出する．
   - フォルダ名は苗字のローマ字の小文字（例：`saitama`）にしておく．

## うまくいかないとき

| 症状 | 対処 |
|---|---|
| PDF ができない．「pdflatex」と表示される | フォルダごと開いているか．`.vscode` フォルダを消していないか |
| 参照が `??`，引用が `[?]` になる | もう一度保存する（再コンパイルされる） |
| それでも直らない | 3. の手順で Claude に聞く．解決しなければ指導教員に相談する |

## 補足：git で管理したい人へ

ダウンロードの代わりに，クローンしてもよい．

```
git clone https://github.com/kazumichiINOUE/irlab-thesis-template.git saitama
```

研究室のリポジトリには push できない．自分のリポジトリで管理するときは，必ず非公開（private）にする．
