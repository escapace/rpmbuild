# rpmbuild

RPM package collection

```sh
# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

docker buildx create --driver docker-container
docker buildx use NAME

docker buildx build \
--platform linux/amd64 \
--tag escapace/rpmbuild:amd64 \
--load .

docker buildx build \
--platform linux/arm64 \
--tag escapace/rpmbuild:arm64 \
--load .

docker run --rm -it \
  --privileged --platform linux/amd64 \
  -v $(pwd):/tmp/repository \
  -e HOST_UID="$(id -u)" \
  -e HOST_GID="$(id -g)" \
  --entrypoint /bin/bash \
  escapace/rpmbuild:amd64

docker run --rm -it \
  --privileged --platform linux/arm64 \
  -v $(pwd):/tmp/repository \
  -e HOST_UID="$(id -u)" \
  -e HOST_GID="$(id -g)" \
  --entrypoint /bin/bash \
  escapace/rpmbuild:arm64
```

If unable to sudo inside the container change the binfmt flag to `OCF` in
`/usr/lib/binfmt.d/qemu-aarch64-static.conf`.

sudo systemctl restart systemd-binfmt.service
