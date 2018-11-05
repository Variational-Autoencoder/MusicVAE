build:
	docker build -t munkai/pytorch:cpu -f Dockerfile.cpu .

run:
	docker run -it -p 8888:8888 -v `pwd`:/work -v `pwd`/../clean_midi:/work/clean_midi munkai/pytorch:cpu ./jupyter_run.sh

.PHONY: run build
