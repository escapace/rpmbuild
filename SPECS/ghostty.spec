# Adapted from kmf/dank-ws-copr (itself derived from Terra's EL10 spec).
# Ghostty 1.4 needs GTK >= 4.18 and libadwaita >= 1.7; EL10 ships 4.16 and
# 1.6, so stay on 1.3.x until EL10 rebases.

# https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
# https://ziglang.org/download/
%global zig_public_key RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U
%global zig_version 0.15.2
%global appid com.mitchellh.ghostty

# gtk4-layer-shell is not packaged for EL10, so the bundled copy is shipped
# privately in %%{_libdir}/ghostty. zig does not give it a build-id.
%global __provides_exclude_from ^%{_libdir}/ghostty/.*$
%global __requires_exclude ^libgtk4-layer-shell\\.so
%undefine _missing_build_ids_terminate_build

Name:           ghostty
Version:        1.3.1
Release:        1%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0) AND Apache-2.0
URL:            https://ghostty.org/
ExclusiveArch:  x86_64 aarch64

Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig
# Zig package cache for --system builds: fetch-zig-cache.sh with
# ZIG_GLOBAL_CACHE_DIR=ghostty-%%{version}-vendor, tmp/ removed
Source2:        ghostty-%{version}-vendor.tar.xz
# Upstream zig instead of EPEL's: EPEL zig is x86_64-only and its version
# floats (0.16 breaks ghostty 1.3.x)
Source3:        https://ziglang.org/download/%{zig_version}/zig-x86_64-linux-%{zig_version}.tar.xz
Source4:        https://ziglang.org/download/%{zig_version}/zig-x86_64-linux-%{zig_version}.tar.xz.minisig
Source5:        https://ziglang.org/download/%{zig_version}/zig-aarch64-linux-%{zig_version}.tar.xz
Source6:        https://ziglang.org/download/%{zig_version}/zig-aarch64-linux-%{zig_version}.tar.xz.minisig
# Don't install the Debug layer-shell built for the unit tests over the
# release one
Patch0:         ghostty-layer-shell-install.patch

BuildRequires:  gettext
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libX11-devel
BuildRequires:  minisign
BuildRequires:  ncurses
BuildRequires:  pandoc-cli
BuildRequires:  patchelf
BuildRequires:  pkgconfig
BuildRequires:  systemd-rpm-macros
BuildRequires:  wayland-devel
BuildRequires:  xz

Requires:       ghostty-terminfo
Requires:       gtk4
Requires:       libadwaita

%description
Ghostty is a fast, feature-rich, and cross-platform terminal emulator that
uses platform-native UI and GPU acceleration.

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%ifarch x86_64
/usr/bin/minisign -V -m %{SOURCE3} -x %{SOURCE4} -P %{zig_public_key}
%endif
%ifarch aarch64
/usr/bin/minisign -V -m %{SOURCE5} -x %{SOURCE6} -P %{zig_public_key}
%endif
%autosetup -p1
tar -xJf %{SOURCE2}
%ifarch x86_64
tar -xJf %{SOURCE3}
%endif
%ifarch aarch64
tar -xJf %{SOURCE5}
%endif
mv zig-%{_arch}-linux-%{zig_version} zig

%build
# zig build compiles and installs in one step; see %%install

%install
export ZIG_GLOBAL_CACHE_DIR="$PWD/zig-global-cache"
# Themes come from iTerm2-Color-Schemes and are not covered by the License
# tag; refer to the licenses of the individual themes upstream:
# https://github.com/mbadolato/iTerm2-Color-Schemes
# https://github.com/mbadolato/iTerm2-Color-Schemes/issues/638
# EL10's harfbuzz 8.4 is too old; under --system the other font/image
# libraries must be bundled too or harfbuzz's cimport still fails.
# gtk4-layer-shell is not packaged for EL10.
DESTDIR=%{buildroot} ./zig/zig build \
    --system "$PWD/ghostty-%{version}-vendor/p" \
    --prefix %{_prefix} \
    --prefix-lib-dir %{_libdir} \
    --build-id=sha1 \
    --summary all \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Dstrip=false \
    -Dversion-string=%{version} \
    -Demit-docs \
    -Demit-themes=true \
    -fno-sys=harfbuzz \
    -fno-sys=freetype \
    -fno-sys=fontconfig \
    -fno-sys=libpng \
    -fno-sys=zlib \
    -fno-sys=oniguruma \
    -fno-sys=gtk4-layer-shell

# Shipped separately by ghostty-terminfo
rm -rf %{buildroot}%{_datadir}/terminfo

# libghostty-vt is not shipped; the layer-shell headers are build-only
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/libghostty-vt.so*
rm -f %{buildroot}%{_datadir}/pkgconfig/libghostty-vt.pc

# zig leaves a relative RUNPATH into its build cache for the bundled lib
install -d %{buildroot}%{_libdir}/ghostty
mv %{buildroot}%{_libdir}/libgtk4-layer-shell.so %{buildroot}%{_libdir}/ghostty/
patchelf --set-rpath %{_libdir}/ghostty %{buildroot}%{_bindir}/ghostty

%find_lang %{appid}

%post
%systemd_user_post app-%{appid}.service

%preun
%systemd_user_preun app-%{appid}.service

%postun
%systemd_user_postun app-%{appid}.service

%files -f %{appid}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/ghostty/
%{_datadir}/%{name}/
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/bash-completion/completions/%{name}.bash
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/kio/servicemenus/%{appid}.desktop
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/nautilus-python/extensions/%{name}.py
%{_datadir}/nvim/site/*/%{name}.vim
%{_datadir}/vim/vimfiles/*/%{name}.vim
%{_datadir}/zsh/site-functions/_%{name}
%{_iconsdir}/hicolor/*/apps/%{appid}.png
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}.5*
%{_userunitdir}/app-%{appid}.service
