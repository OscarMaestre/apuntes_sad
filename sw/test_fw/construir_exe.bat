pyinstaller -F probar_conexiones.py
copy conexiones.txt dist

rmdir /S /Q __pycache__
rmdir /S /Q build
del *.spec