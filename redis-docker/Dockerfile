FROM redis:alpine
WORKDIR /redis
RUN echo 1 > /proc/sys/vm/overcommit_memory

RUN redis-server /usr/local/etc/redis/redis.conf --bind 0.0.0.0