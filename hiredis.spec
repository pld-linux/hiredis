Summary:	A minimalistic C client library for Redis
Summary(pl.UTF-8):	Minimalistyczna biblioteka C klienta Redisa
Name:		hiredis
Version:	0.11.0
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://github.com/redis/hiredis/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a78e34702c6e34cc44126b178ed82225
Patch0:		link.patch
URL:		https://github.com/redis/hiredis/
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

%prep
%setup -qc
mv *-%{name}-*/* .
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	DEBUG="" \
	LDFLAGS="-L. %{rpmldflags}" \
	OPTIMIZATION="%{rpmcflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="cp -a" \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_bindir}
install -p hiredis-example hiredis-test $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md COPYING README.md
%attr(755,root,root) %{_bindir}/hiredis-example
%attr(755,root,root) %{_bindir}/hiredis-test
%attr(755,root,root) %{_libdir}/libhiredis.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libhiredis.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhiredis.so
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libhiredis.a
