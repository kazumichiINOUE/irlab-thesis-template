#!/usr/bin/env python3
"""卒業論文のディレクトリが，研究室の論文集に取り込める形かを調べる．

使い方：
    python3 tools/check.py                 # 自分の論文（このディレクトリ）を調べる
    python3 tools/check.py DIR [DIR ...]   # 指定したディレクトリを調べる

ERROR があれば終了コード 1 を返す．WARN は論文集では動くが，確認したほうがよい点．
"""
import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent

REQUIRED = [
    "main.tex", "meta.tex", "preamble.tex", "abstract_en.tex", "abstract_ja.tex",
    "chapters.tex", "acknowledgments.tex", "appendix.tex", "references.bib",
    "irlthesis.sty",
]
# 雛形のまま使うファイル（論文集では読まないので，書き足しても反映されない）
UNCHANGED = ["main.tex", "irlthesis.sty"]
# 本文以外の役割をもつファイル（本文用の禁止命令の検査から外す）
NOT_CONTENT = {"main.tex", "preamble.tex", "meta.tex"}
# 検査しないディレクトリ（生成物，道具，記入例）
SKIP_DIRS = {"build", "tools", "sample"}

# 本文のファイルに書いてはいけない命令と，その理由
FORBIDDEN = [
    (r"\\documentclass|\\begin\{document\}|\\end\{document\}", "本文のファイルに文書の枠組みは書かない"),
    (r"\\usepackage|\\RequirePackage", "パッケージは preamble.tex で読み込む"),
    (r"\\graphicspath", "\\graphicspath は使わない．図は fig/xxx.pdf のように書く"),
    (r"\\begin\{thebibliography\}|\\bibliography\{|\\bibliographystyle|\\addbibresource|\\printbibliography",
     "参考文献は references.bib に書き，\\cite で引用する"),
    (r"\\tableofcontents|\\listoffigures|\\listoftables|\\maketitle", "目次・表紙は main.tex が作る"),
    (r"\\pagestyle|\\pagenumbering|\\setcounter\{page\}|\\frontmatter|\\mainmatter|\\backmatter",
     "ページ番号・ページの書式は変えない"),
    (r"\\appendix\b", "\\appendix は main.tex が出す．付録は appendix.tex に書く"),
    (r"\\include\{", "\\include ではなく \\input を使う"),
]
VERBATIM_ENVS = ("lstlisting", "verbatim", "minted")
FILE_COMMANDS = [
    # (正規表現, 拡張子を省略したときに試す拡張子)
    (r"\\includegraphics\*?(?:\[[^\]]*\])?\{([^}]+)\}", ["", ".pdf", ".png", ".jpg", ".jpeg", ".eps"]),
    (r"\\lstinputlisting(?:\[[^\]]*\])?\{([^}]+)\}", [""]),
    (r"\\includeCode(?:\[[^\]]*\])?\{([^}]+)\}", [""]),
    (r"\\input\{([^}]+)\}", ["", ".tex"]),
]


class Report:
    def __init__(self, root):
        self.root = root
        self.items = []

    def error(self, msg, path=None, line=None):
        self.items.append(("ERROR", self._where(path, line), msg))

    def warn(self, msg, path=None, line=None):
        self.items.append(("WARN", self._where(path, line), msg))

    def _where(self, path, line):
        if path is None:
            return ""
        rel = path.relative_to(self.root) if path.is_absolute() else path
        return f"{rel}:{line}" if line else str(rel)

    @property
    def n_errors(self):
        return sum(1 for level, _, _ in self.items if level == "ERROR")


def code_lines(path):
    """コメントと verbatim 系の環境を除いた (行番号, 行) を返す．"""
    in_verbatim = None
    for no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if in_verbatim:
            if re.search(r"\\end\{%s\}" % in_verbatim, raw):
                in_verbatim = None
            continue
        line = re.sub(r"(?<!\\)%.*$", "", raw)
        m = re.search(r"\\begin\{(%s)\}" % "|".join(VERBATIM_ENVS), line)
        if m and not re.search(r"\\end\{%s\}" % m.group(1), line):
            in_verbatim = m.group(1)
        yield no, line


def surname(root):
    meta = root / "meta.tex"
    if not meta.exists():
        return None
    m = re.search(r"\\thesisauthoren\{([^}]*)\}", meta.read_text(encoding="utf-8"))
    if not m:
        return None
    upper = [w for w in m.group(1).split() if w.isupper() and len(w) > 1]
    return upper[-1].lower() if upper else None


