FROM bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
LABEL maintainer="YPangalela"

ENV HDFS_CONF_DFS_DATANODE_DATA_DIR=file:///hadoop/dfs/data

RUN mkdir -p /hadoop/dfs/data

VOLUME /hadoop/dfs/data

COPY start-datanode.sh start-datanode.sh

RUN chmod +x start-datanode.sh

EXPOSE 9864

CMD [ "./start-datanode.sh" ]