%% Unofficial template based on 20230420110546.doc.
%% Compile with XeLaTeX or LuaLaTeX. Metadata and layout logic use expl3.
\NeedsTeXFormat{LaTeX2e}[2022-06-01]
\ProvidesExplClass{csee}{2026-10-08}{0.1.0}{Proceedings of the CSEE template}
\RequirePackage{l3keys2e}
\msg_new:nnn { csee } { engine }
  { Please~compile~this~document~with~XeLaTeX~or~LuaLaTeX. }
\sys_if_engine_pdftex:T { \msg_fatal:nn { csee } { engine } }
\tl_new:N \g__csee_fontset_tl
\keys_define:nn { csee / class }
  {
    fontset .choice:,
    fontset / auto .code:n = { \tl_gset:Nn \g__csee_fontset_tl { auto } },
    fontset / windows .code:n = { \tl_gset:Nn \g__csee_fontset_tl { windows } },
    fontset / fandol .code:n = { \tl_gset:Nn \g__csee_fontset_tl { fandol } },
    fontset .initial:n = auto,
  }
\ProcessKeysOptions { csee / class }
\PassOptionsToPackage{no-math}{fontspec}
\LoadClass[a4paper,twoside,zihao=5,fontset=none,scheme=plain]{ctexart}
\RequirePackage{geometry}
\RequirePackage{amsmath}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{caption}
\RequirePackage{enumitem}
\RequirePackage{siunitx}
\RequirePackage{fancyhdr}
\RequirePackage[superscript]{cite}
\RequirePackage{hyperref}
\hypersetup{hidelinks,bookmarksnumbered=true,unicode=true}
\cs_set_protected:Npn \@citess #1 { \textsuperscript{[#1]} }

% Word sizes are PostScript points (bp), rather than TeX points (pt).
\tl_if_eq:NnT \g__csee_fontset_tl { auto }
  {
    \IfFontExistsTF{SimSun}
      { \tl_gset:Nn \g__csee_fontset_tl { windows } }
      { \tl_gset:Nn \g__csee_fontset_tl { fandol } }
  }
\tl_if_eq:NnTF \g__csee_fontset_tl { windows }
  {
    \setCJKmainfont{SimSun}[AutoFakeBold=2.5,ItalicFont=KaiTi]
    \setCJKsansfont{SimHei}[BoldFont=SimHei]
    \setCJKmonofont{FangSong}
    \setCJKfamilyfont{zhsong}{SimSun}[AutoFakeBold=2.5]
    \setCJKfamilyfont{zhhei}{SimHei}[BoldFont=SimHei]
    \setCJKfamilyfont{zhkai}{KaiTi}
    \setCJKfamilyfont{zhfs}{FangSong}
    \setCJKfamilyfont{cseeack}{KaiTi}
    \newfontfamily\cseeacklatin{KaiTi}
    \setmainfont{Times~New~Roman}
    \setsansfont{Arial}
  }
  {
    \setCJKmainfont{FandolSong-Regular.otf}
      [BoldFont=FandolSong-Bold.otf,ItalicFont=FandolKai-Regular.otf]
    \setCJKsansfont{FandolHei-Regular.otf}[BoldFont=FandolHei-Bold.otf]
    \setCJKmonofont{FandolFang-Regular.otf}
    \setCJKfamilyfont{zhsong}{FandolSong-Regular.otf}[BoldFont=FandolSong-Bold.otf]
    \setCJKfamilyfont{zhhei}{FandolHei-Regular.otf}[BoldFont=FandolHei-Bold.otf]
    \setCJKfamilyfont{zhkai}{FandolKai-Regular.otf}
    \setCJKfamilyfont{zhfs}{FandolFang-Regular.otf}
    \setCJKfamilyfont{cseeack}{FandolKai-Regular.otf}
    \newfontfamily\cseeacklatin{FandolKai-Regular.otf}
    \setmainfont{TeX~Gyre~Termes}
    \setsansfont{TeX~Gyre~Heros}
  }
