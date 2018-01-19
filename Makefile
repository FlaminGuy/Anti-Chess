all: sf
sf: ./Stockfish/*.cpp ./Stockfish/*.h
	$(MAKE) -C ./Stockfish build ARCH=x86-64
	cp ./Stockfish/stockfish ./sf
clean:
	$(MAKE) -C ./Stockfish clean
	rm sf