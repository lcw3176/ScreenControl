# ScreenControl

###client.py
* 서버와 연결되면 서버로 화면 전송
* 컨트롤 쓰레드 생성, 서버의 마우스나 키보드 입력을 처리

###server.py
* tkinter가 활용된 서버 파일
* tkiinter Canvas에 이미지를 올리는 작업이 느림, 프레임 저하
* 원격 제어를 하기엔 너무 끊김

###server2.py
* server.py의 개선판
* wxpython을 활용함
* 프레임이 상당히 오름, 원격 제어가 가능한 수준이 됨
