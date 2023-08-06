#
# Conditional build:
%bcond_without	ssl	# SSL library

Summary:	A minimalistic C client library for Redis
Summary(pl.UTF-8):	Minimalistyczna biblioteka C klienta Redisa
Name:		hiredis
Version:	1.2.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/redis/hiredis/releases
Source0:	https://github.com/redis/hiredis/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	119767d178cfa79718a80c83e0d0e849
Patch0:		link.patch
URL:		https://github.com/redis/hiredis/
%{?with_ssl:BuildRequires:	openssl-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hiredis is a minimalistic C client library for the Redis database.

%description -l pl.UTF-8
Hiredis to minimalistyczna biblioteka C klienta bazy danych Redis.

%package devel
Summary:	Header files for hiredis C development
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania w C z użyciem hiredisa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files to develop applications using a
Redis database.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bazę danych Redis.

%package static
Summary:	Static hiredis library
Summary(pl.UTF-8):	Statyczna biblioteka hiredis
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hiredis library.

%description static -l pl.UTF-8
Statyczna biblioteka hiredis.

%package ssl
Summary:	SSL support library for hiredis
Summary(pl.UTF-8):	Biblioteka opsługi SSL dla biblioteki hiredis
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ssl
SSL support library for hiredis.

%description ssl -l pl.UTF-8
Biblioteka opsługi SSL dla biblioteki hiredis.

%package ssl-devel
Summary:	Header file for hiredis SSL library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki hiredis SSL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ssl = %{version}-%{release}
Requires:	openssl-devel

%description ssl-devel
Header file for hiredis SSL library.

%description ssl-devel -l pl.UTF-8
Plik nagłówkowy biblioteki hiredis SSL.

%package ssl-static
Summary:	Static hiredis SSL library
Summary(pl.UTF-8):	Statyczna biblioteka hiredis SSL
Group:		Development/Libraries
Requires:	%{name}-ssl-devel = %{version}-%{release}

%description ssl-static
Static hiredis SSL library.

%description ssl-static -l pl.UTF-8
Statyczna biblioteka hiredis SSL.

%package tools
Summary:	Test utility for hiredis
Summary(pl.UTF-8):	Narzędzie testowe do biblioteki hiredis
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
%if %{with ssl}
Requires:	%{name}-ssl = %{version}-%{release}
%endif

%description tools
Test utility for hiredis.

%description tools -l pl.UTF-8
Narzędzie testowe do biblioteki hiredis.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	DEBUG="" \
	LDFLAGS="%{rpmldflags}" \
	OPTIMIZATION="%{rpmcflags} %{rpmcppflags}" \
	PREFIX=%{_prefix} \
	LIBRARY_PATH=%{_lib} \
	%{?with_ssl:USE_SSL=1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBRARY_PATH=%{_lib} \
	%{?with_ssl:USE_SSL=1}

install -d $RPM_BUILD_ROOT%{_bindir}
install -p hiredis-test $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md COPYING README.md
%attr(755,root,root) %{_libdir}/libhiredis.so.1.1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhiredis.so
%dir %{_includedir}/hiredis
%{_includedir}/hiredis/adapters
%{_includedir}/hiredis/alloc.h
%{_includedir}/hiredis/async.h
%{_includedir}/hiredis/hiredis.h
%{_includedir}/hiredis/read.h
%{_includedir}/hiredis/sds.h
%{_includedir}/hiredis/sockcompat.h
%{_pkgconfigdir}/hiredis.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhiredis.a

%if %{with ssl}
%files ssl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhiredis_ssl.so.1.1.0

%files ssl-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhiredis_ssl.so
%{_includedir}/hiredis/hiredis_ssl.h
%{_pkgconfigdir}/hiredis_ssl.pc

%files ssl-static
%defattr(644,root,root,755)
%{_libdir}/libhiredis_ssl.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hiredis-test
