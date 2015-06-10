#!/bin/bash

csv2json attendingGuestDB.csv attendingGuestDB.json

python makeNamePlates.py

cd processed
rm *.pdf

for F in `find . -type f -name "*svg"`
do
    BASE=`pwd`/`basename $F .svg`
    FILE=$BASE.svg
    PDFFILE=$BASE.pdf
    /Applications/Inkscape.app/Contents/Resources/script -z -f $FILE -A $PDFFILE
    echo "Created "$PDFFILE
done

cd ..

PDFconcat -o NameTagsAlphabetized.pdf processed/*.pdf
mv NameTagsAlphabetized.pdf processed/
