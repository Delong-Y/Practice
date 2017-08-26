import codecs
import getopt
import locale
import socket
import subprocess
import sys
import threading
import traceback


listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("ONT Net Tool")
    print("Usage: ont.py -t target_host -p port")
    print("-l --listen               - listen on [target_host]:[port] for incoming connections")
    print("-e --execute\=file_to_run - execute the given file upon receiving a connection")
    print("-c --command              - initialize a command shell")
    print("-u --upload\=destination  - upon receiving connection upload a file and write to [destination]")
    print("")
    print("")
    sys.exit(0)


def main():
    global listen
    global execute
    global upload
    global command
    global target
    global upload_destination
    global port

    if len(sys.argv[1:]) == 0:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
            [help, listen, execute, target, port, command, upload])
    except:
        traceback.print_exc()
        usage()

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--command'):
            command = True
        elif o in ('-u', '--upload'):
            upload = True
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'

    if not listen and len(target) and port > 0:
        buffer = input()
        buffer += "\n"
        client_sender(buffer)

    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            if not isinstance(buffer, bytes):
                buffer = buffer.encode('utf-8')
            client.send(buffer)

        while True:

            recv_len = 1
            response = ''.encode('utf-8')

            while recv_len:
                data = client.recv(4096)
                recv_len = len(response)
                response += data
                if recv_len < 4096:
                    break
            if not isinstance(response, str):
                response = response.decode('utf-8')
                print(response)

            buffer = input()
            buffer += "\n"
            if not isinstance(buffer, bytes):
                buffer = buffer.encode('utf-8')
            client.send(buffer)
    except:
        traceback.print_exc()
        client.close()
        sys.exit(0)


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target, port))

        server.listen(5)

        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()
    except:
        traceback.print_exc()
        sys.exit(0)

def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Error!"

    code_name = codecs.lookup(locale.getpreferredencoding()).name
    if not isinstance(output, str):
        output = output.decode(code_name).encode('utf-8')
    else:
        output = output.encode('utf-8')
    return output


def client_handler(client_sokcet):
    global upload
    global execute
    global command

    if len(upload_destination):
        upfile = ''.encode('utf-8')
        while True:
            data = client_sokcet.recv(1024)
            up_file += data
            if len(data) < 1024:
                break
        try:
            with open(upload_destination, 'wb') as f:
                f.write(up_file)

            client_sokcet.send("Successfully saved file to {0}\r\n".format(upload_destination).encode('utf-8'))
        except:
            client_sokcet.send("Failed to save file to {0}\r\n".format(upload_destination).encode('utf-8'))
            traceback.print_exc()

    if len(execute):
        output = run_command(execute)
        if not isinstance(output, bytes):
            output = output.encode('utf-8')
        client_sokcet.send(output)

    if command:
        while True:
            client_sokcet.send("<MAS:#> ".encode('utf-8'))
            cmd_buffer = ''.encode('utf-8')
            while True:
                data = client_sokcet.recv(1024)
                cmd_buffer += data
                if "\n" in cmd_buffer.decode('utf-8'):
                    break

            output = run_command(cmd_buffer.decode('utf-8'))
            client_sokcet.send(output)



if __name__ == '__main__':
    main()
