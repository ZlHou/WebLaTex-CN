$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error -shell-escape %O %S';
$biber = 'biber %O %S';
$out_dir = 'build';
