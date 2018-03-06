set DIRECTORIO_TEMP=temp
set COMPRESOR="c:\Program Files\7-Zip\7z.exe"
rmdir /S /q %DIRECTORIO_TEMP%
mkdir temp
copy pyvalidator.py %DIRECTORIO_TEMP%
cd %DIRECTORIO_TEMP%
@REM el --noconfirm es para que no pregunte
pyinstaller --noconfirm pyvalidator.py

%COMPRESOR% a pyvalidator.zip dist/pyvalidator

copy pyvalidator.zip .. /Y

cd ..
rmdir /S /q %DIRECTORIO_TEMP%