Python 실행 파일 만들기

1. pyinstaller 설치
   C:\Apps\Python\Python311\Scripts\pip install --proxy http://[id:passwrd]@rb-proxy-apac.bosch.com:8080 pyinstaller
   pip upgrade 
   C:\Apps\Python\Python311\python.exe -m pip install --proxy http://[id:passwrd]@rb-proxy-apac.bosch.com:8080 --upgrade pip
2. 실행파일 만들기
   Cmd : pyinstaller -F [python file]
    Ex : pyinstaller -F touch_dcm.py
