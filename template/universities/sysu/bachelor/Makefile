MAIN = main
NAME = sysuthesis
PRE = pre
CLSFILES = $(NAME).cls
BSTFILES = $(NAME)-numerical.bst

SHELL = bash
LATEXMK = latexmk -xelatex
# VERSION = $(shell cat $(NAME).cls | egrep -o "\\ustcthesisversion{v[0-9.]+" \
# 	  | egrep -o "v[0-9.]+")
TEXMF = $(shell kpsewhich --var-value TEXMFHOME)

.PHONY : main cls doc clean all install distclean zip FORCE_MAKE help
.DEFAULT_GOAL := help

help: ## 显示本 Makefile 常用命令帮助
	@grep -E '^[a-zA-Z_-]+ :.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = " :.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

main : $(MAIN).pdf ## 编译论文正文 (main.pdf)

pre : $(PRE).pdf ## 编译答辩展示用ppt文档 (pre.pdf)

all : main pre doc ## 编译所有文档 (正文、答辩ppt、说明文档)

cls : $(CLSFILES) $(BSTFILES)

doc : $(NAME)-guide.pdf

$(MAIN).pdf : main.tex $(CLSFILES) $(BSTFILES) FORCE_MAKE
	$(LATEXMK) $<

$(PRE).pdf : pre.tex FORCE_MAKE
	$(LATEXMK) $<

$(NAME)-guide.pdf : $(NAME)-guide.tex FORCE_MAKE
	$(LATEXMK) $<

clean : FORCE_MAKE ## 清理编译生成的中间文件
	$(LATEXMK) -c main.tex pre.tex $(NAME)-guide.tex

cleanall : ## 清理所有生成的文件（包括 PDF）
	$(LATEXMK) -C main.tex pre.tex $(NAME)-guide.tex

install : cls doc
	mkdir -p $(TEXMF)/{doc,source,tex}/latex/$(NAME)
	mkdir -p $(TEXMF)/bibtex/bst/$(NAME)
	cp $(BSTFILES) $(TEXMF)/bibtex/bst/$(NAME)
	cp $(NAME).pdf $(TEXMF)/doc/latex/$(NAME)
	cp $(CLSFILES) $(TEXMF)/tex/latex/$(NAME)

zip : main pre doc
	ln -sf . $(NAME)
	zip -r ../$(NAME)-$(VERSION).zip $(NAME)/{*.md,LICENSE,\
	$(NAME)-guide.tex,$(NAME)-guide.pdf,$(NAME).cls,*.bst,*.bbx,*.cbx,figures,\
	main.tex,pre.tex,sysusetup.tex,chapters,bib,$(MAIN).pdf,$(PRE).pdf,\
	latexmkrc,Makefile}
	rm $(NAME)
