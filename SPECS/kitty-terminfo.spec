Name:           kitty-terminfo
Version:        0.38.0
Release:        1
URL:            https://sw.kovidgoyal.net/kitty
Summary:        The terminfo file for Kitty Terminal
License:        GPL-3.0-only
BuildArch:      noarch

Source0:        xterm-kitty
Source1:        LICENSE

Provides:       kitty-terminfo = %{version}-%{release}
Provides:       kitty-terminfo
Requires:       ncurses-base

%description
Cross-platform, fast, feature full, GPU based terminal emulator.

The terminfo file for Kitty Terminal.

%prep
# No preparation needed since this is a simple packaging

%build
# No build steps required for this package

%install
# Create destination directories
install -d %{buildroot}%{_datadir}/terminfo/x
install -d %{buildroot}%{_datadir}/licenses/kitty-terminfo

# Copy files to their destinations
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/terminfo/x/xterm-kitty
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/licenses/kitty-terminfo/LICENSE

%files
%license %{_datadir}/licenses/kitty-terminfo/LICENSE
%{_datadir}/terminfo/x/xterm-kitty
