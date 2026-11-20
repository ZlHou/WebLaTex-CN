all: nih-r01.pdf

%.pdf: %.tex
	pdflatex $*.tex
	if ( grep -q citation $*.aux ) ; then \
		bibtex $* ; \
		pdflatex $*.tex ; \
	fi
	pdflatex $*.tex

clean:
	rm -f *.dvi *.bbl *.aux *.blg *.log *.ps

