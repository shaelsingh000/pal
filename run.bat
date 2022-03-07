@echo off
echo Preparing server for Welcome Pal webapp developed by shael at http://127.0.0.1:8000/
shael\Scripts\activate && cd example && python manage.py runserver
pause
