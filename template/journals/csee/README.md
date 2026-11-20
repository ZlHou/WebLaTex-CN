# CSEE LaTeX3 论文模板

根据 `docs/20230420110546.doc` 编写的《中国电机工程学报》非官方论文模板。
`csee.cls` 使用 LaTeX3（`expl3`）实现元数据、键值接口、题名、摘要与附录逻辑，
使用 CTEX 和标准 LaTeX 宏包完成中文排版、公式、图表及双栏输出。
本模板以提供的 Word 文件为依据，不声明符合期刊后续修订要求。

[English](README_en.md)

## 文件与编译

| 文件 | 用途 |
| --- | --- |
| `csee.cls` | 模板文档类 |
| `main.tex` | 可直接修改的完整示例 |
| `csee-doc.tex` | 参考 SUEPTeX 组织方式编写的独立 LaTeX 使用指南 |
| `build/csee-doc.pdf` | 编译后的使用指南，含接口示例、排错及 Word 核对记录 |
| `.latexmkrc` | 默认使用 XeLaTeX，产物写入 `build/` |
| `build/main.pdf` | 编译后的示例 PDF |
| `docs/20230420110546.doc` | 原始 Word 版式参考 |
| `.gitignore` | 编译产物、辅助文件与临时文件的 Git 忽略规则 |

本机已使用完整安装的 TeX Live 2026 验证，首选 XeLaTeX。在项目目录执行：

```sh
latexmk main.tex
latexmk csee-doc.tex
```

生成的 PDF 位于 `build/`，不纳入 Git。首次获取项目后需自行编译。
强制重新构建指南可执行 `latexmk -g csee-doc.tex`。

不使用 latexmk 时，连续运行两次：

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

第二种方式将 PDF 写到项目根目录。编辑器的编译引擎也应设置为 XeLaTeX，
并把 `csee.cls` 与主文件放在同一目录；不支持 pdfLaTeX。
论文也支持 LuaLaTeX；本指南按 XeLaTeX 编译。
模板依赖 CTEX、fontspec、geometry、amsmath、newtxmath、graphicx、booktabs、
caption、enumitem、siunitx、fancyhdr、cite 和 hyperref；示例额外使用 TikZ。

## 填写论文信息

在导言区用 `\cseesetup{...}` 设置字段，正文开始后依次调用 `\maketitle`、
`\makeabstract`。题名和作者信息通栏，摘要及正文双栏。

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

其他可选字段：`article-id`（文章编号）、`clc`（中图分类号）、
`document-code`（文献标志码）、`subject-code`（学科分类号）、
`funding`、`funding-en`（首页左栏无标号基金脚注）、
`short-title`（奇数页页眉）、`editor`（责任编辑）。空字段不显示内容。
中文单位的外括号、作者间全角逗号、中英文关键词分隔符需要自行填写。
多单位可用 `\\` 换行，用 `\textsuperscript{1}` 标注作者单位序号。
英文标题大小写及姓名拼写由作者控制，不自动转换。
分类号的字母与数字间距可写作 `TM\hspace{0.25em}73`。

## 正文、图表与参考文献

正文三级标题使用 `\section`、`\subsection`、`\subsubsection`，自动编号。
原 Word 的二级、三级、四级标题分别对应上述三个命令。
其中 `\section` 为小四黑体与 Arial，段前段后各 6 bp；
`\subsection` 为五号黑体与 Arial，段前段后为 0；二者换行均无悬挂缩进。
`enumerate` 列表自动产生 `1）`、`2）`。用 `\num{12345.87908}` 和
`\qty{50}{\hertz}` 统一数字分组与单位间距。
数学变量应使用数学模式；多行公式可使用 `equation` 与 `aligned`。
需按原稿要求将换行运算符保留在上一行末，模板不会自动选择数学换行位置。

在标准 `figure` 或 `table` 环境内使用：

```tex
\cseecaption{中文图题或表题}{English Caption}
\label{fig:example}
```

表题放在表格上方，图题放在图形下方。使用 `\ref{fig:example}` 引用。
跨栏图表使用 `figure*`、`table*`；它们的位置遵循 LaTeX 的双栏浮动规则。
表格推荐 `booktabs` 三线表，顶底线 0.75 bp、栏目线 0.5 bp。
`tabular`、`tabular*` 中默认采用六号、14 bp 行距。
图中中文须由绘图工具设置为六号宋体，英文为 Times New Roman；
外部图片内部的字号与线宽不会由模板自动修改。

