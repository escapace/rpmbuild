# RPM build workspace

Non-obvious invariants for updating or adding RPM packages in this repo.

## Extracting sources from an upstream SRPM

Use `rpm2cpio` + `cpio` to extract individual files from a `.src.rpm`:

```sh
rpm2cpio <pkg>.src.rpm | cpio -idmv '<filename>'
```

Running `rpm -qp --list` first shows what is inside before extracting.

## Rebasing a spec from an upstream SRPM

When adopting a spec from an upstream SRPM (e.g. Fedora), reset the
`rpmautospec` `release_number` back to `1`. Upstream SRPMs carry their
own release counter; leaving it in place produces a wrong local NVR.

## Vendor tarballs across minor version bumps

For packages that bundle dependencies via a CMake `deps.txt` (e.g. neovim),
a vendor tarball from one release can be reused for the next if every
dependency URL and version in `cmake.deps/deps.txt` is identical.

**Always verify** before reusing: diff the `deps.txt` files from both
releases. If any entry changed, download the new dependency and rebuild
the vendor tarball.

## Vendor tarball directory prefix

The directory name **inside** the vendor tarball must match the package
version being built (e.g. `neovim-0.12.3-vendor/…`). The cmake build uses
the directory as a path. Re-package with the correct prefix even when the
contents are unchanged:

```sh
tar -xzf old-vendor.tar.gz --strip-components=1 -C tmp-dir/new-pkg-vendor
tar -czf new-vendor.tar.gz -C tmp-dir new-pkg-vendor
```

## System dependency availability

Before activating a `BuildRequires` for a system library, confirm it is
present and meets the minimum version:

```sh
pkg-config --modversion <lib>
pkg-config --atleast-version=<min> <lib> && echo OK || echo MISSING
dnf repoquery <lib>-devel
```

If the library is absent from all configured repos, fall back to the
bundled version via the appropriate `-DUSE_BUNDLED_<LIB>=ON` cmake flag
and leave the `BuildRequires` commented out with a note.

## Local mock dependencies and cascading `Requires`

When building a new local dependency (e.g. `spice-protocol`), you must explicitly add its RPM path to the `PACKAGE_INSTALL_REQUIREMENTS` block in `./manage`. 

Crucially, if the new dependency is exposed downstream via `pkg-config` (e.g. `spice-server.pc` contains `Requires: spice-protocol`), you must **also** add it to the `PACKAGE_INSTALL_REQUIREMENTS` of any downstream package that builds against it (e.g. `qemu`). `mock` runs isolated rebuilds and will fail to resolve transitive dependencies if they are only available locally.

## Large upstream source tarballs

Do not commit upstream source tarballs that exceed GitHub's 100MB file size limit (e.g. QEMU). Instead, exclude them from the repo and download them dynamically in the GitHub Actions workflow (`.github/workflows/build.yaml`) using a secure `curl` step prior to running the `./manage build` command.
