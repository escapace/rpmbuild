Summary:        For Easy Rule Making
Name:           ferm
Version:        2.7
Release:        1%{?dist}
Group:          Applications/System
License:        GPLv2+
Source:         http://ferm.foo-projects.org/download/%{version}/%{name}-%{version}.tar.gz
Source1:        ferm.service
URL:            http://ferm.foo-projects.org/

BuildArchitectures:     noarch
BuildRequires:          perl-generators
BuildRequires:          perl(Data::Dumper)
BuildRequires:          perl(File::Spec)
BuildRequires:          systemd
BuildRequires:          /usr/bin/pod2text
BuildRequires:          /usr/bin/pod2man
BuildRequires:          /usr/bin/pod2html
BuildRequires:          make
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%define _unpackaged_files_terminate_build 0

%description
Ferm is a tool to maintain complex firewalls, without having the
trouble to rewrite the complex rules over and over again. Ferm
allows the entire firewall rule set to be stored in a separate
file, and to be loaded with one command. The firewall configuration
resembles structured programming-like language, which can contain
levels and lists.

%prep
%setup -q

%build

%install
rm -Rf $RPM_BUILD_ROOT

make install PREFIX=$RPM_BUILD_ROOT%{_prefix} DOCDIR=$RPM_BUILD_ROOT%{_pkgdocdir} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1

install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.rst TODO NEWS examples/
%{_mandir}/man1/*
%{_sbindir}/import-ferm
%{_sbindir}/ferm
