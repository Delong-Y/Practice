import sys
import traceback
import socket

def conn_tcp():
    target_host = '127.0.0.1'
    target_port = 9999
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host,target_port))

        sent_bytes = "hello!".encode('utf-8')
        client.send(sent_bytes)
        response = client.recv(4096)
        print(response)
    except Exception as e:
        print(e)
    finally:
        client.close()

def conn_udp():
    target_host = "127.0.0.1"
    target_port = 80

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sent_bytes = "hello!".encode('utf-8')
    client.sendto(sent_bytes, (target_host, target_port))
    data, addr = client.recvfrom(4096)

    print(data)


def client_sender(buffer):
    target_host = '127.0.0.1'
    target_port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target_host, target_port))

        if len(buffer):
            client.send(buffer.encode('utf-8'))

        while True:
            recv_len = 1
            response = b''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(response)
                response += data
                if recv_len < 4096:
                    break

            print(response.decode('utf-8'))

            buffer = input()
            buffer += "\n"
            client.send(buffer.encode('utf-8'))
    except:
        traceback.print_exc()
        client.close()

def main():
    buffer = 'first hello!'
    client_sender(buffer)


if __name__ == '__main__':
    main()
    sys.exit(0)
