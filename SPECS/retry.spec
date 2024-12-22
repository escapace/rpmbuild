Name:      retry
Version:   2
Release:   1
Summary:   Retry a command with exponential backoff
License:   MIT
Group:     System Tools

Source0:   retry

BuildArch: noarch
Provides:  retry = %{version}-%{release}
Provides:  retry
Requires:  bash

%description
Retry a command with exponential backoff

%prep
# we have no source, so nothing here

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/retry
