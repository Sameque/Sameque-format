
@echo off
if [%1] == [] goto done
SET command=%1

if %command% == install goto :install
if %command% == teste goto :bas
goto end 
    :install 
        echo Instalando...
        pip install -e .["dev"]
    goto end
    :bas
        echo Testando...
        tests/ -v --cov=delivery
:end

:done
