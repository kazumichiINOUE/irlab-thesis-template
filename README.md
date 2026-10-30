# 卒業論文の雛形（埼玉大学 教育学部 情報・ロボット研究室）

この雛形で，卒業論文を1冊の論文としてコンパイルする．
同じファイルは，研究室の卒業論文集にもそのまま取り込まれる．
そのため，ファイルの役割と「書き方の規則」を守る．

- 執筆の手順（ダウンロード，VS Code と Claude の使い方，提出）は [GUIDE.md](GUIDE.md) にある．同じ内容の PDF は [GUIDE.pdf](GUIDE.pdf)．
- 記入例は [sample/](sample/) にある．仕上がりは [sample/sample.pdf](sample/sample.pdf)．
- 雛形一式のダウンロード：<https://github.com/kazumichiINOUE/irlab-thesis-template/archive/refs/heads/main.zip>

## 役割分担

- 本文（Abstract，要旨，各章，謝辞，付録，参考文献の中身）は，すべて学生本人が書く．
- Claude が手伝うのは，コンパイルとその周辺に限る．
  - エラー・警告の原因の特定と説明
  - LaTeX の書き方（図・表・数式・引用・ソースコードの入れ方）の説明
  - 本文の文言を変えない範囲でのマークアップの修正案（括弧の対応，特殊文字のエスケープ，ラベルと参照の対応など）
  - 「書き方の規則」に沿っているかの確認
- Claude は，本文の執筆・加筆・推敲・要約・翻訳をしない．
  文言を変えなければ直らない問題は，箇所と理由を示して学生に任せる．

## 必要な環境

TeX Live（LuaLaTeX，biber，latexmk を含む）を使う．次の3つが動けばよい．

```sh
lualatex --version
biber --version
latexmk --version
```

## コンパイル

VS Code の拡張機能 LaTeX Workshop でコンパイルする．
このディレクトリをフォルダとして開き，`.tex` ファイルを保存するか，右上の ▷（Build LaTeX project）を押す．
PDF は `build/main.pdf` にでき，右上のアイコン（View LaTeX PDF）で表示できる．

- `.vscode/settings.json` により，LaTeX Workshop は `latexmkrc` の設定（LuaLaTeX と biber，生成物は `build/`）で latexmk を実行する．
- latexmk は，参照や参考文献が確定するまで必要な回数を自動で繰り返す．
- エラーは VS Code の「問題」タブに出る．全体の記録は `build/main.log`，参考文献の記録は `build/main.blg`．

ターミナルからは次のように実行する．

```sh
latexmk       # コンパイル
latexmk -C    # PDF も含めて生成物を消す
```

## ファイルの構成

| ファイル | 中身 | 編集 | 論文集 |
|---|---|---|---|
| `meta.tex` | 題目，氏名，所属コース（中学校・小学校），年度，提出日 | する | 部の扉に使う |
| `abstract_en.tex` | Abstract（本文だけ） | する | 載る |
| `abstract_ja.tex` | 要旨（本文だけ） | する | 載る |
| `chapters.tex` | 章のファイルの並び | する | 載る |
| `chapters/*.tex` | 各章（`\chapter` から書く） | する | 載る |
| `acknowledgments.tex` | 謝辞（本文だけ） | する | 載らない |
| `appendix.tex` | 付録（`\chapter` から書く） | する | 載る |
| `references.bib` | 参考文献 | する | 載る |
| `preamble.tex` | 追加のパッケージと命令 | 必要なときだけ | 読み込む |
| `fig/` | 図のファイル | 置く | |
| `src/` | 付録に載せるソースコード | 置く | |
| `main.tex` | 個人版の組み立て | しない | 使わない |
| `irlthesis.sty` | 研究室共通のスタイル | しない | 研究室の正本を使う |
| `latexmkrc`，`.vscode/` | コンパイルの設定 | しない | |
| `tools/check.py` | 形式のチェック | しない | |
| `GUIDE.md`，`GUIDE.pdf` | 執筆の手順 | しない | |
| `tools/make_guide_pdf.sh` | `GUIDE.pdf` を作る（教員用） | しない | |
| `sample/` | 記入例（ダミーの本文） | しない | 使わない |

