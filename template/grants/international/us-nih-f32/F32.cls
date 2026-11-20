%% F32.cls

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{F32}

\LoadClass[11pt]{article}

%\RequirePackage{draftwatermark}  % delete this in your document!
%\SetWatermarkText{Sample}    % delete this in your document!
%\SetWatermarkLightness{0.9}  % delete this in your document!

\RequirePackage[top=0.5in, bottom=0.5in, left=0.5in, right=0.5in]{geometry}
\RequirePackage{helvet}
\RequirePackage{url} % hypderref?
\RequirePackage{graphicx}

\renewcommand{\familydefault}{\sfdefault}
\pagestyle{empty}

% Fancy page-width tables
\RequirePackage{tabularx}

% Use a package for framed boxes
\RequirePackage{mdframed}

\RequirePackage[T1]{fontenc}
\RequirePackage{amssymb}


\RequirePackage{setspace}
\RequirePackage{microtype}

\RequirePackage{amsfonts}
\RequirePackage{amsmath}

\RequirePackage{floatrow}

\RequirePackage[normalem]{ulem} % for nci.bst

\RequirePackage{sidecap}
\RequirePackage[abs]{overpic}
\RequirePackage{wrapfig}


\RequirePackage{hyperref}
\hypersetup{colorlinks=true, urlcolor=black, citecolor=black, linkcolor=black}

\RequirePackage[numbers,sort&compress]{natbib}

\newcommand{\doi}[1]{\href{http://dx.doi.org/#1}{doi:#1}}

\newcommand{\ac}[1]{{\sc \lowercase{#1}}}

\renewcommand{\baselinestretch}{.93}

\RequirePackage{wrapfig}

\makeatletter

\newcommand{\captionfonts}{\footnotesize}

\makeatletter  % Allow the use of @ in command names
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{{\captionfonts #1: #2}}%
  \ifdim \wd\@tempboxa >\hsize
    {\captionfonts #1. #2\par}
  \else
    \hbox to\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
\makeatother

\renewcommand{\figurename}{{\bf Figure}}

\setlength{\abovecaptionskip}{-5pt}

\makeatother

\renewcommand{\refname}{Bibliography and References Cited}

\setlength{\parindent}{0pt} % Don't indent first line
%\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex} % Add some space between paragraphs
\setlength{\parskip}{0.8ex} % Add some space between paragraphs

%%%%%%%%%%%%%%%%%%%%% c-bun's additions
\newcommand{\comment}[1]{\textit{\textcolor{red}{#1}}}
\RequirePackage{booktabs}
\RequirePackage{upgreek} % allows nonitalic greek letters
\RequirePackage{titlesec}
\RequirePackage{courier}
\titlespacing\subsubsection{0pt}{6pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt} % allows use of sections without all that extra spacing.
\renewcommand{\tablename}{{\bf Table}}
%\RequirePackage{lineno} % uncomment for line numbers. You're welcome.
%\linenumbers % uncomment for line numbers. You're welcome.
%%%%%%%%%%%%%%%%%%%%% end c-bun's additions
