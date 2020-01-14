pyinstaller -F probar_conexiones_de_salida.py
copy conexiones.txt dist

rmdir /S /Q __pycache__
rmdir /S /Q build
del *.spec