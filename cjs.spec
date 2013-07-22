%global _internal_version  fb472ad

Name:          cjs
Version:       1.34.0
Release:       0.2.git%{_internal_version}%{?dist}
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

BuildRequires: js-devel
BuildRequires: cairo-gobject-devel
BuildRequires: gobject-introspection-devel >= 1.31.22
BuildRequires: readline-devel
BuildRequires: dbus-glib-devel
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
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q -n linuxmint-%{name}-%{_internal_version}
sed -i -e 's@{ACLOCAL_FLAGS}@{ACLOCAL_FLAGS} -I m4@g' Makefile.am
echo "AC_CONFIG_MACRO_DIR([m4])" >> configure.ac

rm -f configure

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure --disable-static)

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
%{_libdir}/cjs-1.0/
%{_datadir}/cjs-1.0/

%files devel
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-1.0.pc
%{_libdir}/pkgconfig/cjs-dbus-1.0.pc
%{_libdir}/pkgconfig/cjs-internals-1.0.pc
%{_libdir}/*.so

%changelog
* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.2.gitfb472ad
- add isa tag to -devel sub-package

* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.1.gitfb472ad
- Inital build

