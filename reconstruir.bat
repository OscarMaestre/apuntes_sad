call make html
copiar.py
call make latex
cd build\latex
call pdflatex ApuntesDeLenguajesDeMarcas.tex
call pdflatex ApuntesDeLenguajesDeMarcas.tex
cd ..
cd ..
copy build\latex\*.pdf pdf
git add docs
call git commit -a --allow-empty-message -m ''
call git push

