Name:      amazon-ec2-utils
Summary:   A set of tools for running in EC2
Version:   1.2
Release:   45%{?dist}
License:   MIT
Group:     System Tools

Source0:   ec2-metadata
Source1:   ec2udev-vbd
Source2:   51-ec2-hvm-devices.rules
Source3:   52-ec2-vcpu.rules
Source15:  ec2udev-vcpu
Source16:  60-cdrom_id.rules
Source22:  70-ec2-nvme-devices.rules
Source23:  ec2nvme-nsid
Source24:  ebsnvme-id
Source25:  51-ec2-xen-vbd-devices.rules
Source26:  53-ec2-read-ahead-kb.rules

URL:       https://github.com/aws/amazon-ec2-utils
BuildArch: noarch
Provides:  amazon-ec2-utils = %{version}-%{release}
Provides:  ec2-metadata
Obsoletes: ec2-metadata
Requires:  curl
BuildRequires: python3
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
ec2-utils contains a set of utilities for running in ec2.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT/opt/aws/bin
%if 0%{?amzn} >= 2 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/usr/lib/udev
%else
mkdir -p $RPM_BUILD_ROOT/lib/udev
%endif
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

install -m755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/sbin/
install -m755 %{SOURCE15} $RPM_BUILD_ROOT/sbin/
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m645 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE16} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE25} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE26} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/

#udev rules for nvme block devices and supporting scripts
install -m644 %{SOURCE22} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%if 0%{?amzn} >= 2 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
install -m755 %{SOURCE23} $RPM_BUILD_ROOT/usr/lib/udev
%else
install -m755 %{SOURCE23} $RPM_BUILD_ROOT/lib/udev
%endif
install -m755 %{SOURCE24} $RPM_BUILD_ROOT/sbin/

ln -sf %{_bindir}/ec2-metadata $RPM_BUILD_ROOT/opt/aws/bin/ec2-metadata

%check
%{__python3} -m py_compile %{SOURCE24}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/ec2-metadata
/opt/aws/bin/ec2-metadata
%if 0%{?amzn} >= 2 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
/usr/lib/udev/ec2nvme-nsid
%else
/lib/udev/ec2nvme-nsid
%endif
/sbin/ebsnvme-id
/sbin/ec2udev-vbd
/sbin/ec2udev-vcpu
%{_sysconfdir}/udev/rules.d/51-ec2-hvm-devices.rules
%{_sysconfdir}/udev/rules.d/51-ec2-xen-vbd-devices.rules
%{_sysconfdir}/udev/rules.d/52-ec2-vcpu.rules
%{_sysconfdir}/udev/rules.d/53-ec2-read-ahead-kb.rules
%{_sysconfdir}/udev/rules.d/60-cdrom_id.rules
%{_sysconfdir}/udev/rules.d/70-ec2-nvme-devices.rules

%changelog
* Thu Jul 14 2021 Sai Harsha <ssuryad@amazon.com> 1.2-45
- Disable timeout on EBS volumes

* Tue Apr 20 2021 Hailey Mothershead <hailmo@amazon.com> 1.2-44
- Add udev rule to increase read_ahead_kb when an NFS share is mounted

* Tue Mar 16 2021 Heath Petty <hpetty@amazon.com> 1.2-43
- Bump release

* Wed Oct 28 2020 Frederick Lefebvre <fredlef@amazon.com> 1.2-3
- Fix error in ebsnvme-id when printing to stderr
- Add testing of python syntax to spec file

* Mon May 18 2020 Suraj Jitindar Singh <surajjs@amazon.com> 1.2-2
- Import github version 1.3 of amazon-ec2-utils
- Update ec2-metadata documentation link
- Add manual pages for ec2-metadata and ebsnvme-id
- Fix copyright strings repo-wide
- Add udev rule to add by-path links for xen vbd devices

* Tue Feb 25 2020 Frederick Lefebvre <fredlef@amazon.com> 1.2-1
- Fix output of multi-line fields

* Wed Jan 15 2020 Frederick Lefebvre <fredlef@amazon.com> 1.1-1
- Add IMDSv2 support

* Tue Aug 27 2019 Anchal Agarwal <anchalag@amazon.com> 1.0-2
- Add udev rule to define lower timeout for instance storage volumes

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
