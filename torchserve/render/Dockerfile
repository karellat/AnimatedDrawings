FROM nvidia/cuda:12.1.1-base-ubuntu22.04

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Fixing apt question for timezone
RUN apt update
RUN export TZ=Europe/Prague && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# FastAPI
RUN apt-get install -y python3.10 python3-pip ffmpeg libsm6 libxext6 git && pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN git clone https://github.com/karellat/AnimatedDrawings && cd AnimatedDrawings && pip3 install -e .
# Animated drawings 
# Install OpenGL
RUN apt-get install -y cmake pkg-config mesa-utils libglu1-mesa-dev freeglut3-dev mesa-common-dev libglew-dev libglfw3-dev libglm-dev libao-dev libmpg123-dev
# Dummy Display
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY :1
RUN apt-get install -y xserver-xorg-video-dummy x11-apps
VOLUME /tmp/.X11-unix

COPY ./xorg.conf /etc/X11/xorg.conf
COPY ./main.py /code/
COPY ./config /code/config
COPY ./start.sh /code/

CMD ["/bin/sh", "-c", "bash ./start.sh"]