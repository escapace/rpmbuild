%if 0%{?el8}
# see https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
# EPEL 8's %%cmake defaults to in-source build, which neovim does not support
%undefine __cmake_in_source_build
%endif

Name:           neovim
# Version:        0.10.0~dev.3117.g4e5c633ed
Version:        0.10.0
Release:        1%{?dist}

License:        Apache-2.0 AND Vim
Summary:        Vim-fork focused on extensibility and agility
Url:            https://neovim.io

Source0:        nightly.tar.gz
Source1:        sysinit.vim

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  gperf
BuildRequires:  jemalloc-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  unzip
# need the build with the fix for the resize buffer issue
Suggests:       (python2-neovim if python2)
Suggests:       (python3-neovim if python3)
# XSel provides access to the system clipboard
# Recommends:     xsel
# Recommends:     wl-clipboard

%description
Neovim is a refactor - and sometimes redactor - in the tradition of
Vim, which itself derives from Stevie. It is not a rewrite, but a
continuation and extension of Vim. Many rewrites, clones, emulators
and imitators exist; some are very clever, but none are Vim. Neovim
strives to be a superset of Vim, notwithstanding some intentionally
removed misfeatures; excepting those few and carefully-considered
excisions, Neovim is Vim. It is built for users who want the good
parts of Vim, without compromise, and more.

%prep
# %setup -T -b 0 -q -n neovim-nightly
%setup -T -b 0 -q -n neovim-0.10.0

%build

make distclean
make CMAKE_BUILD_TYPE=Release \
     CMAKE_EXTRA_FLAGS="-DCMAKE_INSTALL_PREFIX=%{_prefix} -DENABLE_JEMALLOC=ON -DUSE_BUNDLED=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr -DINCLUDE_INSTALL_DIR:PATH=/usr/include -DLIB_INSTALL_DIR:PATH=/usr/lib64 -DSYSCONF_INSTALL_DIR:PATH=/etc -DSHARE_INSTALL_PREFIX:PATH=/usr/share -DLIB_SUFFIX=64"

%install
make install DESTDIR=%{buildroot}

install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    runtime/nvim.desktop
install -d -m0755 %{buildroot}%{_datadir}/pixmaps
install -m0644 runtime/nvim.png %{buildroot}%{_datadir}/pixmaps/nvim.png

%fdupes %{buildroot}%{_datadir}/
# Fix exec bits
find %{buildroot}%{_datadir} \( -name "*.bat" -o -name "*.awk" \) \
    -print -exec chmod -x '{}' \;
%find_lang nvim

%files -f nvim.lang
%license LICENSE.txt
%doc CONTRIBUTING.md README.md
%{_bindir}/nvim

%{_mandir}/man1/nvim.1*
%{_datadir}/applications/nvim.desktop
%{_datadir}/pixmaps/nvim.png
%{_datadir}/icons/hicolor/128x128/apps/nvim.png

%dir %{_datadir}/nvim
%{_datadir}/nvim/sysinit.vim

%{_datadir}/nvim/runtime/
%{_libdir}/nvim/

%changelog
* Wed Mar 27 2024 Aron Griffis <aron@scampersand.com> - 0.10.0~dev.2709.g00e9c6955-1
- Nightly build from git master

* Thu Sep 07 2023 Andreas Schneider <asn@redhat.com> - 0.9.2-1
- Update to version 0.9.2
  * For changelog see `:help news`

* Mon Aug 28 2023 LuK1337 <priv.luk@gmail.com> - 0.9.1-4
- Improve spec template

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Andreas Schneider <asn@redhat.com> - 0.9.1-2
- Build with new libluv-devel

* Wed May 31 2023 Andreas Schneider <asn@redhat.com> - 0.9.1-1
- Update to version 0.9.1
  * For changelog see `:help news`

* Tue May 02 2023 Andreas Schneider <asn@redhat.com> - 0.9.0-3
- Improve semantic token performance
- related: rhbz#2188229 - Fix applying patches

* Fri Apr 21 2023 Andreas Schneider <asn@redhat.com> - 0.9.0-2
- resolves: rhbz#2188229 - Fix buffer overflow for user command

