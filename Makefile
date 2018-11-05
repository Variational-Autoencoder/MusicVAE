build:
	docker build -t munkai/pytorch:cpu -f Dockerfile.cpu .

run:
	docker run -it -p 8888:8888 -v `pwd`:/work munkai/pytorch:cpu ./jupyter_run.sh

.PHONY: run build
