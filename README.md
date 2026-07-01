# rpmbuild

RPM package collection for CentOS Stream 10.

The top-level `manage` command is a Python 3 script with no runtime Python dependencies.

- `./manage build ...` and `./manage update-repository` run on the host and invoke Docker.
- `manage container-build ...` and `manage container-update-repository` run inside the image.

## Container image

```sh
# Optional, for cross-architecture builds.
# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

docker buildx create --driver docker-container --use

docker buildx build \
  --platform linux/amd64 \
  --tag ghcr.io/escapace/rpmbuild:latest-amd64 \
  --load .

docker buildx build \
  --platform linux/arm64 \
  --tag ghcr.io/escapace/rpmbuild:latest-arm64 \
  --load .
```

If sudo fails inside the arm64 container, change the binfmt flag to `OCF` in `/usr/lib/binfmt.d/qemu-aarch64-static.conf`, then run:

```sh
sudo systemctl restart systemd-binfmt.service
```

## Build packages

Use `RPMBUILD_IMAGE` to select a local image, or let `manage` default to `ghcr.io/escapace/rpmbuild`.

```sh
RPMBUILD_IMAGE=ghcr.io/escapace/rpmbuild:latest-amd64 \
  ./manage build --platform linux/amd64 python-pymongo

RPMBUILD_IMAGE=ghcr.io/escapace/rpmbuild:latest-arm64 \
  ./manage build --platform linux/arm64 lua-cqueues
```

## Update repository metadata

```sh
./manage update-repository
```

This builds a small inline CentOS Stream 10 image with `createrepo_c`, then runs `container-update-repository` and writes `repository/stable/linux/centos/10/...` in the mounted repository checkout.

## Check for outdated RPMs

On CentOS Stream 10, compare RPMs in `RPMS/` with the latest packages available from enabled CentOS and EPEL repositories. The output includes packages available at the same version as well as newer versions.

```sh
./manage outdated
./manage outdated --arch aarch64
./manage outdated --arch all --json
```
