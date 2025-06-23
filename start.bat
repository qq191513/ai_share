@echo off
title Aqitanai Project Server

:: Change directory to the script's own location
cd /d %~dp0

echo ==========================================================
echo  Starting local server for Aqitanai Project
echo  Project directory: %cd%
echo ==========================================================
echo.
echo  Opening browser at http://localhost:8000 ...
start "" http://localhost:8000
echo.
echo  Starting Python web server on port 8000...
echo  (Please keep this window open to keep the server running)
echo.
D:/ProgramData/anaconda3/envs/get_html/python -m http.server 8000 