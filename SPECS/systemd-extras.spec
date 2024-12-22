#global commit 1781de18ab8ebc3e42a607851d8effb3b0355c87
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

%global stable 1

%if 0%{?__isa_bits} == 64
%global elf_bits (64bit)
%global elf_suffix ()%{elf_bits}
%endif

# Bootstrap may be needed to break circular dependencies with cryptsetup,
# e.g. when re-building cryptsetup on a json-c SONAME-bump.

%bcond bootstrap 0
%bcond tests   0
%bcond lto     0

# When bootstrap, libcryptsetup is disabled
# but auto-features causes many options to be turned on
# that depend on libcryptsetup (e.g. libcryptsetup-plugins)
%global __meson_auto_features disabled

# Support for quick builds with rpmbuild --build-in-place.
# See README.build-in-place.
%bcond_with    inplace

Name:           systemd-extras
Url:            https://systemd.io
%if %{without inplace}
Version:        256
Release:        1%{?commit:.git%{shortcommit}}%{?dist}
%else
# determine the build information from local checkout
Version:        %(tools/meson-vcs-tag.sh . error | sed -r 's/-([0-9])/.^\1/; s/-g/_g/')
Release:        1
%endif

# For a breakdown of the licensing, see README
License:        LGPL-2.1-or-later AND MIT AND GPL-2.0-or-later
Summary:        System and Service Manager (optional components)

%global github_version %(c=%{version}; echo ${c}|tr '~' '-')

# download tarballs with "spectool -g systemd.spec"
%if %{defined commit}
Source0:        https://github.com/systemd/systemd%{?stable:-stable}/archive/%{commit}/systemd-%{shortcommit}.tar.gz
%else
%if 0%{?stable}
Source0:        https://github.com/systemd/systemd-stable/archive/v%{github_version}/systemd-%{github_version}.tar.gz
%else
Source0:        https://github.com/systemd/systemd/archive/v%{github_version}/systemd-%{github_version}.tar.gz
%endif
%endif

# Sources to make optional systemd components building on CentOS/RHEL 9
Source9000:     systemd-network.sysusersd
Source9001:     systemd-timesync.sysusersd

# Backports of patches from upstream (0000–0499)
#
# Any patches which are "in preparation" upstream should be listed here, rather
# than in the next section. Packit CI will drop any patches in this range before
# applying upstream pull requests.

# https://github.com/systemd/systemd/issues/26488
# https://bugzilla.redhat.com/show_bug.cgi?id=2164404
# Patch0001:      https://github.com/systemd/systemd/pull/26494.patch

# Those are downstream-only patches, but we don't want them in packit builds:
# https://bugzilla.redhat.com/show_bug.cgi?id=1738828
# Patch0490:      use-bfq-scheduler.patch

# Adjust upstream config to use our shared stack
# Patch0491:      fedora-use-system-auth-in-pam-systemd-user.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  coreutils
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  libfdisk-devel
BuildRequires:  libpwquality-devel
BuildRequires:  pam-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-libs-devel
BuildRequires:  dbus-devel
BuildRequires:  /usr/sbin/sfdisk
# /usr/bin/getfacl is needed by test-acl-util
BuildRequires:  /usr/bin/getfacl
BuildRequires:  libacl-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libblkid-devel
BuildRequires:  xz-devel
BuildRequires:  xz
BuildRequires:  lz4-devel
BuildRequires:  lz4
BuildRequires:  bzip2-devel
BuildRequires:  libzstd-devel
BuildRequires:  libidn2-devel
BuildRequires:  libcurl-devel
BuildRequires:  kmod-devel
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
BuildRequires:  gnutls-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  libxslt
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(tss2-rc)
BuildRequires:  pkgconfig(tss2-mu)
BuildRequires:  pkgconfig(libbpf)
BuildRequires:  docbook-style-xsl
BuildRequires:  pkgconfig
BuildRequires:  gperf
BuildRequires:  gawk
BuildRequires:  tree
BuildRequires:  hostname
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(lxml)
BuildRequires:  firewalld-filesystem
BuildRequires:  libseccomp-devel
BuildRequires:  meson >= 0.43
BuildRequires:  gettext
# We use RUNNING_ON_VALGRIND in tests, so the headers need to be available
BuildRequires:  valgrind-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  perl
BuildRequires:  perl(IPC::SysV)

