#!/bin/sh
# GUIDE.md から GUIDE.pdf を作る（教員用．学生は使わない）
# GUIDE.md を直したら実行する．macOS の Google Chrome と gh（GitHub CLI）を使う．
#   sh tools/make_guide_pdf.sh [出力先]   （出力先を省くと GUIDE.pdf）
set -eu
cd "$(dirname "$0")/.."
out="${1:-GUIDE.pdf}"
case "$out" in /*) ;; *) out="$PWD/$out" ;; esac
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# GitHub と同じ描き方で HTML にする
gh api markdown -f mode=markdown -F text=@GUIDE.md > "$tmp/body.html"

cat > "$tmp/guide.html" <<'EOF'
<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>卒業論文の執筆手順</title>
<style>
  @page { size: A4; margin: 14mm 17mm; }
  body {
    font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", sans-serif;
    font-size: 10pt; line-height: 1.5; color: #1f2328;
  }
  h1 { font-size: 18pt; margin: 0 0 4pt; padding-bottom: 4pt; border-bottom: 2px solid #1f2328; }
  h2 { font-size: 12.5pt; margin: 11pt 0 3pt; padding: 2pt 8pt; background: #eef1f4; border-left: 4px solid #1f2328; }
  h1, h2 { break-after: avoid; }
  p, li { margin: 1.5pt 0; }
  ol, ul { margin: 3pt 0; padding-left: 20pt; }
  ol { break-inside: avoid; }   /* 手順の途中で改ページしない */
  table { border-collapse: collapse; margin: 6pt 0; width: 100%; break-inside: avoid; }
  th, td { border: 1px solid #c8ccd1; padding: 2pt 6pt; text-align: left; vertical-align: top; }
  th { background: #f3f5f7; }
  code { font-family: Menlo, monospace; font-size: 9pt; background: #f3f5f7; padding: 0 3pt; border-radius: 3px; }
  pre { background: #f3f5f7; padding: 5pt 10pt; margin: 4pt 0; border-radius: 4px; break-inside: avoid; white-space: pre-wrap; }
  pre code { background: none; padding: 0; }
  a { color: #0b57d0; text-decoration: none; word-break: break-all; }
  .anchor, .octicon { display: none; }
  .markdown-heading { break-after: avoid; }
</style>
</head>
<body>
EOF
cat "$tmp/body.html" >> "$tmp/guide.html"
echo '</body></html>' >> "$tmp/guide.html"

"$chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf-no-header \
  --print-to-pdf="$out" "file://$tmp/guide.html" 2>/dev/null
echo "作成：$out"
