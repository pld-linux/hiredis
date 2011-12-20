Summary:	A minimalistic C client library for Redis
Name:		hiredis
Version:	0.10.0
Release:	1
License:	BSD
Group:		Libraries
URL:		https://github.com/antirez/hiredis
Source0:	https://github.com/antirez/hiredis/tarball/v%{version}/%{name}-%{version}.tgz
# Source0-md5:	66edb31cdc39c94978ddf98538259d72
Patch0:		link.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hiredis is a minimalistic C client library for the Redis database.

%package devel
Summary:	Header files and libraries for hiredis C development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries to
develop applications using a Redis database.

%prep
%setup -qc
mv *-%{name}-*/* .
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	DEBUG="" \
	LDFLAGS="-L. %{rpmldflags}" \
	OPTIMIZATION="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="cp -a" \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_bindir}
install -p hiredis-example hiredis-test $RPM_BUILD_ROOT%{_bindir}

find $RPM_BUILD_ROOT -name *.a | xargs rm -v

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING TODO
%attr(755,root,root) %{_bindir}/hiredis-example
%attr(755,root,root) %{_bindir}/hiredis-test
%attr(755,root,root) %{_libdir}/libhiredis.so.*.*.*
%ghost %{_libdir}/libhiredis.so.0

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_includedir}/%{name}
%{_libdir}/libhiredis.so