%description
The systemd-extras package provides optional systemd components as sub-
packages, such as systemd-networkd and systemd-timesyncd, which are not
part of CentOS Stream or Red Hat Enterprise Linux (or possibly
derivatives).
%if 0%{?stable}
This package was built from the %(c=%version; echo "v${c%.*}-stable") branch of systemd.
%endif

%package -n systemd-networkd
Summary:        System daemon that manages network configurations
License:        LGPL-2.1-or-later
BuildRequires:  systemd-rpm-macros
Requires:       dbus >= 1.9.18
Requires:       (util-linux-core or util-linux)
%{?systemd_requires}
%{?sysusers_requires_compat}

# Recommends to replace normal Requires deps for stuff that is dlopen()ed
Recommends:     libidn2.so.0%{?elf_suffix}
Recommends:     libidn2.so.0(IDN2_0.0.0)%{?elf_bits}

%description -n systemd-networkd
systemd-networkd is a system service that manages networks. It detects
and configures network devices as they appear, as well as creating virtual
network devices.

%package -n systemd-timesyncd
Summary:        System daemon to synchronize local system clock with NTP server
License:        LGPL-2.1-or-later
BuildRequires:  systemd-rpm-macros
Requires:       dbus >= 1.9.18
Requires:       (util-linux-core or util-linux)
%{?systemd_requires}
%{?sysusers_requires_compat}

%description -n systemd-timesyncd
systemd-timesyncd is a system service to synchronize the local system clock
with a remote Network Time Protocol server. It specifically implements only
SNTP; this minimalistic service will set the system clock for large offsets
or slowly adjust it for smaller deltas.

%prep
%autosetup -n %{?commit:systemd%{?stable:-stable}-%{commit}}%{!?commit:systemd%{?stable:-stable}-%{github_version}} -p1

%build
%global ntpvendor %(source /etc/os-release; echo ${ID})
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