* Fri Apr 07 2023 Andreas Schneider <asn@redhat.com> - 0.9.0-1
- Update to version 0.9.0
  * For changelog see `:help news`

* Mon Mar 27 2023 Andreas Schneider <asn@redhat.com> - 0.8.3-4
- resolves: rhbz#2181836 - Fix snprintf buffer overflow with tags

* Sat Mar 25 2023 Andreas Schneider <asn@redhat.com> - 0.8.3-3
- resolves: rhbz#2165805 - Fix snprintf buffer overflow

* Sun Mar 05 2023 Andreas Schneider <asn@redhat.com> - 0.8.3-2
- Update License to SPDX expression
- Update spec template for auto(release|changelog)

* Thu Feb 02 2023 Andreas Schneider <asn@redhat.com> - 0.8.3-1
- Update to version 0.8.3
  * https://github.com/neovim/neovim/releases/tag/v0.8.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 Andreas Schneider <asn@redhat.com> - 0.8.2-1
- Update to version 0.8.2
  * https://github.com/neovim/neovim/releases/tag/v0.8.2

* Mon Nov 14 2022 Andreas Schneider <asn@redhat.com> - 0.8.1-1
- Update to version 0.8.1
  * https://github.com/neovim/neovim/releases/tag/v0.8.1

* Fri Sep 30 2022 Andreas Schneider <asn@redhat.com> - 0.8.0-1
- Update to version 0.8.0
  * https://github.com/neovim/neovim/releases/tag/v0.8.0

* Wed Sep 21 2022 Andreas Schneider <asn@redhat.com> - 0.7.2-4
- Build with libvterm 0.3

