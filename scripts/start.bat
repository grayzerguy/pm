@echo off
set IMAGE_NAME=pmapp
set CONTAINER_NAME=pmapp

docker build -t %IMAGE_NAME% .

docker ps -a --format "%%.Names" | findstr /R /C:"^%CONTAINER_NAME%$" >nul
if %ERRORLEVEL%==0 (
    docker rm -f %CONTAINER_NAME% >nul 2>&1
)

docker run -d --name %CONTAINER_NAME% -p 8000:8000 %IMAGE_NAME%

echo Container started at http://localhost:8000