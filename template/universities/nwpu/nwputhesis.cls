\NeedsTeXFormat{LaTeX2e}[2022/06/01]
\ProvidesClass{nwputhesis}
[2026/03/25 v2.3.0 nwputhesis]
\input{infra/options.def}
\RequirePackage{fix-cm}                                    % 允许 CM 数学字体连续缩放
\LoadClass[a4paper]{book}                                   % openright 默认：硕博双面从奇数页起排
\ExplSyntaxOn
\nwpu_if_bachelor:T
  {
    \nwpu_if_printmode:TF
      { \@twosidetrue }                                           % 双面印刷：各部分从奇数页起排
      { \@twosidefalse \@mparswitchfalse }                        % 默认单面印刷
  }
\ExplSyntaxOff
\input{infra/format-constants.def}
\input{infra/core.def}
\input{infra/fonts.def}
\input{infra/layout.def}
%%-----------------------------------------------------------------------------%
%% hyperref 应尽可能靠后加载，但需早于使用其命令的 localization.def
%%-----------------------------------------------------------------------------%
\RequirePackage[                                            % 超链接设置
    unicode=true,                                           % 允许 Unicode
    colorlinks=false,                                       % 不改变文字颜色
    pdfborder={0 0 0},                                      % 不显示边框
    bookmarks=true]{hyperref}                               % 显示书签页
\hypersetup{                                                % Acrobat 默认设置
    pdftoolbar=true,                                        % 显示工具栏
    pdfmenubar=true,                                        % 显示菜单栏
    pdffitwindow=true,                                      % 缩放以适应窗口大小
    pdfstartview={FitH},                                    % 适合窗口宽度
    pdfnewwindow=true,                                      % 以新窗口打开链接
    hypertexnames=false,                                    % 避免重复页锚点命名
}                                                           %
\special{pdf:minorversion 7}                                % 允许包含 PDF 1.7 页面
\providecommand\HyperLocalCurrentHref{}
\RequirePackage{bookmark}                                   %
\pdfstringdefDisableCommands{%                              % 解决 "Token not allowed in a PDF string" 警告
\def\!{}%
\def\quad{ }%
\def\qquad{  }%
}
\input{infra/localization.def}
\input{infra/metadata.def}
\input{infra/title.def}
\input{infra/abstract.def}
\input{infra/bibliography.def}
\input{infra/appendix.def}
\input{infra/backmatter.def}
\ExplSyntaxOn
\bool_set_true:N \l__nwpu_class_loaded_bool
\ExplSyntaxOff