CONFIGURE_OPTS=(
        -Dmode=release
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
        -Ddns-servers=
        -Duser-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin

        -Dadm-gid=4
        -Dtty-gid=5
        -Ddisk-gid=6
        -Dlp-gid=7
        -Dkmem-gid=9
        -Dwheel-gid=10
        -Dcdrom-gid=11
        -Ddialout-gid=18
        -Dutmp-gid=22
        -Dtape-gid=33
        -Dkvm-gid=36
        -Dvideo-gid=39
        -Daudio-gid=63
        -Dusers-gid=100
        -Dinput-gid=104
        -Drender-gid=105
        -Dsgx-gid=106
        -Dsystemd-journal-gid=190
        -Dsystemd-network-uid=192
        -Dsystemd-resolve-uid=193

        -Dacl=true
        -Danalyze=false
        -Dapparmor=false
        -Daudit=true
        -Db_lto=false
        -Db_ndebug=false
        -Dbacklight=false
        -Dbinfmt=false
        -Dbootloader=disabled
        -Dbpf-framework=false
        -Dbzip2=true
        -Dcompat-mutable-uid-boundaries=true
        -Dcreate-log-dirs=false
        -Dcryptolib=openssl
        -Ddefault-compression=zstd
        -Ddefault-dns-over-tls=no
        -Ddefault-dnssec=no
        -Ddefault-kill-user-processes=false
        -Ddefault-llmnr=no
        -Ddefault-mdns=no
        -Ddefault-net-naming-scheme=latest
        -Ddefault-timeout-sec=45
        -Ddefault-user-timeout-sec=45
        -Ddns-over-tls=openssl
        -Defi=false
        -Delfutils=disabled
        -Dfallback-hostname="localhost"
        -Dfirst-boot-full-preset=true
        -Dfirstboot=true
        -Dgcrypt=disabled
        -Dgnutls=disabled
        -Dhibernate=false
        -Dhomed=disabled
        -Dhtml=disabled
        -Dhwdb=true
        -Dinstall-tests=false
        -Dkernel-install=false
        -Dlibcryptsetup=false
        -Dlibcurl=true
        -Dlibfido2=false
        -Dlibidn2=true
        -Dlibidn=disabled
        -Dlibiptc=disabled
        -Dlink-boot-shared=false
        -Dlink-journalctl-shared=false
        -Dlink-networkd-shared=false
        -Dlink-portabled-shared=false
        -Dlink-systemctl-shared=false
        -Dlink-timesyncd-shared=false
        -Dlink-udev-shared=false
        -Dlogind=false
        -Dlz4=true
        -Dmachined=false
        -Dman=true
        -Dmicrohttpd=false
        -Dmountfsd=false
        -Dnetworkd=true
        -Dnobody-group=nobody
        -Dnobody-user=nobody
        -Dnscd=false
        -Dnsresourced=false
        -Dnss-myhostname=false
        -Dnss-mymachines=false
        -Dnss-systemd=false
        -Doomd=false
        -Dopenssl=true
        -Dp11kit=true
        -Dpam=true
        -Dpolkit=true
        -Dportabled=false
        -Dpstore=false
        -Dpwquality=false
        -Dqrencode=false
        -Dquotacheck=false
        -Dresolve=false
        -Dsbat-distro-url=mailto:secalert@redhat.com
        -Dshared-lib-tag=%{version}-%{release}
        -Dsmack=true
        -Dsplit-bin=true
        -Dsplit-usr=false
        -Dsshconfdir=no
        -Dsshdconfdir=no
        -Dstandalone-binaries=true
        -Dstatic-libsystemd=true
        -Dstatic-libudev=true
        -Dstatus-unit-format-default=combined
        -Dstoragetm=false
        -Dsupport-url=https://access.redhat.com/support
        -Dsysext=false
        -Dsysusers=true
        -Dtests=unsafe
        -Dtimedated=false
        -Dtimesyncd=true
        -Dtmpfiles=true
        -Dtpm2=true
        -Dtpm=true
        -Dukify=disabled
        -Duserdb=false
        -Dvconsole=false
        -Dversion-tag=%{version}-%{release}
        -Dvmspawn=disabled
        -Dxdg-autostart=false
        -Dxenctrl=disabled
        -Dxz=true
        -Dzlib=true
        -Dzstd=true
)

%if %{without lto}
%global _lto_cflags %nil
%endif

# Do configuration. If doing an inplace build, try to do
# reconfiguration to pick up new options.
%if %{with inplace}
  command -v ccache 2>/dev/null && { CC="${CC:-ccache %__cc}"; CXX="${CXX:-ccache %__cxx}"; }

  [ -e %{_vpath_builddir}/build.ninja ] &&
  %__meson configure %{_vpath_builddir} "${CONFIGURE_OPTS[@]}" ||
%endif
{ %meson "${CONFIGURE_OPTS[@]}"; }

%meson_build

%install
%meson_install

pushd %{buildroot}
  find . \( -type f -o -type l \) -print0 | \
    grep -E -v '(net(work|dev)|time(sync|-set|-wait-sync))' -z -Z | \
    xargs -0 --no-run-if-empty -n1 -IFILE rm -v FILE

    rm -f %{buildroot}%{_prefix}/lib/systemd/portable/profile/nonetwork/service.conf
    rm -f %{buildroot}%{_prefix}/lib/systemd/network/99-default.link
    rm -f %{buildroot}%{_prefix}/lib/systemd/system/network{-online,-pre,}.target
    rm -rf %{buildroot}%{_prefix}/lib/systemd/tests/

    find . -type d -empty -delete
popd

mkdir -p %{buildroot}%{_sysconfdir}/systemd/network/
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/timesync/
touch %{buildroot}%{_localstatedir}/lib/systemd/timesync/clock
# Since systemd v250, systemd-network-generator is no longer part of systemd-networkd, see
# also: https://github.com/systemd/systemd/commit/987dd89c775815831ae21736fe60aef59cb7a6fa
rm -f %{buildroot}{%{_prefix}/lib/systemd,%{_unitdir},%{_mandir}/man8}/systemd-network-generator*

