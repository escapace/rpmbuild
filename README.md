# rpmbuild

RPM package collection

```sh
docker run --rm -it \
  --privileged \
  -v $(pwd):/tmp/repository \
  -e HOST_UID="$(id -u)" \
  -e HOST_GID="$(id -g)" \
  --entrypoint /bin/bash \
  ghcr.io/escapace/rpmbuild:latest
```
