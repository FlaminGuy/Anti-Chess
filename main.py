#!/usr/bin/env python2.7
import subprocess
import sys
import time

DEBUG = False
clock = 180
clock *= 0.95

sf = None
if len(sys.argv)>=3:
	sf = subprocess.Popen(sys.argv[2],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
else:
	sf = subprocess.Popen('./sf',stdin=subprocess.PIPE,stdout=subprocess.PIPE)

if len(sys.argv) < 2:
	sys.stderr.write("need to supply side! (white/black)\n")
	sys.exit(1)
colour = sys.argv[1]
is_white = False
is_black = False
if colour[0]=='w' or colour[0]=='W':
	is_white = True
if colour[0]=='b' or colour[0]=='B':
	is_black = True
if is_white + is_black != 1:
	sys.stderr.write("side must be either 'white' or 'black'\n")
	sys.exit(1)
if DEBUG:
	sys.stderr.write("playing as white\n" if is_white else "playing as black\n")

best_move = None
def sf_command(cmd):
	if DEBUG:
		sys.stderr.write("sending command '"+cmd+"'\n")
	sf.stdin.write(cmd)
	sf.stdin.write("\nisready\n")
	time.sleep(0.01)
	while True:
		line = sf.stdout.readline().strip()
		if DEBUG:
			sys.stderr.write('got line "'+line+'"\n')
		if line == "readyok":
			return
		if len(line)>0 and line.split()[0]=='bestmove':
			global best_move
			best_move = line.split()[1]

moves = []
def sf_setpos():
	sf_command('stop')
	cmd = "position startpos"
	if len(moves)>0:
		cmd += " moves " + " ".join(moves)
	sf_command(cmd)
	sf_command('go infinite')
	time.sleep(0.01)
	global best_move
	best_move = None

	if DEBUG:
		sys.stderr.write("am "+sys.argv[1]+" ")
		sys.stderr.write("current movelist: ")
		sys.stderr.write(str(moves)+"\n")

def make_move(move):
	moves.append(move)
	sf_setpos()

def receive_move():
	move = sys.stdin.readline().strip()
	if DEBUG:
		sys.stderr.write('received from user move '+move+'\n')
	make_move(move)

sf_command('uci')
sf_command('ucinewgame')

def think_move():
	sf_command('stop')
	global best_move
	best_move = None
	if is_white: sf_command('go wtime '+str(int(clock*1000)))
	if is_black: sf_command('go btime '+str(int(clock*1000)))
	sf_command('go infinite')
	while best_move is None:
		sf_command('stop')
		sf_command('go infinite')
	if DEBUG:
		sys.stderr.write('got BESTMOVE '+best_move+'\n')
	return best_move

if is_white:
	move = "g1f3"
	print(move)
	sys.stdout.flush()
	make_move(move)

sf_setpos()

nmoves = 0
while True:
	receive_move()
	L = time.time()
	if DEBUG:
		sf_command('d')
		sys.stderr.write("thinking...\n")
	move = think_move()
	nmoves += 1
	if move == "(none)" or nmoves > 320:
		move = "1/2-1/2"
	print(move)
	sys.stdout.flush()
	make_move(move)
	if DEBUG:
		sf_command('d')
		sys.stderr.write("your move\n")
	R = time.time()
	if DEBUG:
		sys.stderr.write(sys.argv[1]+" used time "+str(R-L)+"\n")
	clock -= R-L + 0.1
	if clock<0.1:
		clock = 0.1




