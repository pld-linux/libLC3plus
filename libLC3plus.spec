Summary:	Fraunhofer LC3plus Codec library
Summary(pl.UTF-8):	Biblioteka kodeka Fraunhofer LC3plus
Name:		libLC3plus
Version:	1.3.6
%define	gitref	887a9e1b3dd5e51462bc60b0400152eab51337ec
Release:	1
# build system from BlueKitchen is BSD-licensed
License:	ETSI IPR + BSD
Group:		Libraries
NoSource0:	https://www.etsi.org/deliver/etsi_ts/103600_103699/103634/01.03.01_60/ts_103634v010301p0.zip
# NoSource0-md5:	3a3bc7c3ef7dcaede82caa73cd641b61
Source1:	https://github.com/bluekitchen/libLC3plus/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source1-md5:	ec70471250a579d418b728a76ff685c3
Patch0:		%{name}-dirs.patch
NoSource:	0
URL:		https://www.iis.fraunhofer.de/en/ff/amm/communication/lc3.html
BuildRequires:	cmake >= 3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LC3plus (Low Complexity Communication Codec Plus) codec library.

%description -l pl.UTF-8
Biblioteka kodeka LC3plus (Low Complexity Communication Codec Plus).

%package devel
Summary:	Header files for LC3plus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LC3plus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LC3plus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LC3plus.

%prep
%setup -q -n ETSI_Release

%{__mv} LC3plus_ETSI_src_* LC3plus_src

%{__tar} xf %{SOURCE1} -C LC3plus_src/src/fixed_point --strip-components=1
%patch0 -p1

%build
install -d build
cd build
%cmake ../LC3plus_src/src/fixed_point

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LC3plus_src/Readme.txt LC3plus_src/src/fixed_point/{LICENSE,README.md}
%attr(755,root,root) %{_libdir}/libLC3plus.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libLC3plus.so
%{_includedir}/LC3plus
%{_pkgconfigdir}/LC3plus.pc
