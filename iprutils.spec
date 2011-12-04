Summary: Utilities for the IBM Power Linux RAID adapters
Name:    iprutils
Version: 2.2.20
Release: 1%{?dist}
License: CPL
Group:   System Environment/Base
URL:     http://sourceforge.net/projects/iprdd/

Source0: http://downloads.sourceforge.net/project/iprdd/iprutils%20for%202.6%20kernels/%{version}/%{name}-%{version}-src.tgz

# missing man page
Source1: iprdbg.8.gz

Patch0:  %{name}-cflags.patch
Patch1:  %{name}-initscripts.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: ppc64

Requires: /sbin/pidof

BuildRequires: libsysfs-devel
BuildRequires: pciutils-devel
BuildRequires: ncurses-devel
BuildRequires: libcap-devel
BuildRequires: kernel-devel

Obsoletes: ipr-utils

%description
Provides a suite of utilities to manage and configure SCSI devices
supported by the ipr SCSI storage device driver.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .cflags
%patch1 -p1 -b .initscripts

%build
CFLAGS="%{optflags}" %{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} INSTALL_MOD_PATH=%{buildroot} install

%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -m 0755 init.d/iprinit %{buildroot}%{_sysconfdir}/rc.d/init.d/iprinit
%{__install} -m 0755 init.d/iprdump %{buildroot}%{_sysconfdir}/rc.d/init.d/iprdump
%{__install} -m 0755 init.d/iprupdate %{buildroot}%{_sysconfdir}/rc.d/init.d/iprupdate

# missing man page
%{__install} -m 0755 %SOURCE1 %{buildroot}%{_mandir}/man8/

# move all binaries from /sbin to /usr/sbin and
# make symbolink links for all binaries in /sbin to /usr/sbin
mkdir %{buildroot}/usr/sbin
for file in iprconfig iprdbg iprdump iprinit iprupdate; do
  mv %{buildroot}/sbin/$file %{buildroot}/usr/sbin/$file
  ln -s /usr/sbin/$file %{buildroot}/sbin/$file
done


%post
/sbin/chkconfig --add iprdump
/sbin/chkconfig --add iprupdate
/sbin/chkconfig --add iprinit

%preun
/sbin/chkconfig --del iprdump
/sbin/chkconfig --del iprupdate
/sbin/chkconfig --del iprinit

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README LICENSE
/sbin/*
/usr/sbin/*
%{_mandir}/man*/*
%{_sysconfdir}/rc.d/init.d/*

%changelog
* Mon Apr 12 2010 Roman Rakus <rrakus@redhat.com> - 2.2.20-1
- Update to 2.2.20
  Resolves: #581001

* Thu Feb 11 2010 Roman Rakus <rrakus@redhat.com> 2.2.18-3
- Added missing man page
- moved files from /sbin to /usr/sbin and made symlinks
  Resolves: #558784

* Mon Jan 11 2010 Roman Rakus rrakus@redhat.com 2.2.18-2
- We don't support ppc
  Resolves: #553793

* Wed Nov 04 2009 Roman Rakus <rrakus@redhat.com> - 2.2.18-1
- Version 2.2.18
- Corrected initscripts

* Thu Sep 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.17-1
- Version 2.2.17

* Mon Aug 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.16-1
- Bump to version 2.2.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 2 2009 Will Woods <wwoods@redhat.com> - 2.2.13-2
- Fix iprdump startup - #483340
- iprutils-swab-moved.patch - fix compilation with 2.6.29 kernels (#483643)

* Fri Nov 21 2008 Roman Rakus <rrakus@redhat.com> - 2.2.13-1
- New upstream version

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-6
- Fixed ExclusiveArch tag

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-5
- Fixed chkconfig issue - #453165

* Wed Apr  9 2008 Roman Rakus <rrakus@redhat.cz> - 2.2.8-4
- Rewrited initscripts for satisfying LSB spec

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 2.2.8-2
- Rebuild for gcc-4.3

* Fri Nov 16 2007 David Cantrell <dcantrell@redhat.com> - 2.2.8-1
- Upgrade to latest upstream release

* Mon Oct  1 2007 Jeremy Katz <katzj@redhat.com> - 2.2.6-3
- don't require redhat-lsb (#252343)

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 2.2.6-2
- Rebuild

* Thu May 17 2007 Paul Nasrat <pnasrat@redhat.com> - 2.2.6-1
- Update to latest upstream

* Thu Jul 13 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.5-1
- New upstream version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.4-3.1
- rebuild

* Mon Jul 10 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-3
- Add redhat-lsb requires

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 2.1.4-2
- Rebuild against new sysfsutils

* Mon Jun 26 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 23 2005 Paul Nasrat <pnasrat@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Use RPM_OPT_FLAGS

* Tue Aug 02 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.15.3-1
- update to 2.0.15.3-1

* Wed May 11 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.14.2-1
- update to 2.0.14.2 (#156934)

* Thu Feb 24 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.7-1
- Update to 2.0.13.7 (#144654)
- Project moved location to sourceforge

* Mon Jan 03 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.5-1
- Update to 2.0.13.5 (#143593)

* Wed Dec  8 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.4-2
- link dynamically to sysfsutils instead of statically (#142310)

* Wed Dec 08 2004 Paul Nasrat <pnasrat@redhat.com> 2.0.13.4-1
- update to 2.0.13.4 (#142164)

* Fri Dec  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.3-1
- update to 2.0.13.3 (#141707)

* Mon Nov 15 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.2-1
- update to 2.0.13.2 (#139083)
  - fix firmware upload for firmware in /lib instead of /usr/lib
  - fix sysfs race

* Wed Oct  6 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13-1
- update to 2.0.13 (#128996)

* Tue Aug  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.12-1
- update to 2.0.12
- include a copy of libsysfs to build

* Tue Jun 15 2004 Jeremy Katz <katzj@redhat.com> - 1.0.7-1
- update to 1.0.7 (#125988)

* Tue May 11 2004 Jeremy Katz <katzj@redhat.com> - 1.0.5-3
- obsolete ipr-utils (old package name)

* Thu Mar 25 2004 Jeremy Katz <katzj@redhat.com> 1.0.5-2
- 1.0.5
- some spec file tweaks

* Tue Nov 25 2003 Brian King <brking@us.ibm.com> 1.0.3-2
- Fixed segmentation fault in iprupdate
