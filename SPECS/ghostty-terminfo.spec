Name:           ghostty-terminfo
Version:        1.0.0
Release:        1
URL:            https://github.com/ghostty-org/ghostty
Summary:        The terminfo file for ghostty Terminal
License:        MIT
BuildArch:      noarch

Source0:        xterm-ghostty
Source1:        LICENSE

Provides:       ghostty-terminfo = %{version}-%{release}
Provides:       ghostty-terminfo
Requires:       ncurses-base

%description
Terminal emulator that uses platform-native UI and GPU acceleration.

The terminfo file for ghostty Terminal.

%prep
# No preparation needed since this is a simple packaging

%build
# No build steps required for this package

%install
# Create destination directories
install -d %{buildroot}%{_datadir}/terminfo/x
install -d %{buildroot}%{_datadir}/licenses/ghostty-terminfo

# Copy files to their destinations
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/licenses/ghostty-terminfo/LICENSE

%files
%license %{_datadir}/licenses/ghostty-terminfo/LICENSE
%{_datadir}/terminfo/x/xterm-ghostty
