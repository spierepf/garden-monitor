repl:
	cd pyboard && MICROPYPATH=./lib:. micropython

upload:
	rshell rsync pyboard /pyboard

download:
	rshell rsync /pyboard pyboard

run-app-local:
	cd pyboard && MICROPYPATH=./lib:. micropython -m app

run-app:
	rshell repl \~ import app \~
