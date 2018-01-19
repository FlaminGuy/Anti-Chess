#!/usr/bin/env python2.7
from subprocess import Popen, PIPE
import sys
import tempfile
import time
from os import read

deftime=180

white = Popen(['./main.py','white','./sf'],stdin=PIPE,stdout=PIPE)
black = Popen(['./main.py','black','./sf'],stdin=PIPE,stdout=PIPE)

prv = time.time()
def ts():
	global prv
	cur = time.time()
	ret = cur-prv
	prv = cur
	return ret
moves = []
black_time = deftime
white_time = deftime

def printit():
	board = Popen('./sf',stdin=PIPE,stdout=PIPE)
	board.stdin.write('position startpos moves '+' '.join(moves)+'\nd\nisready\n')
	while True:
		line = board.stdout.readline().strip()
		if line=="readyok":
			break
		print(line)
	board.kill()

while True:
	ts()
	move = ""
	while len(move) < 4:
		time.sleep(0.01)
		try:
			move = read(white.stdout.fileno(),1024).strip()
		except OSError:
			move = ""
	tt=ts()
	white_time -= tt
	print(str(tt)+"white made move "+move)
	moves.append(move)
	if move=="1/2-1/2": break
	black.stdin.write(move+"\n")
	printit()

	ts()
	move = ""
	while len(move) < 4:
		time.sleep(0.01)
		try:
			move = read(black.stdout.fileno(),1024).strip()
		except OSError:
			move = ""
	tt=ts()
	black_time -= tt
	print(str(tt)+"black made move "+move)
	moves.append(move)
	if move=="1/2-1/2": break
	white.stdin.write(move+"\n")
	printit()

white.kill()
black.kill()

print(moves)
print('position startpos moves '+' '.join(moves))
print('white time left '+str(white_time))
print('black time left '+str(black_time))
