:: Recreates GisFilesList.txt
@echo off
dir /B *txt | find /V /I "GisFilesList.txt" > GisFilesList.txt
