import socket
import os
import sys

host = '0.0.0.0'
port = 3389

# 서버 소켓 오픈
# socket.AF_INET: 주소 종류 지정(IP) / socket.SOCK_STREAM: 통신 종류 지정(TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.SOL_SOCKET: 소켓 옵션
# SO_REUSEADDR: 현재 사용 중인 ip/ 포트번호를 재사용 할 수 있다.
# 커널이 소켓을 사용 하는 중에도 계속 해서 사용할 수 있다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server socket 에 ip와 port 를 붙여줌(bind)
server_socket.bind((host, port))

# 접속 준비 완료
server_socket.listen()

# echo program: 입력한 값을 메아리 치는 기능(그대로 다시 보냄)
print(' server start ')

# accept(): 클라이언트 접속 기다리며 대기
# 클라이언트가 접속하면 서버-클라이언트 1:1 통신이 가능한 작은 소켓(client_soc)을 만들어서 반환
# 접속한 클라이언트의 주소(addr)역시 반환
client_soc, addr = server_socket.accept()

print('connect client addr: ', addr)


# recv(메시지 크기) :소켓에서 크기만큼 읽는 함수
# 소켓에 읽을 데이터가 없으면 생길 때까지 대기함

def cpucheck():
    # cpu 사용량 계산
    cpu = str(os.popen('sar 1 1').readlines())
    A_ind = cpu.index('A')
    cpu = cpu[A_ind + 8:]
    cpu = cpu[66:-4]
    # print('--------------CPU--------------')
    # print('cpu usage : ',100-float(cpu),'%')
    # print('cpu free : ',float(cpu),'%')
    # print()
    return 100 - float(cpu), float(cpu)  # cpu 사용률,가용률


def memcheck():
    # 메모리 사용량 계산
    mem = str(os.popen('free -t -k').readlines())
    T_ind = mem.index('T')
    mem = mem[T_ind + 6:]
    mem_T = mem[:13]
    mem_sub = mem[14:]
    mem_U = mem_sub[:13]
    # print('-------------memory-------------')
    # print('memory usage : ',round(float(mem_U)/float(mem_T)*100,2),'%')
    # print('memory free : ',100-round(float(mem_U)/float(mem_T)*100,2),'%')
    # print()
    return round(float(mem_U) / float(mem_T) * 100, 2), 100 - round(float(mem_U) / float(mem_T) * 100, 2)  # 메모리 사용률,가용률


def diskcheck():
    # 디스크 파일 시스템 정보
    st = os.statvfs("/")

    # 총, 남은 디스크 용량 계산
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    free = st.f_bavail * st.f_frsize

    # print("disk total :" + str(total/1024/1024/1024)[0:5] + "GB")
    # print('--------------DISK--------------')
    # print("disk used : " + str(used/1024/1024/1024)[0:5] + "GB")
    # print("disk free : " + str(free/1024/1024/1024)[0:5] + "GB")
    # print()
    return str(used / 1024 / 1024 / 1024)[0:5], str(free / 1024 / 1024 / 1024)[0:5]  # 사용량,남은양


while True:

    data = client_soc.recv(1024)
    msg = data.decode()  # 읽은 데이터 디코딩
    print('recv msg: ', msg)
    if msg == "":
        break

    if msg == 'Status?':
        cpu_u, cpu_f = cpucheck()
        mem_u, mem_f = memcheck()
        disk_u, disk_f = diskcheck()
        cpu = '--------------CPU--------------\n' + 'cpu usage : ' + str(cpu_u) + '%\n' + 'cpu free : ' + str(
            cpu_f) + '%\n\n'
        mem = '-------------memory------------\n' + 'memory usage : ' + str(mem_u) + '%\n' + 'memory free : ' + str(
            mem_f) + '%\n\n'
        disk = '-------------DISK--------------\n' + 'disk usage : ' + str(disk_u) + 'GB\n' + 'disk free : ' + str(
            disk_f) + 'GB\n\n'

        msg = cpu + mem + disk

        client_soc.sendall(msg.encode(encoding='utf-8'))
        # 메세지 클라이언트로 보냄
server_socket.close()  # 사용한 서버 소켓 닫기
