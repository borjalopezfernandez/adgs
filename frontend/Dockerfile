#########################################################################
#
#     Dockerfile.dev
#
#########################################################################
#
# Dockerfile for the development of the Front-End of the ADGS
#
# Base the image on centos7
FROM centos:centos7
MAINTAINER Daniel Brosnan Blázquez <daniel.brosnan@deimos-space.com>

ARG ADGSFE_PACKAGE

USER root

RUN useradd -m -o -r -u 2020 adgs

RUN yum install -y epel-release

RUN yum install -y python36 \
    python36-pip \
    gcc \
    python36-devel \
    pytest \
    npm \
    openssl \
    chromium \
    chromedriver

RUN yum update -y

RUN pip3 install wheel

# Copy ADGSFE package
RUN mkdir /adgsfe_packages
COPY --from=adgsfe_packages_directory $ADGSFE_PACKAGE /adgsfe_packages
RUN chown -R adgs:adgs /adgsfe_packages
    
# Create folders for ADGSFE
RUN mkdir /log
RUN mkdir /scripts
RUN mkdir /resources_path

# Change ownership to the boa user
RUN chown -R adgs /log /scripts /resources_path

# Create directory where the auxip repository is going to be attached for development
RUN mkdir /adgsfe
RUN chown adgs /adgsfe

USER adgs

# Install ADGSFE package
RUN pip3 install --user /adgsfe_packages/*

# Environment Variables for ADGSFE
ENV FLASK_APP adgsfe
ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV PATH="${PATH}:/scripts"

# Add path to the scripts installed by pip in the home of the adgs user to PATH
ENV PATH="${PATH}:/home/adgs/.local/bin"

# expose port
EXPOSE 5000

CMD ["/bin/bash", "-c", "gunicorn --worker-tmp-dir /dev/shm -b 0.0.0.0:5000 -w 12 $FLASK_APP.wsgi:app --log-file /log/web_server -t 3600; sleep infinity"]