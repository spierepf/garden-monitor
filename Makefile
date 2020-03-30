repl:
	cd pyboard && MICROPYPATH=./lib:. micropython

upload:
	rshell rsync pyboard /pyboard

download:
	rshell rsync /pyboard pyboard
