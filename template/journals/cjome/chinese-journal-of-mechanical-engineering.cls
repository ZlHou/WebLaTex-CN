\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{chinese-journal-of-mechanical-engineering}[LaTeX template for Chinese Journal of Mechanical Engineering]

\LoadClass{ctexart}

\newcommand{\doi}[1]{\def\CJOME@doi{#1}}
\newcommand{\abst}[1]{\def\CJOME@abstract{#1}}
\newcommand{\keyword}[1]{\def\CJOME@keyword{#1}}

\RequirePackage[linesnumbered, ruled]{algorithm2e}
\RequirePackage{amsmath}
\RequirePackage{authblk}
\RequirePackage[backend=biber, style=gb7714-2015, citestyle=gb7714-2015]{biblatex}
\RequirePackage{bm}
\RequirePackage{booktabs}
\RequirePackage{calc}
\RequirePackage{caption}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{float}
% Change to Times New Roman. See: https://tex.stackexchange.com/a/667009
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper, left=.77in, right=.77in, top=.85in, bottom=.85in]{geometry}
\RequirePackage{graphicx}
\RequirePackage[colorlinks=true, citecolor=magenta]{hyperref}
% See: https://tex.stackexchange.com/a/667009
\RequirePackage{mathptmx}
\RequirePackage{multicol}
% Add this to indent first paragraph of a section
\RequirePackage[indentafter]{titlesec}

% algorithm2e settings
\renewcommand{\algorithmcfname}{算法}
\SetKwInOut{KwIn}{输入}
\SetKwInOut{KwOut}{输出}

% CJK font settings
\setCJKmainfont{SimSun}[AutoFakeBold=1.3]
\setCJKsansfont{SimHei}
\setCJKfamilyfont{zhfs}{FangSong}

% fancyhdr settings
\fancypagestyle{firststyle}{
    \setlength{\headheight}{36pt}%
    \setlength{\topmargin}{-53.7pt}%
    \setlength{\headsep}{28pt}%
    \renewcommand{\headrulewidth}{.26pt}%
    \fancyhf{}%
    \fancyhead[L]{\small
        \begin{tabular}{l}%
            第**卷第**期 \\[.5em]
            2\ 0\ *\ *\ 年\ *\ 月
        \end{tabular}}%
    \fancyhead[C]{%
        \begin{tabular}{c}
            \Large 机\quad 械\quad 工\quad 程\quad 学\quad 报 \\[.34em]
            \large JOURNAL OF MECHANICAL ENGINEERING
        \end{tabular}}%
    \fancyhead[R]{\small
        \begin{tabular}{ll}%
            Vol.** & No.* \\[.5em]
            *** & 20**
        \end{tabular}}%
    \renewcommand{\headrule}{%
        \hbox to\headwidth{\leaders\hrule height \headrulewidth depth \headrulewidth\hfill}%
        \vskip \dimexpr 1pt-\baselineskip \relax
        \hbox to\headwidth{\leaders\hrule height \headrulewidth depth \headrulewidth\hfill}}%
    }
\fancypagestyle{fancy}{%
    % Should keep track of the previous setting
    \setlength{\headheight}{26pt}%
    \setlength{\headsep}{12pt}%
    \renewcommand{\headrulewidth}{.8pt}
    \fancyhf{}%
    \fancyhead[C]{\small\vspace{1pt} 机\quad 械\quad 工\quad 程\quad 学\quad 报}}
\pagestyle{fancy}

% Set title format and spacing
\titleformat*{\section}{\raggedright\Large\normalfont}
\titleformat*{\subsection}{\raggedright\normalsize\sffamily}
\titlespacing*{\section}{0pt}{1em}{1.2em}
\titlespacing*{\subsection}{0pt}{.6em}{.6em}

% Set figure/table caption format
\captionsetup{%
    labelsep=quad,
    font=normalsize
}

\setlist{%
    nosep, % Remove separation between items
    labelsep=0pt, % Remove space between label and item
    leftmargin=0pt, % Remove left margin of items
    itemindent=2\parindent % Add exact *one* indent, but wonder why should be double here
}

% See biblatex manual section 3.8.7: Bibliography Headings and Environments
\defbibheading{bibliography}{%
    \begin{center}
        \normalsize\sffamily 参\quad 考\quad 文\quad 献
    \end{center}
    \addcontentsline{toc}{section}{参考文献}}

% Set multi-column separation
\setlength{\columnsep}{2em}

% authblk stuff
% Reset defined title, authors, etc.
\def\InfoBundle{}
\def\EnInfoBundle{}

\renewcommand{\Authsep}{\quad}
\renewcommand{\Authand}{\quad}
\renewcommand{\Authands}{\quad}
\renewcommand{\affilsep}{0pt}

\makeatletter
\newcommand{\CJOME@maketitle}{%
    \begin{center}
        \begingroup\huge\sffamily\@title\endgroup
        \vskip 2.5em
        \begingroup\@author\endgroup
    \end{center}
    \vskip 1em
    \begingroup\small
        \noindent{\sffamily 摘要：}\CJOME@abstract\par
        \noindent{\sffamily 关键词：}\CJOME@keyword\par
        \noindent{\sffamily 中图分类号：}TP241.3
    \endgroup}

\newcommand{\CJOME@enmaketitle}{%
    \begin{center}
        \begingroup\Large\bfseries\@title\endgroup
        \vskip 1.25em
        \begingroup\@author\endgroup
    \end{center}
    \vskip .7em
    \begingroup\small
        \noindent{\bfseries Abstract：}\CJOME@abstract\par
        \noindent{\bfseries Key words：}\CJOME@keyword
    \endgroup}

\renewcommand{\maketitle}{%
    % DOI stuff
    % See: https://tex.stackexchange.com/a/830
    \renewcommand*{\thefootnote}{\fnsymbol{footnote}}
    \begingroup
        \noindent\bfseries DOI：\CJOME@doi
    \endgroup
    \vskip 2em
    % Special settings for Chinese auth/affil
    \renewcommand{\Authfont}{\fangsong\Large}
    \renewcommand\AB@affilsepx{\protect；\\\protect\Affilfont}
    % We suppose that both author and affil are defined
    \renewcommand\@author{\begingroup\AB@authlist\endgroup\\[\affilsep]\begingroup（\AB@affillist）\endgroup}
    % Chinese title and other stuff
    \InfoBundle
    \CJOME@maketitle
    \vskip 2.5em
    % Reset maketitle and authblk settings
    \renewcommand\AB@authlist{}
    \renewcommand\AB@affillist{}
    \renewcommand\AB@authors{}
    \renewcommand\AB@empty{}
    \setcounter{authors}{0}
    \setcounter{affil}{0}
    \renewcommand\AB@affilsep{\protect\Affilfont}
    \renewcommand\AB@affilsepx{\protect\\\protect\Affilfont}
    % Special settings for English auth/affil
    \renewcommand{\Authfont}{\large}
    \renewcommand\AB@affilsepx{\protect;\\\protect\Affilfont}
    \renewcommand\@author{\begingroup\AB@authlist\endgroup\\[\affilsep]\begingroup(\AB@affillist)\endgroup}
    % English title and other stuff
    \EnInfoBundle
    \CJOME@enmaketitle
    % Reset global settings
    % See: https://tex.stackexchange.com/a/830
    \renewcommand*{\thefootnote}{\arabic{footnote}}
    \setcounter{footnote}{0}}
\makeatother
