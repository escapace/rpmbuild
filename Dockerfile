FROM quay.io/centos/centos:stream10

ENV container=docker
ENV DOCKER=true

RUN dnf clean all && \
  dnf update --assumeyes && \
  dnf install --assumeyes dnf-plugins-core epel-release && \
  dnf config-manager --set-enabled crb && \
  dnf install --assumeyes --allowerasing \
    bc \
    coreutils \
    createrepo_c \
    expect \
    findutils \
    git \
    gnupg \
    mock \
    rpm-build \
    rpm-sign \
    sudo \
    yum-utils && \
  dnf clean all && \
  rm -rf /var/cache/yum/ /var/cache/dnf/

RUN adduser -u 1000 -G mock -U -m centos && \
  echo 'centos ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
  mkdir -p /home/centos/cache /home/centos/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
  echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros && \
  echo "config_opts['isolation'] = 'simple'" >> /etc/mock/site-defaults.cfg && \
  echo "config_opts['cache_topdir'] = '/home/centos/cache/mock'" >> /etc/mock/site-defaults.cfg && \
  chmod g+w /etc/mock/*.cfg

WORKDIR /home/centos/rpmbuild
VOLUME /tmp/repository
VOLUME /home/centos/cache

COPY ./manage /home/centos/rpmbuild/manage
COPY ./.manage.yml /home/centos/rpmbuild/.manage.yml
COPY ./scripts /home/centos/rpmbuild/scripts

RUN chown centos:centos -R /home/centos && install -g mock -m 2775 -d /home/centos/cache/mock

USER centos
RUN /home/centos/rpmbuild/manage trust-escapace
ENTRYPOINT ["/home/centos/rpmbuild/manage"]
CMD ["build"]
