import socket
import sys
import argparse

def getMsg(string):
    msg = string
    bytes = b""
    while bytes != msg:
        bytes += sock.recv(2022)
        if bytes == msg:
            break
        if msg.find(bytes) != 0:
            bytes = b""


def mail(filename, sock):
    try:
        file = open(filename, "rb")
    except FileNotFoundError:
        print(f"The file named {filename} doesn't exit.")
        quit()
    else:
        while True:
            portion = file.read(10000)
            if portion:
                sock.send(portion)
            else:
                file.close()
                break


#Connects Client and Binds them to the address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Arguments Needed - Parser
parser = argparse.ArgumentParser()
parser.add_argument("host", type = str, help = "Host name")
parser.add_argument("port", type = int, help = "Port number")
parser.add_argument("filename", type = str, help = "File name")
args = parser.parse_args()

if int(port) < 1 or int(port) > 65535:
    sys.stderr.write("ERROR:")
    sys.exit(1)


#10 second timeout counter
sock.settimeout(10)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4044)

try:
    sock.connect((args.host, args.port))

    getMsg(b"accio\r\n")# First Message

    sock.send(b"confirm-accio\r\n")  # First Confirm

    getMsg(b"accio\r\n")# Second Message

    sock.send(b"confirm-accio-again\r\n")  # Second Confirm

    sent = sock.send(b"\r\n")

    mail(args.filename, sock)
    sock.close()

except socket.error: #TimeOut
    sys.stderr.write("ERROR:")
    sys.exit(1)

sys.exit(0)
