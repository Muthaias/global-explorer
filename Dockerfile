FROM fedora

RUN dnf update -y && \
    dnf install python -y 
RUN dnf install python-pip -y

COPY ./requirements.txt /opt/requirements.txt

RUN python -m pip install -r /opt/requirements.txt

VOLUME [ "/exec" ]
WORKDIR /exec
ENTRYPOINT [ "bash" ]