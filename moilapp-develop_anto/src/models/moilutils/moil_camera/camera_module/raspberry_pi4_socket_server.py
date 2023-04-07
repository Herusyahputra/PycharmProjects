import socket

HOST = '0.0.0.0'
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

while True:
	conn, addr = s.accept()
	while True:
		indata = conn.recv(1024)
		print(f'get: {indata.decode()} from: {addr}')
		if len(indata) == 0:
			conn.close()
			break
		outdata = 'raspberrypi'
		conn.send(outdata.encode())