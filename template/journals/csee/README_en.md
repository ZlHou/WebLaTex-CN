# CSEE LaTeX3 Paper Template

An unofficial template for Proceedings of the CSEE, based on the supplied
`docs/20230420110546.doc`. The `csee.cls` class uses LaTeX3 (`expl3`) for metadata,
keys, titles, abstracts and appendix logic. CTEX and standard LaTeX packages
provide Chinese typesetting, mathematics, floats and two-column output.
The supplied Word file is the reference; this template does not claim compliance
with subsequent journal revisions.

[中文](README.md)

## Files and compilation

| File | Purpose |
| --- | --- |
| `csee.cls` | Document class |
| `main.tex` | Complete editable example |
| `csee-doc.tex` | Standalone LaTeX user guide organized after the SUEPTeX handbook |
| `build/csee-doc.pdf` | Compiled Chinese guide with examples, troubleshooting and Word comparison records |
| `.latexmkrc` | XeLaTeX configuration; output goes to `build/` |
| `build/main.pdf` | Compiled example |
| `docs/20230420110546.doc` | Original Word layout reference |
| `.gitignore` | Git exclusions for build outputs, auxiliary and temporary files |

Verified locally with a complete TeX Live 2026 installation. Prefer XeLaTeX:

```sh
latexmk main.tex
latexmk csee-doc.tex
```

Generated PDFs go to `build/` and are excluded from Git. Compile them after
obtaining the project. To force a guide rebuild, run `latexmk -g csee-doc.tex`.

Alternatively, run twice:

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The alternative writes the PDF to the project root. Set your editor to XeLaTeX
and keep the class next to the main file. pdfLaTeX is unsupported.
The paper also supports LuaLaTeX; compile the guide with XeLaTeX. The class loads CTEX, fontspec, geometry, amsmath, newtxmath,
graphicx, booktabs, caption, enumitem, siunitx, fancyhdr, cite and hyperref.
The example additionally uses TikZ.

## Paper metadata

Set fields with `\cseesetup{...}` in the preamble, then call `\maketitle` and
`\makeabstract` after `\begin{document}`. Titles and author information span
both columns; abstracts and main text use two columns.

```tex
\documentclass{csee}
\cseesetup{
  title = {中文题名},
  title-en = {English Title},
  authors = {张三，李四},
  authors-en = {ZHANG San, LI Si},
  affiliations = {（作者单位、地址与邮编）},
  affiliations-en = {(Affiliation, Address and Postal Code)},
  abstract-en = {English abstract.},
  keywords-en = {keyword one; keyword two},
  abstract = {中文摘要。},
  keywords = {关键词一；关键词二},
}
\begin{document}
\maketitle
\makeabstract
\section{引言}
正文内容。
\end{document}
```

Optional fields are `article-id`, `clc`, `document-code`, `subject-code`,
`funding`, `funding-en` (unnumbered funding notes in the first left column),
`short-title` (odd-page header), and `editor`. Empty fields omit their content.
Supply affiliation parentheses and punctuation yourself. Use `\\` for multiple
affiliation lines and `\textsuperscript{1}` for affiliation markers. English
capitalization and name spelling are author-controlled. For classification
spacing, write e.g. `TM\hspace{0.25em}73`.

## Text, floats and references

Use `\section`, `\subsection` and `\subsubsection` for numbered headings.
They correspond to levels two, three and four in the source Word document.
`\section` uses 12 bp SimHei and Arial with 6 bp before and after;
`\subsection` uses 10.5 bp SimHei and Arial with zero paragraph spacing.
Both wrap without hanging indentation.
The `enumerate` environment labels items `1）`, `2）`. Use `\num{12345.87908}`
and `\qty{50}{\hertz}` for grouped numbers and number-unit spacing.
Use math mode for variables and `equation` with `aligned` for multiline
equations. Place a line-ending operator on the preceding line as requested
by the reference; the class does not select equation breaks automatically.

Inside standard `figure` and `table` environments, use:

```tex
\cseecaption{中文图题或表题}{English Caption}
\label{fig:example}
```

Place table captions above tables and figure captions below figures. Refer
with `\ref{fig:example}`. Use `figure*` and `table*` for full-width floats;
their placement follows LaTeX's two-column float rules. Prefer booktabs tables:
outer rules are 0.75 bp and column rules are 0.5 bp. `tabular` and `tabular*`
default to 7.5 bp type with 14 bp leading. Set external figure labels to 7.5 bp
SimSun and Times New Roman in the drawing tool; the class cannot change text
or line widths embedded in images.

