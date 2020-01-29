FROM ubuntu:16.04
RUN apt-get update && apt-get install -y --no-install-recommends \
	python3-dev \
	python3-pip \
	build-essential libssl-dev libffi-dev \
	libxml2-dev libxslt1-dev zlib1g-dev \
	&& \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -U pip setuptools
RUN pip3 install -r requirements.txt
RUN python3 setup.py build
RUN python3 setup.py install

ENTRYPOINT python3 -m stableconfigs input/example.txt