個人版の並びは，表紙，Abstract，要旨，目次（図目次・表目次），本文，謝辞，付録，参考文献である．
論文集では，表紙・目次・謝辞を除き，部の扉，Abstract，要旨，本文，付録，参考文献の順に載る．

## 書き方の規則

論文集は，`main.tex` を使わずに上の各ファイルを直接読み込み，全員の論文を一つの文書として組む．
次の規則は，そのための規則である．

1. `main.tex` と `irlthesis.sty` は編集しない．書き足しても論文集には反映されない．
2. 章を増やすときは，`chapters/` にファイルを作り，`chapters.tex` に `\input{chapters/ファイル名}` を足す．`\include` は使わない．
3. ファイルのパスは，このディレクトリから書く．図は `fig/`，ソースコードは `src/` に置き，`fig/overview.pdf` のように書く．`\graphicspath` は使わない．
4. ファイル名とディレクトリ名には，半角英数字と `-` `_` だけを使う．空白や日本語を使わない．
5. 参考文献は `references.bib` に書き，本文で `\cite{キー}` と引用する．`thebibliography` 環境と `\bibitem` は使わない．
6. パッケージの追加と命令の定義は `preamble.tex` にだけ書く．`\newcommand` で作る命令の名前は，自分の苗字で始める（例：`\saitamaFig`）．論文集では全員の `preamble.tex` を一つの文書で読むため，名前が重なるとエラーになる．
7. 本文のファイルに，ページや文書全体の設定を変える命令を書かない．`\documentclass`，`\usepackage`，`\pagestyle`，`\pagenumbering`，`\setcounter{page}`，`\frontmatter`，`\mainmatter`，`\appendix`，`\tableofcontents`，`\printbibliography` などである．
8. ラベルには種類を表す接頭辞を付ける．章 `chap:`，節 `sec:`，図 `fig:`，表 `tab:`，式 `eq:`，ソースコード `lst:`．同じ論文の中では重ねない．他の学生と同じ名前でもよい（論文集では論文ごとに区別される）．
9. キャプションに `\ref` や `\cite` を書くときは，`\caption[図目次用の短い文]{本文用の文}` とし，図目次用の文には書かない．
10. 論文集では，図の配置指定を `[t]`，表を `[b]` にそろえる．個人版でも同じ指定にしておくと，論文集との違いが出ない．

## 書き方の例

記入例 `sample/` に，以下の例を実際に使った原稿と，その仕上がり（`sample/sample.pdf`）がある．

### 図

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\linewidth]{fig/overview.pdf}
  \caption{システムの概要}
  \label{fig:overview}
\end{figure}
```

本文では `Fig.~\ref{fig:overview}に示す．` のように参照する．

### 図の横並び

```latex
\begin{figure}[t]
  \centering
  \begin{subfigure}{0.45\linewidth}
    \centering
    \includegraphics[width=\linewidth]{fig/before.png}
    \caption{処理前}
    \label{fig:before}
  \end{subfigure}
  \begin{subfigure}{0.45\linewidth}
    \centering
    \includegraphics[width=\linewidth]{fig/after.png}
    \caption{処理後}
    \label{fig:after}
  \end{subfigure}
  \caption{処理の前後の画像}
  \label{fig:beforeafter}
\end{figure}
```

### 表

```latex
\begin{table}[b]
  \centering
  \caption{実験条件}
  \label{tab:condition}
  \begin{tabular}{lr}
    \toprule
    項目 & 値 \\
    \midrule
    試行回数 & 10 \\
    距離 & \SI{1.5}{m} \\
    \bottomrule
  \end{tabular}