%check
# Nothing must link against libsystemd-shared.so
for binary in $(find %{buildroot} -type f -executable); do
  ! ldd $binary 2>&1 | grep 'libsystemd-shared' &> /dev/null
done

%pre -n systemd-networkd
%sysusers_create_compat %{SOURCE9000}

%post -n systemd-networkd
%systemd_post systemd-networkd.service systemd-networkd-wait-online.service

%preun -n systemd-networkd
%systemd_preun systemd-networkd.service systemd-networkd-wait-online.service

%postun -n systemd-networkd
%systemd_postun_with_restart systemd-networkd.service systemd-networkd-wait-online.service

%pre -n systemd-timesyncd
%sysusers_create_compat %{SOURCE9001}

%post -n systemd-timesyncd
%if 0%{?rhel} == 8
# Move old stuff around in /var/lib
if [ -L %{_localstatedir}/lib/systemd/timesync ]; then
    rm %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/private/systemd/timesync %{_localstatedir}/lib/systemd/timesync
fi
if [ -f %{_localstatedir}/lib/systemd/clock ] ; then
    mkdir -p %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/systemd/clock %{_localstatedir}/lib/systemd/timesync/.
fi
%endif
%systemd_post systemd-timesyncd.service

%preun -n systemd-timesyncd
%systemd_preun systemd-timesyncd.service

%postun -n systemd-timesyncd
%systemd_postun_with_restart systemd-timesyncd.service

