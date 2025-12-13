@echo off
chcp 65001 > nul
title Удаление Квантового Кликера
echo Удаление игры...
echo Удалить папку с сохранениями? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    rmdir /s /q "saves"
)
echo Игра удалена. Вы можете удалить эту папку вручную.
pause