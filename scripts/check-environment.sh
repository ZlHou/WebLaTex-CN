#!/usr/bin/env bash
set -euo pipefail

for tool in node npm xelatex lualatex latexmk biber bibtex latexindent fc-match pdftotext git python3 bwrap; do
    command -v "$tool" >/dev/null || { echo "Missing command: $tool" >&2; exit 1; }
done
node --version
npm --version
if command -v codex >/dev/null; then codex --version; fi
for file in ctexart.cls xeCJK.sty luatexja.sty fontspec.sty unicode-math.sty amsmath.sty amsthm.sty siunitx.sty algorithm.sty algorithmic.sty algorithm2e.sty tikz.sty pgfplots.sty biblatex.sty natbib.sty gb7714-2015.bbx XITSMath-Regular.otf; do
    kpsewhich "$file" >/dev/null || { echo "Missing TeX dependency: $file" >&2; exit 1; }
done
for family in 'Noto Serif CJK SC' 'XITS Math'; do
    fc-match -f '%{family}\n' "$family" | grep -F "$family" >/dev/null
done

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
cd "$scratch"
cat > smoke.tex <<'TEX'
\documentclass[UTF8,fontset=fandol]{ctexart}
\usepackage{amsmath,amsthm,unicode-math,siunitx,algorithm,algorithmic,tikz,pgfplots}
\setmathfont{XITS Math}
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{references.bib}
\begin{document}
\section{中文科技论文环境验证}
中文摘要：测试中文、数学公式、计量单位与参考文献。English text.
\[ E=mc^2,\qquad \int_0^1 x^2\,\mathrm{d}x=\frac{1}{3}. \]
实验温度为 \qty{300}{\kelvin}，参见文献\cite{smoke}。
\begin{algorithm}\caption{环境验证}\begin{algorithmic}
\STATE Compute $x=1+1$.
\end{algorithmic}\end{algorithm}
\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}
\printbibliography
\end{document}
TEX
cat > references.bib <<'BIB'
@article{smoke,
  author = {张三 and 李四},
  title = {中文科学排版环境测试},
  journal = {测试学报},
  year = {2026},
  volume = {1},
  pages = {1--2}
}
BIB
for engine in xelatex lualatex; do
    mkdir "$engine"
    if ! latexmk "-$engine" -interaction=nonstopmode -halt-on-error -outdir="$engine" smoke.tex >"$engine/build.txt" 2>&1; then
        cat "$engine/build.txt" >&2
        exit 1
    fi
    test -s "$engine/smoke.pdf"
    test -s "$engine/smoke.bbl"
    pdftotext "$engine/smoke.pdf" "$engine/smoke.txt"
    grep -F '中文科技论文环境验证' "$engine/smoke.txt" >/dev/null
    grep -F '中文科学排版环境测试' "$engine/smoke.txt" >/dev/null
    if grep -E 'Missing character:|There were undefined references|Citation .* undefined' "$engine/smoke.log"; then
        echo "Incomplete $engine output" >&2
        exit 1
    fi
    echo "$engine: Chinese, mathematics and Biber bibliography passed"
done
echo 'LaTeX environment OK'
