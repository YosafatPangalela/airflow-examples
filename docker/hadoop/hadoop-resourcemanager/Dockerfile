FROM bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8
LABEL maintainer="YPangalela"

COPY start-resourcemanager.sh start-resourcemanager.sh

RUN chmod +x start-resourcemanager.sh

EXPOSE 8088

CMD [ "./start-resourcemanager.sh" ]