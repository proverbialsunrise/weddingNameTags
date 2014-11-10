#!/bin/bash


source /Users/dan/.bash_profile
for F in `find . -type f -name "*svg"`
do
    BASE=`basename $F .svg`
    echo $BASE
    /Applications/Inkscape.app/Contents/Resources/bin/inkscape --without-gui  \
    --file=$F               \
    --export-pdf=$BASE.pdf  \ 
done

#pdfjam *.pdf -o TableCards.pdf   PDFJAM seems to mess with the margins.  We'll need another solution.