* Thu Aug 25 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.7.2-3
- Enforce the minimum tree-sitter version at runtime (Fixes: rhbz#2100577)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 26 2022 Andreas Schneider <asn@redhat.com> - 0.7.2-1
- Update to version 0.7.2

* Fri Apr 15 2022 Andreas Schneider <asn@redhat.com> - 0.7.0-1
- Update to version 0.7.0

* Thu Mar 17 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.6.1-4
- Support building on EPEL 8

* Wed Feb 09 2022 Andreas Schneider <asn@redhat.com> - 0.6.1-3
- Fix libvterm 0.2 support

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 01 2022 Andreas Schneider <asn@redhat.com> - 0.6.1-1
- Update to version 0.6.1

* Wed Dec 01 2021 Andreas Schneider <asn@redhat.com> - 0.6.0-1
- Update to version 0.6.0

* Thu Oct 28 2021 Andreas Schneider <asn@redhat.com> - 0.5.1-2
- Use luajit also on aarch64

* Mon Sep 27 2021 Andreas Schneider <asn@redhat.com> - 0.5.1-1
- Update to version 0.5.1

* Fri Jul 30 2021 Andreas Schneider <asn@redhat.com> - 0.5.0-5
- Build with luajit2.1-luv when we use luajit

* Fri Jul 30 2021 Andreas Schneider <asn@redhat.com> - 0.5.0-4
- resolves: rhbz#1983288 - Build with lua-5.1 on platforms where luajit is not
  available

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Andreas Schneider <asn@redhat.com> - 0.5.0-2
- Fixed execute bits of bat and awk files

* Mon Jul 05 2021 Andreas Schneider <asn@redhat.com> - 0.5.0-1
- Raise BuildRequires for some libraries

* Sat Jul 03 2021 Andreas Schneider <asn@redhat.com> - 0.5.0-0
- Update to version 0.5.0
  * https://github.com/neovim/neovim/releases/tag/v0.5.0

* Mon Apr 19 2021 Andreas Schneider <asn@redhat.com> - 0.4.4-5
- resolves: #1909495 - Load installed vim plugins
- Make build reproducible

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep  1 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.4.4-3
- When using Lua 5.4, also pull in lua-bit32 at installation

* Mon Aug 31 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.4.4-2
- Do not hardcode Lua version
- Patch to support detecting Lua 5.4
- Pull in lua-bit32 when built against Lua 5.4

* Wed Aug 05 2020 Andreas Schneider <asn@redhat.com> - 0.4.4-1
- Update to version 0.4.4
- Use new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 22 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.4.3-6
- Update build requirements

* Sun Feb 23 2020 Andreas Schneider <asn@redhat.com> - 0.4.3-5
- Update to upstream patchset for -fno-common

* Mon Feb 17 2020 Andreas Schneider <asn@redhat.com> - 0.4.3-4
- Update patchset for -fno-common

* Mon Feb 17 2020 Andreas Schneider <asn@redhat.com> - 0.4.3-3
- resolves: #1799680 - Fix -fno-common issues

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Andreas Schneider <asn@redhat.com> - 0.4.3-1
- Update to version 0.4.3

* Mon Oct 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.2-2
- Fix glitches for terminals sayin xterm but not xterm

* Thu Oct 03 2019 Andreas Schneider <asn@redhat.com> - 0.4.2-1
- Update to version 0.4.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 05 2019 Andreas Schneider <asn@redhat.com> - 0.3.8-1
- Update to version 0.3.8

* Wed May 29 2019 Andreas Schneider <asn@redhat.com> - 0.3.7-1
- Update to version 0.3.7

* Wed May 29 2019 Andreas Schneider <asn@redhat.com> - 0.3.6-1
- resolves: #1714849 - Update to version 0.3.6

* Tue May 07 2019 Andreas Schneider <asn@redhat.com> - 0.3.5-1
- resolves: #1703867 - Update to version 0.3.5

* Wed Mar 06 2019 Aron Griffis <aron@scampersand.com> - 0.3.4-1
- Update to version 0.3.4 with luajit, rhbz #1685781

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.3-2
- Remove Recommends: xterm

* Sun Jan 06 2019 Andreas Schneider <asn@redhat.com> - 0.3.3-1
- Update to version 0.3.3

* Wed Jan 02 2019 Andreas Schneider <asn@redhat.com> - 0.3.2-1
- Update to version 0.3.2

* Fri Aug 10 2018 Andreas Schneider <asn@redhat.com> - 0.3.1-1
- Update to version 0.3.1

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.3.0-6
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-5
- Rebuild for new binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-4
- Disable jemalloc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Andreas Schneider <asn@redhat.com> - 0.3.0-2
- resolves: #1592474 - Add jemalloc as a requirement

* Mon Jun 11 2018 Andreas Schneider <asn@redhat.com> - 0.3.0-1
- Update to version 0.3.0
- resolves: #1450624 - Set default python_host_prog

* Sat May 26 2018 Andreas Schneider <asn@redhat.com> - 0.2.2-3
- Rebuild against unibilium-2.0.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 23 2017 Andreas Schneider <asn@redhat.com> - 0.2.2-1
- resolves: #1510899 - Update to version 0.2.2

* Wed Nov 08 2017 Andreas Schneider <asn@redhat.com> - 0.2.1-1
- resolves: #1510762 - Update to version 0.2.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Than Ngo <than@redhat.com> 0.2.0-3
- fixed bz#1451143, ppc64/le build failure

* Mon May 15 2017 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.2.0-2
- Adjust spec for building on epel7

* Mon May 08 2017 Andreas Schneider <asn@redhat.com> - 0.2.0-1
- resolves: #1447481 - Update to 0.2.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Filip Szymański <fszymanski at, fedoraproject.org> - 0.1.7-6
- Add RPM spec file template

* Thu Dec 08 2016 Filip Szymański <fszymanski at, fedoraproject.org> - 0.1.7-5
- Add recommends for python2-neovim and xsel
- Remove unused CMake options
- Use %%make_build and %%make_install macros
- Remove unnecessary %%defattr directive

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-4
- Set license file correctly

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-3
- Update build requires

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-2
- Add Recommends for python3-neovim
- Use 'bit32' from lua 5.3

* Mon Nov 28 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-1
- Update to version 0.1.7

* Tue Nov 15 2016 Andreas Schneider <asn@redhat.com> - 0.1.6-2
- Removed Group:
- Removed BuildRoot:

* Thu Nov 10 2016 Andreas Schneider <asn@redhat.com> - 0.1.6-1
- Initial version 0.1.6
