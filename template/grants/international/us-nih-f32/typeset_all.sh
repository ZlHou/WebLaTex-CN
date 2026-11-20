#!/bin/bash
for texfile in *.tex
do
  xelatex $texfile
done

for auxfile in *.aux
do
    bibtex `basename $auxfile .aux`
done

for texfile in *.tex
do
  xelatex $texfile
  xelatex $texfile
done

rm ./*.out
rm ./*.aux
rm ./*.bbl
rm ./*.blg
rm ./*.log
