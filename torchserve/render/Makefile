SHELL := /bin/sh

run_local: 
	source ~/.bashrc && conda activate animated_drawings && uvicorn main:app --reload
build: 
	sudo docker build -t animatedapi .
run: build
	sudo docker run -it --gpus=all --rm -p 8000:8000 --name animated animatedapi 
term: 
	sudo docker container exec -it animated /bin/sh

test:
	curl -v -F "motion_id=2" -F "char_cfg=@example/char_cfg.yaml" -F "mask=@example/mask.png" -F "texture=@example/texture.png" -o 'example.gif' http://localhost:8000/render 