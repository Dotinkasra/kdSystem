FROM ubuntu

# ENVは環境変数API_PATHを指定します。
# /apiはコンテナ側のディレクトリです。
# ENV API_PATH /api

# WORKDIR はRUN CMD ENTRYPOINT COPY ADD 実行時の
# 作業ディレクトリを指定します。
# WORKDIR $API_PATH
RUN export LANG=C.UTF-8
RUN export LANGUAGE=en_US:

RUN apt update -y
RUN apt install python3 -y -qq --no-install-recommends
RUN apt install python3-pip -y -qq --no-install-recommends
RUN pip3 install --upgrade pip

RUN pip install flask
RUN pip install PyMySQL
RUN pip install flask_restful
RUN pip install requests_oauthlib
RUN pip install natsort