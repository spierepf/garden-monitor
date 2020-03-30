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

install-deps:
	cd pyboard && MICROPYPATH=./lib:. micropython -m upip install -r ../requirements.txt

run-update-local:
	cd pyboard && MICROPYPATH=./lib:. micropython -m update

run-update:
	rshell repl \~ import update \~
