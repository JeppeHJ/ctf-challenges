# Dockerfile for pwn - Dat Overflow Dough
FROM ubuntu:latest

COPY ./recipe .
COPY ./flag.txt .

RUN chmod +x recipe

RUN apt-get update -y
RUN apt-get install -y socat

#RUN gcc -O0 -g -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0 -Wl,-z,norelro recipe.c -o recipe

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:'./recipe'"]
