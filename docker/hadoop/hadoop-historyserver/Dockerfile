FROM bde2020/hadoop-historyserver:2.0.0-hadoop3.2.1-java8
LABEL maintainer="YPangalela"

RUN mkdir -p /hadoop/yarn/timeline

VOLUME [ "/hadoop/yarn/timeline" ]

COPY start-historyserver.sh start-historyserver.sh

RUN chmod +x start-historyserver.sh

EXPOSE 8188

CMD [ "./start-historyserver.sh" ]
