FROM nvidia/cuda:12.1.1-base-ubuntu22.04

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Fixing apt question for timezone
RUN apt update
RUN export TZ=Europe/Prague && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# FastAPI
RUN apt-get install -y python3.10 python3-pip ffmpeg libsm6 libxext6 git && pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN git clone https://github.com/facebookresearch/AnimatedDrawings.git && cd AnimatedDrawings && pip3 install -e .
# Animated drawings 

COPY ./main.py /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]