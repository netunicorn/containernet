FROM ubuntu:22.04
LABEL maintainer="manuel@peuster.de"

ENV DEBIAN_FRONTEND=noninteractive

# install required packages
RUN apt-get clean
RUN apt-get update \
    && apt-get install -y  git \
    net-tools \
    aptitude \
    build-essential \
    python3-setuptools \
    python3-dev \
    python3-pip \
    software-properties-common \
    ansible \
    curl \
    iptables \
    iputils-ping \
    sudo \
    nano \
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install containernet (using its Ansible playbook)
COPY . /containernet
WORKDIR /containernet/ansible
RUN ansible-playbook -i "localhost," -c local --skip-tags "notindocker" install.yml && \
    apt-get autoremove -y && apt clean && rm -rf /var/lib/apt/lists/* && pip cache purge
WORKDIR /containernet
RUN make develop

# Hotfix: https://github.com/pytest-dev/pytest/issues/4770
RUN pip3 install "more-itertools<=5.0.0"

# tell containernet that it runs in a container
ENV CONTAINERNET_NESTED 1

# Important: This entrypoint is required to start the OVS service
ENTRYPOINT ["util/docker/entrypoint.sh"]
CMD ["python3", "examples/netunicorn_test.py"]