% Load after the text fonts: newtxmath captures the current roman family.
\RequirePackage[noOT1]{newtxmath}
\DeclareMathAlphabet{\mathsf}{TU}{\sfdefault}{m}{n}
\SetMathAlphabet{\mathsf}{bold}{TU}{\sfdefault}{b}{n}
\DeclareRobustCommand\songti{\CJKfamily{zhsong}}
\DeclareRobustCommand\heiti{\CJKfamily{zhhei}}
\DeclareRobustCommand\kaishu{\CJKfamily{zhkai}}
\DeclareRobustCommand\fangsong{\CJKfamily{zhfs}}
\sys_if_engine_xetex:T { \xeCJKsetup{CheckSingle=true} }
\sys_if_engine_luatex:T { \ltjsetparameter{jcharwidowpenalty=10000} }
\geometry{a4paper,top=3.2cm,bottom=2.5cm,left=2cm,right=2cm,
  headheight=28bp,headsep=6bp,footskip=6bp}
% Header top is 2 cm from the paper edge, independent of the body margin.
\setlength\headsep{\dimexpr 1.2cm-\headheight\relax}
\setlength\columnsep{0.78cm}
\dim_new:N \g__csee_body_baseline_dim
\dim_gset:Nn \g__csee_body_baseline_dim { \textheight / 42 }
\cs_set_protected:Npn \normalsize
  {
    \@setfontsize\normalsize{10.5bp}{\g__csee_body_baseline_dim}
    \abovedisplayskip=6bp~plus~2bp~minus~2bp
    \belowdisplayskip=6bp~plus~2bp~minus~2bp
    \abovedisplayshortskip=3bp~plus~2bp
    \belowdisplayshortskip=3bp~plus~2bp
  }
\cs_set_protected:Npn \small { \@setfontsize\small{9bp}{14bp} }
\cs_set_protected:Npn \footnotesize { \@setfontsize\footnotesize{7.5bp}{12bp} }
\DeclareMathSizes{10.5bp}{10.5bp}{6.5bp}{4.5bp}
\normalsize
\setlength\parindent{0.74cm}
\setlength\parskip{0pt}
\setlength\emergencystretch{1em}
\linespread{1}
\raggedbottom
\setcounter{secnumdepth}{3}
\ctexset{
  section = {
    format=\sffamily\heiti\fontsize{12bp}{\g__csee_body_baseline_dim}\selectfont,
    name={},number=\arabic{section},aftername=\hspace{1em},
    beforeskip=6bp,afterskip=6bp,indent=0pt,hang=false,afterindent=true,
  },
  subsection = {
    format=\sffamily\heiti\fontsize{10.5bp}{\g__csee_body_baseline_dim}\selectfont,
    name={},aftername=\hspace{1em},beforeskip=0pt,afterskip=0pt,
    indent=0pt,hang=false,afterindent=true,
  },
  subsubsection = {
    format=\rmfamily\songti\fontsize{10.5bp}{\g__csee_body_baseline_dim}\selectfont,
    name={},aftername=\hspace{1em},beforeskip=0pt,afterskip=0pt,
    indent=0pt,hang=false,afterindent=true,
  },
}
\setlist[enumerate]{label=\arabic*）,leftmargin=0.74cm,labelsep=0pt,
  itemindent=0pt,topsep=0pt,itemsep=0pt,parsep=0pt,partopsep=0pt}
\sisetup{group-separator={\hspace{0.25em}},group-minimum-digits=4,
  group-digits=all,number-unit-product={\nobreak\hspace{0.25em}}}
\setlength\heavyrulewidth{0.75bp}
\setlength\lightrulewidth{0.5bp}
\setlength\cmidrulewidth{0.5bp}
\setlength\aboverulesep{0pt}
\setlength\belowrulesep{0pt}
\setlength\textfloatsep{6bp~plus~2bp~minus~2bp}
\setlength\intextsep{3bp~plus~2bp~minus~1bp}
\AddToHook{env/tabular/begin}{\fontsize{7.5bp}{14bp}\selectfont}
\AddToHook{env/tabular*/begin}{\fontsize{7.5bp}{14bp}\selectfont}
\DeclareCaptionFont{csee}{\rmfamily\heiti\bfseries\fontsize{9bp}{14bp}\selectfont}
\captionsetup{font=csee,labelsep=quad,justification=centering,
  singlelinecheck=false,skip=3bp}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}
