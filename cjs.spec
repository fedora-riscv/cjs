%global _internal_version  7a65cc7

Name:          cjs
Epoch:         1
Version:       2.4.0
Release:       0.1.git%{_internal_version}%{?dist}
Summary:       Javascript Bindings for Cinnamon

Group:         System Environment/Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           http://cinnamon.linuxmint.com
# To generate tarball
# wget https://github.com/linuxmint/cjs/archive/%%{version}.tar.gz -O cjs-%%{version}.tar.gz
# for git
# wget https://github.com/linuxmint/cjs/tarball/%%{_internal_version} -O cjs-%%{version}.git%%{_internal_version}.tar.gz
Source0:       http://leigh123linux.fedorapeople.org/pub/cjs/source/cjs-%{version}.git%{_internal_version}.tar.gz
#Source0:       http://leigh123linux.fedorapeople.org/pub/cjs/source/cjs-%{version}.tar.gz

Patch0:         0001-rename.patch

BuildRequires: pkgconfig(mozjs-24)
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.39.3
BuildRequires: readline-devel
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: intltool
# Bootstrap requirements
BuildRequires: gtk-doc
BuildRequires: gnome-common

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary: Tests for the cjs package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description tests
The cjs-tests package contains tests that can be used to verify
the functionality of the installed cjs package.

%prep
%setup -q -n linuxmint-cjs-%{_internal_version}
%patch0 -p1
sed -i -e 's@{ACLOCAL_FLAGS}@{ACLOCAL_FLAGS} -I m4@g' Makefile.am
echo "AC_CONFIG_MACRO_DIR([m4])" >> configure.ac
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static --enable-installed-tests
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags} V=1

%install
%make_install

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LGPL NEWS README
%{_bindir}/cjs
%{_bindir}/cjs-console
%{_libdir}/*.so.*
%{_libdir}/cjs/

%files devel
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-*1.0.pc
%{_libdir}/*.so

%files tests
%{_libexecdir}/cjs/
%{_datadir}/installed-tests/

%changelog
* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.0-0.1.git7a65cc7
- update to latest git
- swap to mozjs24

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.2-1
- update to 2.2.2

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:2.2.1-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.1-1
- update to 2.2.1

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.0-1
- update to 2.2.0

* Wed Oct 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:2.0.0-1
- update to 2.0.0

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:1.9.1-2
- add epoch to -devel

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:1.9.1-1
- update to 1.9.1
- add epoch

* Sun Sep 15 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.5.gita30f982
- update to latest git

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.4.gitfb472ad
- rebuilt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34.0-0.3.gitfb472ad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.2.gitfb472ad
- add isa tag to -devel sub-package

* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.1.gitfb472ad
- Inital build

