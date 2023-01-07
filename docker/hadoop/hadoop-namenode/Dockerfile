FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
LABEL maintainer="YPangalela"

ENV HDFS_CONF_DFS_NAMENODE_DATA_DIR=file:///hadoop/dfs/name

RUN mkdir -p /hadoop/dfs/name

VOLUME /hadoop/dfs/name

COPY ./start-namenode.sh ./start-namenode.sh

RUN chmod +x ./start-namenode.sh

EXPOSE 9870

CMD [ "./start-namenode.sh" ]