\renewcommand\figurename{图}
\renewcommand\tablename{表}
\NewDocumentCommand \cseecaption { m m }
  {
    \caption[#1]{#1\\
        \str_if_eq:eeTF { \@captype } { figure } { Fig. } { Tab. }
        \nobreakspace\use:c { the\@captype }\quad #2
    }
  }

% All paper metadata is stored in an expl3 property list.
\prop_new:N \g__csee_info_prop
\clist_map_inline:nn
  { title,title-en,authors,authors-en,affiliations,affiliations-en,
    abstract,abstract-en,keywords,keywords-en,article-id,clc,
    document-code,subject-code,funding,funding-en,short-title,editor }
  {
    \prop_gput:Nnn \g__csee_info_prop {#1} { }
    \keys_define:nn { csee / info }
      { #1 .code:n = { \prop_gput:Nnn \g__csee_info_prop {#1} {##1} } }
  }
\NewDocumentCommand \cseesetup { m } { \keys_set:nn { csee / info } {#1} }
\cs_new:Npn \__csee_info:n #1 { \prop_item:Nn \g__csee_info_prop {#1} }
\prg_new_conditional:Npnn \__csee_if_info:n #1 { T,F,TF }
  {
    \exp_args:Ne \tl_if_blank:nTF { \__csee_info:n {#1} }
      { \prg_return_false: } { \prg_return_true: }
  }
\cs_new_protected:Npn \__csee_title_line:nnn #1#2#3
  {
    \__csee_if_info:nT {#1}
      { \group_begin: #2 \__csee_info:n {#1}\par \group_end: \vskip #3 }
  }
\cs_new_protected:Npn \__csee_classification:
  {
    \group_begin:
      \raggedright\rmfamily\heiti\fontsize{9bp}{14bp}\selectfont
      \clist_map_inline:nn
        { article-id/文章编号,clc/中图分类号,document-code/文献标志码,subject-code/学科分类号 }
        { \__csee_classification_item:w ##1\q_stop }
      \par
    \group_end:
  }
\cs_new_protected:Npn \__csee_classification_item:w #1/#2\q_stop
  { \__csee_if_info:nT {#1} { #2：\__csee_info:n {#1}\hspace{4em} } }
\cs_new_protected:Npn \__csee_title:
  {
    \__csee_classification:
    \vskip 12bp
    \group_begin:
      \centering\setlength\parindent{0pt}
      \__csee_title_line:nnn { title }
        { \sffamily\heiti\fontsize{22bp}{30bp}\selectfont } {6bp}
      \__csee_title_line:nnn { authors }
        { \rmfamily\fangsong\fontsize{14bp}{\g__csee_body_baseline_dim}\selectfont } {3bp}
      \__csee_title_line:nnn { affiliations }
        { \rmfamily\kaishu\fontsize{10.5bp}{\g__csee_body_baseline_dim}\selectfont }
        {\g__csee_body_baseline_dim}
      \__csee_title_line:nnn { title-en }
        { \rmfamily\bfseries\fontsize{12bp}{\g__csee_body_baseline_dim}\selectfont } {3bp}
      \__csee_title_line:nnn { authors-en }
        { \rmfamily\fontsize{10.5bp}{\g__csee_body_baseline_dim}\selectfont } {3bp}
      \__csee_title_line:nnn { affiliations-en }
        { \rmfamily\fontsize{9bp}{\g__csee_body_baseline_dim}\selectfont } {12bp}
    \group_end:
  }
\cs_new_protected:Npn \__csee_abstract_item:nnn #1#2#3
  {
    \__csee_if_info:nT {#1}
      { \vskip #3 \noindent {\bfseries #2}\__csee_info:n {#1}\par }
  }
\NewDocumentCommand \makeabstract { }
  {
    \group_begin:
      \small\songti\rmfamily\setlength\parindent{0pt}
      \__csee_abstract_item:nnn { abstract-en } { ABSTRACT:~ } {0pt}
      \__csee_abstract_item:nnn { keywords-en } { KEY~WORDS:~ } {6bp}
      \__csee_abstract_item:nnn { abstract } { \heiti 摘要： } {6bp}
      \__csee_abstract_item:nnn { keywords } { \heiti 关键词： } {6bp}
    \group_end:
  }
\cs_new_protected:Npn \__csee_funding:
  {
    \group_begin:
      \cs_set:Npn \thefootnote { }
      \cs_set:Npn \@makefnmark { }
      \cs_set_protected:Npn \@makefntext ##1 { \parindent=0.63cm \noindent ##1 }
      \begin{NoHyper}\footnotetext{
        \__csee_if_info:nT { funding }
          { \hspace*{0.63cm}基金项目：\__csee_info:n {funding}\par }
        \__csee_if_info:nT { funding-en }
          { \hspace*{0.63cm}\__csee_info:n {funding-en}\par }
      }\end{NoHyper}
    \group_end:
  }
\bool_new:N \g__csee_title_made_bool
\msg_new:nnn { csee } { title-twice } { The~title~has~already~been~typeset. }
\msg_new:nnn { csee } { missing-title } { Please~set~the~title~with~cseesetup. }
\RenewDocumentCommand \maketitle { }
  {
    \bool_if:NTF \g__csee_title_made_bool
      { \msg_error:nn { csee } { title-twice } }
      {
        \__csee_if_info:nF {title} { \msg_error:nn { csee } { missing-title } }
        \bool_gset_true:N \g__csee_title_made_bool
        \twocolumn[\__csee_title:]
        \thispagestyle{cseefirst}
        \__csee_if_info:nTF {funding}
          { \__csee_funding: }
          { \__csee_if_info:nT {funding-en} { \__csee_funding: } }
      }
  }
\cs_new_protected:Npn \__csee_header_font: { \small\songti\rmfamily }
\cs_new:Npn \__csee_journal: { 中\quad 国\quad 电\quad 机\quad 工\quad 程\quad 学\quad 报 }
% The 28 bp header box is shared by both page styles. Lift its contents to
% the baselines measured in the Word PDF without moving the text area.
\cs_new_protected:Npn \__csee_header_raise:nn #1#2
  { \raisebox{#1}[0pt][0pt]{\__csee_header_font: #2} }
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\__csee_header_raise:nn{14.089bp}{\thepage}}
\fancyhead[CE]{\__csee_header_raise:nn{14.089bp}{\__csee_journal:}}
\fancyhead[CO]{\__csee_header_raise:nn{14.089bp}{\__csee_info:n {short-title}}}
\renewcommand\headrule{
  \kern-15.349bp\hrule height0.72bp width\headwidth\kern14.629bp
}
\fancypagestyle{cseefirst}{
  \fancyhf{}
  \fancyhead[C]{
    \rlap{\makebox[0pt]{\__csee_header_raise:nn{14.209bp}{\__csee_journal:}}}
    \makebox[0pt]{\__csee_header_raise:nn{3.049bp}{Proceedings~of~the~CSEE}}
  }
  \fancyhead[R]{\__csee_header_raise:nn{3.049bp}{\thepage}}
  \renewcommand\headrule{
    \kern-5.029bp\hrule height0.48bp width\headwidth
    \kern0.48bp\hrule height0.48bp width\headwidth\kern3.589bp
  }
}
\AddToHook{begindocument/end}{
  \pdfstringdefDisableCommands{\def\textsuperscript#1{#1}\def\\{\space}}
  \prop_get:NnN \g__csee_info_prop {authors} \l_tmpa_tl
  \tl_replace_all:Nnn \l_tmpa_tl {\textsuperscript} {\use_none:n}
  \hypersetup{pdftitle={\__csee_info:n {title}},pdfauthor={\l_tmpa_tl}}
}

% Manual references preserve the reference document's 2005 style exactly.
\renewcommand\refname{参考文献}
\RenewDocumentEnvironment{thebibliography}{m}
  {
    \ctexset{section={beforeskip=4bp,afterskip=4bp}}
    \section*{参考文献}
    \small\songti\rmfamily
    \list{[\arabic{enumiv}]}{
      \setlength\leftmargin{0.63cm}\setlength\labelwidth{0.45cm}
      \setlength\labelsep{0.18cm}\setlength\itemsep{0pt}
      \setlength\parsep{0pt}\setlength\topsep{0pt}
      \usecounter{enumiv}
    }
    \sloppy\clubpenalty=4000\widowpenalty=4000
  }
  { \endlist }
\NewDocumentEnvironment{cseeacknowledgements}{}
  {
    \par\addvspace{6bp}
    \group_begin:
      \centering\rmfamily\heiti
      \fontsize{10.5bp}{\g__csee_body_baseline_dim}\selectfont
      \noindent 致\hspace{1em}谢\par
    \group_end:
    \nobreak\nointerlineskip\vskip 16bp
    % Five-point-size KaiTi text with the sample's two-grid-line leading.
    \cseeacklatin\CJKfamily{cseeack}
    \fontsize{10.5bp}{32.3bp}\selectfont
    \setlength\parindent{0.74cm}\setlength\parskip{0pt}
    \@afterindenttrue\@afterheading\ignorespaces
  }
  { \par }
\newcounter{cseedefinition}
\newcounter{cseetheorem}
\NewDocumentEnvironment{cseedefinition}{o}
  {
    \par\refstepcounter{cseedefinition}\noindent
    {\heiti\bfseries 定义\,\thecseedefinition\IfValueT{#1}{（#1）}}\quad\ignorespaces
  } { \par }
\NewDocumentEnvironment{cseetheorem}{o}
  {
    \par\refstepcounter{cseetheorem}\noindent
    {\heiti\bfseries 定理\,\thecseetheorem\IfValueT{#1}{（#1）}}\quad\ignorespaces
  } { \par }
\AddToHook{cmd/appendix/after}{
  \ctexset{section={name={附录\space,},number=\Alph{section},
    format=\sffamily\heiti\fontsize{9bp}{14bp}\selectfont,
    beforeskip=3bp,afterskip=3bp}}
  \counterwithin*{figure}{section}
  \counterwithin*{table}{section}
  \counterwithin*{equation}{section}
  \renewcommand\thefigure{\Alph{section}\arabic{figure}}
  \renewcommand\thetable{\Alph{section}\arabic{table}}
  \renewcommand\theequation{\Alph{section}\arabic{equation}}
  \small
}
\NewDocumentEnvironment{cseebiography}{O{} m +b}
  {
    \par\addvspace{6bp}
    \group_begin:
      \small\songti\rmfamily\setlength\parindent{0.63cm}
      \tl_if_blank:nTF {#1}
        { \noindent\hspace*{0.63cm}{\heiti #2}#3\par }
        {
          \noindent
          \begin{minipage}[t]{2.2cm}
            \vspace{0pt}\includegraphics[width=2.2cm,height=2.8cm,keepaspectratio]{#1}
          \end{minipage}\hspace{0.15cm}
          \begin{minipage}[t]{\dimexpr\linewidth-2.35cm\relax}
            \vspace{0pt}\small\noindent {\heiti #2}#3
          \end{minipage}\par
        }
    \group_end:
  } { }
\NewDocumentCommand \cseeeditor { }
  {
    \__csee_if_info:nT {editor}
      {
        \par\addvspace{6bp}
        \group_begin:\raggedleft\normalsize
          （{\heiti 责任编辑}\quad {\kaishu\__csee_info:n {editor}}）\par
        \group_end:
      }
  }
\endinput
