import socket
import time

server_ip = '20.214.186.223'  # 위에서 설정한 서버 ip
server_port = 3389  # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))


def statuscheck():
    msg = 'Status?'
    socket.sendall(msg.encode(encoding='utf-8'))
    print(msg)


socket.settimeout(10)  # 서버의 응답을 기다리는 시간`

while True:

    statuscheck()  # 메세지 전송
    try:
        data = socket.recv(1024)  # 서버가  보낸 메시지를 클라이언트가 받음
    except TimeoutError as e:
        print(str(e))


    msg = data.decode()  # 읽은 데이터 디코딩
    print(msg)
    print()
    time.sleep(10)  # 메세지 보내는 주기 설정

socket.close()