`cseedefinition` and `cseetheorem` provide independently numbered definitions
and theorems, with optional names. `cseeacknowledgements` provides an unnumbered
acknowledgements heading, centered in 10.5 bp SimHei. Its body follows the
specified font: 10.5 bp KaiTi, 32.3 bp leading and a 0.74 cm first-line
indent. Windows mode uses the system KaiTi font; Fandol mode uses Fandol Kai.
Use `thebibliography`, `\bibitem` and `\cite` for
manual references with bracketed superscript citations. Arrange entries in
first-citation order; the class neither sorts nor generates entries. The
example preserves the reference's GB/T 7714—2005 convention and bilingual
entries instead of substituting another BibLaTeX standard version.

## Appendices and biographies

```tex
\appendix
\section{补充推导} % Appendix A: separate figure/table/equation counters start at A1
% ...
\section{补充数据} % Appendix B: the counters restart at B1
\begin{cseebiography}[portrait.jpg]{张三}
（1990—），男，博士，研究方向为电力系统；E-mail：\url{author@example.com}。
\end{cseebiography}
\cseeeditor
```

The portrait path is optional. Crop portraits to **11:14** beforehand and use
at least **260 × 330 pixels**. With this ratio, the output measures **2.2 × 2.8 cm**.
The class preserves aspect ratio rather than stretching or cropping. A biography
with a photo is an indivisible block and cannot break across pages.

## Reference layout and differences

| Reference requirement | Implementation |
| --- | --- |
| A4; top/bottom/left/right margins 3.2/2.5/2.0/2.0 cm | Follows the written dimensions |
| Two columns, 0.78 cm gap | Full-width title; two-column abstracts and text |
| Header starts 2 cm from paper top | Bilingual first-page journal name; outer page numbers, even-page journal name, odd-page short title; no footer text |
| 10.5-point body; 0.74 cm first-line indent | SimSun and Times New Roman at 10.5 bp |
| 42 lines per page | Body baseline is text height divided by 42, approximately 16.20 bp |
| Chinese title 22 points; authors 14 points | SimHei/Arial at 22 bp, FangSong at 14 bp |
| Bold English title at 12 points | Times New Roman Bold at 12 bp |
| Abstracts, captions and references at 9 points, 14-point leading | 9 bp, 14 bp leading; bold captions |
| Math text/scripts/nested scripts at 10.5/6.5/4.5 points | Corresponding bp sizes with newtxmath |
| Independent appendix numbering | Figure, table and equation counters reset in every appendix |

Word's points are PostScript points, represented by `bp` in LaTeX. The stored
Word top margin is approximately **2.7 cm**, conflicting with the written
**3.2 cm** requirement; this class follows the latter. Word's document grid
and 45/21-character line settings have no identical LaTeX counterpart. LaTeX's
line breaking, mixed scripts, equations, floats and headings do not guarantee
identical pagination or line counts. MathType's legacy symbol font and symbol
size levels are replaced by Times-style newtxmath.
The first-page header uses two 0.48 bp rules with a 0.48 bp clear gap;
subsequent pages use a 0.72 bp rule. Header text and rules are positioned to
match the Word reference PDF, while the body retains its 3.2 cm top margin.
Appendix headings use 9 bp SimHei and Arial with 3 bp spacing before and after;
the reference heading uses 4 bp spacing. See the guide's comparison record.

The default `fontset=auto` selects SimSun, SimHei, KaiTi, FangSong, Times New
Roman and Arial if SimSun is found; all those fonts must be installed in this
mode. Otherwise it selects Fandol, TeX Gyre Termes and TeX Gyre Heros. To force
the portable font set:

```tex
\documentclass[fontset=fandol]{csee}
```

Fandol supports portable compilation but differs from the specified Windows
fonts in letterforms.

## Git version control

Initialize and commit from the project root:

```sh
git init
git add .
git status
git commit -m "Initial commit"
```

Skip `git init` for an existing repository. Review staged files with `git status`
before committing. Keep `.tex`, `.cls`, `.latexmkrc`, the READMEs, the original
Word document and figures under version control. `.gitignore` excludes `build/`,
root-level `main.pdf` and `csee-doc.pdf`, LaTeX auxiliary files and editor temporary
files. PDF figures remain trackable because PDF files are not excluded globally.
Ignore rules do not remove files that Git already tracks.

## Building and checking

The current directory does not include the earlier development `tests/` and
`tools/` directories. For routine checks, build directly:

```sh
latexmk main.tex
latexmk csee-doc.tex
```

Check `build/main.log` and `build/csee-doc.log` for errors, missing characters,
undefined references and Overfull messages. Inspect the resulting PDFs,
especially long headings, odd/even headers, acknowledgements, appendices,
external images and complex tables. Successful compilation does not replace
checking pagination after content changes.
