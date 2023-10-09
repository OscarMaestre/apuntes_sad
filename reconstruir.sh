#!/bin/bash

make html
rm -rf docs/*
cp -r build/html/* docs
cp .nojekyll docs/
make latexpdf
git add docs
git commit -a -m ""
git push
