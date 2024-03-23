#
# Conditional build:
%bcond_with	fixed	# fixed point implementation

Summary:	Fraunhofer LC3plus Codec library
Summary(pl.UTF-8):	Biblioteka kodeka Fraunhofer LC3plus
Name:		libLC3plus
Version:	1.4.1
%define	gitref	887a9e1b3dd5e51462bc60b0400152eab51337ec
Release:	1
License:	ETSI IPR
Group:		Libraries
# search for newer releases at etsi.org
# also (unofficially?) mirrored at https://github.com/arkq/LC3plus/tags with nice versioning
Source0:	https://www.etsi.org/deliver/etsi_ts/103600_103699/103634/01.04.01_60/ts_103634v010401p0.zip
# NoSource0-md5:	9baaf65d7cf4f6cddfba278a7b8b85f2
# inspired by https://github.com/bluekitchen/libLC3plus and https://github.com/Quackdoc/libLC3plus
Source1:	CMakeLists.txt.in
Source2:	LC3plus.pc.in
Patch0:		%{name}-dirs.patch
NoSource:	0
URL:		https://www.iis.fraunhofer.de/en/ff/amm/communication/lc3.html
BuildRequires:	cmake >= 3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with fixed_point}
%define		srcdir	src/fixed_point
%else
%define		srcdir	src/floating_point
%endif

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

%{__sed} -e 's,@VERSION@,%{version},' %{SOURCE1} >LC3plus_src/%{srcdir}/CMakeLists.txt
cp -p %{SOURCE2} LC3plus_src/%{srcdir}

%build
%cmake -B build -S LC3plus_src/%{srcdir}

%{__make} -C build

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
%doc LC3plus_src/Readme.txt
%attr(755,root,root) %{_libdir}/libLC3plus.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libLC3plus.so
%{_includedir}/LC3plus
%{_pkgconfigdir}/lc3plus.pc
