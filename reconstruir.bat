call make html
copiar.py
call make latex
cd build\latex
call pdflatex ApuntesdeSeguridadyaltadisponibilidad.tex
call pdflatex ApuntesdeSeguridadyaltadisponibilidad.tex
cd ..
cd ..
copy build\latex\*.pdf pdf
git add docs
call git commit -a --allow-empty-message -m ''
call git push

