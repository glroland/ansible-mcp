install:
	pip install -r requirements.txt

dev:
	cd src && mcp dev mcp_server.py 

run:
	cd src && python mcp_server.py

build:
	podman build . --platform=linux/amd64 -t ansible-mcp:latest