`cseedefinition`、`cseetheorem` 分别提供“定义”和“定理”环境，可选参数为名称。
`cseeacknowledgements` 提供五号黑体居中的“致谢”标题。
致谢正文使用五号楷体、32.3 bp 行距，首行缩进 0.74 cm。
Windows 模式使用系统楷体 `KaiTi`；Fandol 模式使用 Fandol 楷体。
参考文献使用 `thebibliography`、`\bibitem` 和 `\cite`，引用为方括号上标。
请按首次引用顺序排列条目；模板不自动排序，也不自动生成文献内容。
示例保留原稿要求的 GB/T 7714—2005 著录形式及中英文对照方式，
没有用其他版本的 BibLaTeX 样式替换原稿规则。

## 附录与作者简介

```tex
\appendix
\section{补充推导} % 附录 A；图、表、公式分别从 A1 开始
% ...
\section{补充数据} % 附录 B；图、表、公式分别从 B1 开始

\begin{cseebiography}[portrait.jpg]{张三}
（1990—），男，博士，研究方向为电力系统；E-mail：\url{author@example.com}。
\end{cseebiography}
\cseeeditor
```

照片路径是可选参数，不填时仅显示文字。照片应预先裁成 **11:14**，
像素不少于 **260 × 330**；以此比例输入，输出尺寸为 **2.2 × 2.8 cm**。
模板保留照片比例，不拉伸或自动裁切。单个带照片的简介作为整体排版，不能跨页。

## 版式依据与差异

| 原稿要求 | 模板设置 |
| --- | --- |
| A4；上 3.2、下 2.5、左/右 2.0 cm | 使用文字明确要求的页面尺寸 |
| 双栏，栏间距 0.78 cm | 通栏题名，双栏摘要与正文 |
| 页眉距纸顶 2.0 cm | 首页中英文刊名；后续页外侧页码、偶数页刊名、奇数页短题名；无页脚文字 |
| 五号正文，首行缩进 0.74 cm | 宋体及 Times New Roman，10.5 bp |
| 每页 42 行 | 正文基线间距取版心高度的 1/42，约 16.20 bp |
| 二号中文题名，四号作者 | 黑体/Arial 22 bp，仿宋 14 bp |
| 英文题名小四加粗 | Times New Roman Bold 12 bp |
| 摘要、图表题、参考文献小五；行距 14 pt | 9 bp、14 bp 行距；图表题加粗 |
| 数学正文/上下标/次级上下标 10.5/6.5/4.5 pt | newtxmath，按对应 bp 尺寸设置 |
| 附录单独编号 | 图、表、公式按附录 A/B 分别重新计数 |

Word 的字号“pt”对应 PostScript 点，LaTeX 中使用 `bp` 保持物理尺寸。
原文件保存的上边距约为 **2.7 cm**，与文末文字要求 **3.2 cm** 不一致；
这里采用后者。Word 文档网格及每行 45 字（半栏 21 字）是网格排版设置，
LaTeX 使用其自身的断行算法；混排、公式、浮动体与标题占行不保证逐页逐行相同。
MathType 的旧符号字体与符号级别不能直接移植，数学部分采用 Times 风格的 newtxmath。
首页页眉采用双线，每条 0.48 bp、净间隔 0.48 bp；后续页横线为 0.72 bp。
页眉文字与横线按 Word 参考 PDF 的垂直位置校正，正文上边距仍为 3.2 cm。
附录标题为 9 bp 黑体与 Arial，段前后各 3 bp；参考文献标题段前后各 4 bp。
详见使用指南的核对记录。

默认 `fontset=auto`：检测到 SimSun 时使用宋体、黑体、楷体、仿宋、Times New Roman
和 Arial；此模式要求上述字体均已安装。其他系统自动使用 Fandol、TeX Gyre Termes
和 TeX Gyre Heros。也可显式指定：

```tex
\documentclass[fontset=fandol]{csee}
```

Fandol 便于跨平台编译，但与原稿指定的 Windows 字体字形不同。

## Git 管理

在项目根目录初始化仓库并提交：

```sh
git init
git add .
git status
git commit -m "Initial commit"
```

已有仓库可跳过 `git init`。提交前通过 `git status` 检查暂存内容。
应保留 `.tex`、`.cls`、`.latexmkrc`、README、原始 Word 文档以及论文使用的图片。
`.gitignore` 已忽略 `build/`、根目录下的 `main.pdf` 和 `csee-doc.pdf`、
LaTeX 辅助文件及编辑器临时文件；没有全局忽略 PDF，因此 PDF 插图仍可提交。
忽略规则不会移除已经被 Git 跟踪的文件。

## 构建与检查

当前目录不包含之前用于开发验证的 `tests/` 和 `tools/`，日常检查可直接构建：

```sh
latexmk main.tex
latexmk csee-doc.tex
```

检查 `build/main.log` 与 `build/csee-doc.log` 是否有错误、缺字、未定义引用
或 Overfull 提示，并查看生成的 PDF，尤其是长标题、奇偶页页眉、致谢、附录、
外部图片与复杂表格。编译通过不代表内容修改后的分页无需检查。
