FROM bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8
LABEL maintainer="YPangalela"

COPY start-nodemanager.sh start-nodemanager.sh

RUN chmod +x start-nodemanager.sh

EXPOSE 8042

CMD [ "./start-nodemanager.sh" ]