# latexmk の設定（編集しない）
# このディレクトリで `latexmk` と打つと，LuaLaTeX と biber で main.tex をコンパイルする．
# 生成物はすべて build/ に出る．PDF は build/main.pdf．

@default_files = ('main.tex');
$pdf_mode = 4;    # LuaLaTeX で PDF を作る
$lualatex = 'lualatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$out_dir = 'build';
