%global _hardened_build 1

Name:           tmux
Version:        3.2a
Release:        3%{?dist}
Summary:        A terminal multiplexer

# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            https://tmux.github.io/
Source0:        https://github.com/tmux/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
# Examples has been removed - so include the bash_completion here
Source1:        bash_completion_tmux.sh

BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  libevent-devel
BuildRequires:  libutempter-devel

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
%autosetup

%build
%configure
%make_build


%install
%make_install
# bash completion
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/tmux

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    touch %{_sysconfdir}/shells
  fi
  for binpath in %{_bindir} /bin; do
    if ! grep -q "^${binpath}/tmux$" %{_sysconfdir}/shells; then
       (cat %{_sysconfdir}/shells; echo "$binpath/tmux") > %{_sysconfdir}/shells.new
       mv %{_sysconfdir}/shells{.new,}
    fi
  done
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -e '\!^%{_bindir}/tmux$!d' -e '\!^/bin/tmux$!d' < %{_sysconfdir}/shells > %{_sysconfdir}/shells.new
  mv %{_sysconfdir}/shells{.new,}
fi

%files
%doc CHANGES
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*
%{_datadir}/bash-completion/completions/tmux
