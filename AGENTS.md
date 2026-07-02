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

## Large source artifacts and generated SRPMs

Do not commit upstream source tarballs or generated SRPMs that exceed GitHub's 100MB file size limit (e.g. QEMU). Instead, exclude them from the repo and download upstream tarballs dynamically in the GitHub Actions workflow (`.github/workflows/build.yaml`) using a secure `curl` step prior to running the `./manage build` command. After extracting `packages-*.zip` workflow artifacts, check non-gitignored files for this limit before committing.

## Porting Fedora specs to CentOS 10

When adopting a `.spec` file from Fedora to CentOS Stream 10:
1. Ensure the `Release` tag strictly uses `1%{?dist}` so it natively resolves to `.el10` in the buildroot.
2. Review all `%if 0%{?fedora}` conditional blocks. Important dependencies or features enabled only for modern Fedora versions will be silently dropped on CentOS unless the condition is explicitly expanded to include `|| 0%{?rhel} >= 10`.

## GPG signature synchronization

When updating an upstream source tarball to a new release (e.g. modifying `Version` in a `.spec`), you **must** also download the matching `.sig` or `.asc` signature file for that specific release. Reusing an old signature file, even if renamed, will cause `rpmbuild` to fail instantly in `%prep` with a `BAD signature` error. Since signature files are tiny, commit them directly to the repository alongside the `.spec`.

## Strict RPM %changelog date formatting

`rpmbuild` enforces strict day-of-week validation in `%changelog` blocks. If you manually add a changelog entry, you **must** use a command like `date -d "YYYY-MM-DD"` to verify the exact day of the week (e.g., `Thu` vs `Wed`). Hardcoding the wrong day for a given date will cause an immediate `bogus date in %changelog` build failure.

## Auditing %files during major version bumps

When adopting an older `.spec` for a major new software release, the upstream project frequently adds, renames, or drops firmware blobs, modules, or directories. Do **not** blindly run the build and react to `Installed (but unpackaged) file(s)` or `File not found` errors sequentially (which requires hours of slow rebuilds). Instead:

1. Download the new upstream `.spec` file.
2. Use `comm -13` and `comm -23` to mathematically diff the extracted `%files` block paths between your local spec and the upstream spec.
3. Preemptively add or remove these exact paths from your local `%files` sections to align perfectly with upstream.
