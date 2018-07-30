#!/bin/bash
rm -rf wheels
./wheels.py
cd _wheels
for file in *.tex; do
    xelatex $file
done
for file in *.pdf; do
    convert $file $(basename $file).png
done
rm *.aux *.tex *.log
cd ..