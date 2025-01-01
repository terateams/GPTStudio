FROM python:3.12.8-bookworm

# 设置非交互式前端，避免 apt-get 交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 设置时区
RUN echo "Asia/Shanghai" > /etc/timezone && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apt-get update && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata


RUN apt-get update && \
    apt-get install -y  build-essential ca-certificates libffi-dev libssl-dev libasound2 curl iputils-ping wget && \
    apt-get install -y  poppler-utils ffmpeg libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf - && \
#     cd openssl-1.1.1u && \
#     ./config --prefix=/usr/local && \
#     make -j $(nproc) && \
#     make install_sw install_ssldirs && \
#     ldconfig -v && \
#     export SSL_CERT_DIR=/etc/ssl/certs

# 设置工作目录
WORKDIR /gptstudio
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY requirements-news.txt ./requirements-news.txt
RUN pip install --no-cache-dir -r requirements-news.txt

# 复制项目文件
COPY ./.streamlit ./.streamlit
COPY ./assets ./assets
COPY ./gptstudio ./gptstudio
COPY ./assets ./assets
COPY ./gptstudio.py ./gptstudio.py


ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 暴露 Streamlit 默认端口
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

# 设置启动命令
CMD ["streamlit","run", "gptstudio.py"]