%files -n systemd-networkd
%license LICENSE.LGPL2.1
%dir %{_sysconfdir}/systemd/network/
%config(noreplace) %{_sysconfdir}/systemd/networkd.conf
%{_bindir}/networkctl
%dir %{_prefix}/lib/systemd/network/
%{_prefix}/lib/systemd/network/*
%{?el8:%{_unitdir}/systemd-network-generator.service}
%{_unitdir}/systemd-networkd-*
%{_unitdir}/systemd-networkd.service
%{_unitdir}/systemd-networkd.socket
%{?el8:%{_prefix}/lib/systemd/systemd-network-generator}
%{_prefix}/lib/systemd/systemd-networkd
%{_prefix}/lib/systemd/systemd-networkd-wait-online
%{_sysusersdir}/systemd-network.conf
%{_tmpfilesdir}/systemd-network.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.*
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.network1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.network1.policy
%{_datadir}/polkit-1/rules.d/systemd-networkd.rules
%{_mandir}/man1/networkctl.1*
%{_mandir}/man5/networkd.conf.5*
%{_mandir}/man5/networkd.conf.d.5*
%{_mandir}/man5/org.freedesktop.network1.5*
%{_mandir}/man5/systemd.netdev.5*
%{_mandir}/man5/systemd.network.5*
%{?el8:%{_mandir}/man8/systemd-network-generator.8*}
%{?el8:%{_mandir}/man8/systemd-network-generator.service.8*}
%{_mandir}/man8/systemd-networkd-wait-online.8*
%{_mandir}/man8/systemd-networkd-wait-online.service.8*
%{_mandir}/man8/systemd-networkd-wait-online@.service.8*
%{_mandir}/man8/systemd-networkd.8*
%{_mandir}/man8/systemd-networkd.service.8*
# "/usr/share/bash-completion/completions" is owned by "filesystem", no need to specify
# this explicitely in "Requires:"
%{_datadir}/bash-completion/completions/networkctl
# "/usr/share/zsh" is not owned by any package
# "/usr/share/zsh/site-functions" is owned by curl, likely a packaging error in RHEL
%{_datadir}/zsh/site-functions/_networkctl

%files -n systemd-timesyncd
%license LICENSE.LGPL2.1
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%dir %{_prefix}/lib/systemd/ntp-units.d/
%{_prefix}/lib/systemd/ntp-units.d/80-systemd-timesync.list
%{_unitdir}/systemd-time-wait-sync.service
%{_unitdir}/systemd-timesyncd.service
%{?el8:%dir %{_unitdir}/systemd-tmpfiles-clean.service.d/}
%{?el8:%{_unitdir}/systemd-tmpfiles-clean.service.d/10-time-set.conf}
%{_unitdir}/time-set.target
%{?el8:%dir %{_unitdir}/time-sync.target.d/}
%{?el8:%{_unitdir}/time-sync.target.d/10-time-set.conf}
%{_prefix}/lib/systemd/systemd-time-wait-sync
%{_prefix}/lib/systemd/systemd-timesyncd
%{_sysusersdir}/systemd-timesync.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.timesync1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.timesync1.policy
%{_mandir}/man5/timesyncd.conf.5*
%{_mandir}/man5/timesyncd.conf.d.5*
%{_mandir}/man8/systemd-time-wait-sync.8*
%{_mandir}/man8/systemd-time-wait-sync.service.8*
%{_mandir}/man8/systemd-timesyncd.8*
%{_mandir}/man8/systemd-timesyncd.service.8*
%ghost %dir %{_localstatedir}/lib/systemd/timesync/
%ghost %{_localstatedir}/lib/systemd/timesync/clock

%changelog
* Mon May 15 2023 Robert Scheck <robert@fedoraproject.org> 253.4-1
- Upgrade to 253.4 (and synchronize with systemd-253.4-1.fc39)

* Sun Feb 27 2022 Robert Scheck <robert@fedoraproject.org> 250.3-1
- Upgrade to 250.3 (and synchronize with systemd-250.3-6.fc37)

* Tue Dec 14 2021 Robert Scheck <robert@fedoraproject.org> 249.7-2
- Ship systemd-boot sub-package for x86_64 and aarch64 on RHEL 9

* Tue Dec 07 2021 Robert Scheck <robert@fedoraproject.org> 249.7-1
- Upgrade to 249.7 (and synchronize with systemd-249.7-3.fc36)

* Mon Jun 07 2021 Robert Scheck <robert@fedoraproject.org> 248.3-1
- Upgrade to 248.3 (and synchronize with systemd-248.3-1.fc35)

* Thu Jan 07 2021 Robert Scheck <robert@fedoraproject.org> 247.2-2
- Do not ship systemd.net-naming-scheme(7) anymore (#1913780)

* Sun Dec 20 2020 Robert Scheck <robert@fedoraproject.org> 247.2-1
- Upgrade to 247.2 (and synchronize with systemd-247.2-1.fc34)

* Sun Oct 11 2020 Robert Scheck <robert@fedoraproject.org> 246.6-1
- Upgrade to 246.6 (and synchronize with systemd-246.6-3.fc34)

* Sat Aug 08 2020 Robert Scheck <robert@fedoraproject.org> 246.1-1
- Upgrade to 246.1 (and synchronize with systemd-246.1-1.fc33)

* Tue Jun 02 2020 Robert Scheck <robert@fedoraproject.org> 245.6-1
- Upgrade to 245.6 (and synchronize with systemd-245.6-1.fc33)

* Mon Apr 20 2020 Robert Scheck <robert@fedoraproject.org> 245.5-1
- Upgrade to 245.5 (and synchronize with systemd-245.5-1.fc33)

* Sat Apr 04 2020 Robert Scheck <robert@fedoraproject.org> 245.4-1
- Upgrade to 245.4 (and synchronize with systemd-245.4-1.fc33)

* Fri Mar 27 2020 Robert Scheck <robert@fedoraproject.org> 245.3-1
- Upgrade to 245.3 (and synchronize with systemd-245.3-1.fc33)

* Sun Mar 08 2020 Robert Scheck <robert@fedoraproject.org> 245-1
- Upgrade to 245 (and synchronize with systemd-245-1.fc33)

* Tue Feb 11 2020 Robert Scheck <robert@fedoraproject.org> 244.1-2
- Work around failing test-mountpoint-util (systemd#11505)

* Sun Feb 09 2020 Robert Scheck <robert@fedoraproject.org> 244.1-1
- Initial spec file based on systemd-244.1-2.fc32 (#1789146)