\end{table}
```

表のキャプションは表の上に置く．本文では `Table~\ref{tab:condition}` と参照する．

### 数式

```latex
\begin{equation}
  F = ma
  \label{eq:newton}
\end{equation}
```

本文では `式\eqref{eq:newton}` と参照する．

### 参考文献

`references.bib` に項目を書き，本文で `\cite{example2025}` と引用する．
引用した項目だけが，引用順に参考文献リストへ載る．
書式の例（論文，書籍，Web ページ）は `references.bib` にある．

### ソースコード

```latex
\lstinputlisting[style=customPython, caption={計測プログラム}, label={lst:measure}]{src/measure.py}
```

`style` には `customPython`，`customC`，`customText` がある．
過去の論文で使われた `\includeCode[Python]{src/measure.py}{計測プログラム}` も使える．

## 提出前の確認

VS Code のターミナルで実行する．

```sh
python3 tools/check.py     # Windows では py tools\check.py
```

ERROR がなくなるまで直す．WARN は，指摘の内容を確かめる．
Python が入っていない場合は，指導教員に伝える．

提出物は，`build/` を除いたこのディレクトリ一式である．
ディレクトリ名は，苗字のローマ字の小文字にする（例：`saitama`）．

## Claude への作業指示

学生は基本的に Claude のアプリ版を使い，この README と，問題のあるファイルを添付して質問する．
アプリ版の Claude はコマンドを実行できず，添付されていないファイルは見えない．
Claude Code を使う場合の違いは，最後の項目に書く．

- 回答の前に，この README の「役割分担」と「書き方の規則」を確認する．
- 学生が貼ったエラーメッセージと添付ファイルから原因を特定し，平易に説明する．判断に足りないファイルやログがあれば，どのファイルが要るかを具体的に伝えて添付を頼む．
- 修正は「ファイル名，行番号，修正前，修正後」の形で示す．アプリ版では，ファイルの書き換えは学生が行う．
- 修正は LaTeX のマークアップに限る．本文の語句・文・段落を書き換えない．書き足さない．本文の執筆・推敲・要約・翻訳を頼まれても引き受けず，この README の役割分担を伝える．
- `main.tex`，`irlthesis.sty`，`latexmkrc`，`.vscode/` は編集させない．パッケージが必要なときは，`preamble.tex` に追加する行を示す．
- 規則に反する書き方（`\graphicspath`，`thebibliography`，本文中の `\usepackage` など）を見つけたら，規則に沿う書き方を示す．
- 修正の後は，保存して再コンパイルし，「問題」タブにエラーが残っていないかを確かめるよう学生に伝える．
- Claude Code のようにコマンドを実行できる環境では，自分で `latexmk` を実行し，`build/main.log` を読んで原因を特定する．マークアップの修正は，学生の了承を得てからファイルに反映する．反映の後は再コンパイルし，`python3 tools/check.py` で規則違反がないことを確かめる．

## よくあるエラー

| 症状 | 確かめること |
|---|---|
| `File 'xxx' not found` | パスがこのディレクトリから書かれているか．ファイル名の大文字・小文字と拡張子 |
| `Undefined control sequence` | 命令の綴り．必要なパッケージを `preamble.tex` で読み込んでいるか |
| `Missing $ inserted` | 本文の `_` `^` `&` `%` `#` は `\_` のようにエスケープする |
| 参照が `??` になる | `\label` と `\ref` の名前の一致．もう一度保存してコンパイルする |
| 引用が `[?]`，参考文献が出ない | `\cite` のキーと `references.bib` のキーの一致．`build/main.blg` の biber のエラー |
| biber が失敗し続ける | `build/` を削除してから，もう一度コンパイルする |
| VS Code で pdfLaTeX が動く．`%OUTDIR%` というディレクトリができる | フォルダごと開いているか．`.vscode/settings.json` を雛形のまま置いているか |
