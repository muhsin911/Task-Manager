@echo off
REM Usage:
REM initiate.bat           -- Start docker-compose
REM initiate.bat -b        -- Build Docker image and start docker-compose
REM initiate.bat -d        -- Stop and remove containers
REM initiate.bat -r        -- Restart containers

SETLOCAL ENABLEEXTENSIONS
SET ARG=%1

IF "%ARG%"=="-b" (
    echo Building Docker image and starting containers...
    docker-compose build
    docker-compose up -d
) ELSE IF "%ARG%"=="-d" (
    echo Stopping and removing containers...
    docker-compose down
) ELSE IF "%ARG%"=="-r" (
    echo Restarting containers...
    docker-compose restart
) ELSE (
    echo Starting containers...
    docker-compose up
)
ENDLOCAL