def check(root):
    rep = Report(root)

    for name in REQUIRED:
        if not (root / name).exists():
            rep.error(f"{name} がない（雛形から消さない）")

    if root.resolve() != TEMPLATE_DIR:
        for name in UNCHANGED:
            mine, orig = root / name, TEMPLATE_DIR / name
            if mine.exists() and orig.exists() and mine.read_bytes() != orig.read_bytes():
                rep.warn(f"{name} が雛形から変更されている．論文集では雛形の {name} を使う", mine)

    meta = root / "meta.tex"
    if meta.exists():
        text = meta.read_text(encoding="utf-8")
        for placeholder in ("卒業論文の題目", "埼玉 太郎", "Taro SAITAMA"):
            if placeholder in text:
                rep.warn(f"meta.tex に雛形の記入例「{placeholder}」が残っている", meta)

    tex_files = sorted(p for p in root.rglob("*.tex")
                       if not SKIP_DIRS & set(p.relative_to(root).parts[:-1]))
    labels = {}
    for path in tex_files:
        rel = path.relative_to(root)
        is_content = str(rel) not in NOT_CONTENT
        for no, line in code_lines(path):
            if is_content:
                for pattern, reason in FORBIDDEN:
                    if re.search(pattern, line):
                        rep.error(reason, path, no)
            for pattern, exts in FILE_COMMANDS:
                for m in re.finditer(pattern, line):
                    target = m.group(1).strip()
                    if "#" in target or "\\" in target:
                        continue  # 命令の定義の中の引数
                    if not any((root / (target + ext)).is_file() for ext in exts):
                        rep.error(f"{target} が見つからない（パスはこのディレクトリから書く）", path, no)
                    if re.search(r"[^\x21-\x7e]", target):
                        rep.warn(f"{target}：ファイル名に空白や日本語を使わない", path, no)
            if re.search(r"\\caption\{[^}]*\\(?:ref|autoref|eqref|pageref|cite)\b", line):
                rep.warn("キャプションに \\ref や \\cite を書くときは，\\caption[目次用の短い文]{本文用} とし，"
                         "目次用の文には書かない", path, no)
            for m in re.finditer(r"\\label\{([^}]+)\}", line):
                key = m.group(1)
                if "#" in key:
                    continue
                if key in labels:
                    rep.error(f"ラベル {key} が重複している（最初は {labels[key]}）", path, no)
                else:
                    labels[key] = f"{rel}:{no}"

    preamble = root / "preamble.tex"
    if preamble.exists():
        prefix = surname(root)
        for no, line in code_lines(preamble):
            if re.search(r"\\graphicspath", line):
                rep.error("\\graphicspath は使わない．図は fig/xxx.pdf のように書く", preamble, no)
            for m in re.finditer(r"\\(?:newcommand|DeclareRobustCommand|NewDocumentCommand)\*?\{?\\([A-Za-z@]+)", line):
                name = m.group(1)
                if prefix and not name.lower().startswith(prefix):
                    rep.warn(f"命令 \\{name} の名前が苗字（{prefix}）で始まっていない．論文集で他の学生と衝突しうる",
                             preamble, no)
            if re.search(r"\\(?:renewcommand|def)\b", line):
                rep.warn("\\renewcommand や \\def は，論文集では全員の論文に影響しうる", preamble, no)

    bib = root / "references.bib"
    if bib.exists():
        seen = {}
        for no, line in enumerate(bib.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = re.match(r"\s*@\w+\s*\{\s*([^,\s]+)\s*,", line)
            if m:
                key = m.group(1)
                if key in seen:
                    rep.error(f"文献キー {key} が重複している（最初は {seen[key]} 行目）", bib, no)
                seen.setdefault(key, no)

    return rep


def main(argv):
    dirs = [Path(a) for a in argv] or [TEMPLATE_DIR]
    n_errors = 0
    for d in dirs:
        root = d.resolve()
        rep = check(root)
        print(f"== {d}")
        if not rep.items:
            print("   問題なし")
        for level, where, msg in rep.items:
            print(f"   {level:5} {where + '  ' if where else ''}{msg}")
        n_errors += rep.n_errors
    return 1 if n_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
