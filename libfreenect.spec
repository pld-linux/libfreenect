#
# Conditional build:
%bcond_without	opencv		# OpenCV wrapper
%bcond_without	openni2		# OpenNI2 driver
%bcond_without	python2		# Python 2.x extension
%bcond_without	python3		# Python 3.x extension
#
Summary:	Userspace driver for the Microsoft Kinect
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kontrolera Microsoft Kinect
Name:		libfreenect
Version:	0.6.2
Release:	3
License:	Apache v2.0 or GPL v2
Group:		Libraries
#Source0Download: https://github.com/OpenKinect/libfreenect/releases
Source0:	https://github.com/OpenKinect/libfreenect/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	78648c6eaa74f177a63f26b303247f6e
Patch0:		%{name}-link.patch
Patch1:		%{name}-install.patch
URL:		https://openkinect.org/wiki/Main_Page
BuildRequires:	cmake >= 3.1.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libusb-devel >= 1.0.18
%{?with_opencv:BuildRequires:	opencv-devel}
%if %{with python2}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-numpy-devel
%endif
%if %{with python3}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-numpy-devel
%endif
Requires:	libusb >= 1.0.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfreenect is a userspace driver for the Microsoft Kinect. It runs on
Linux, OSX, and Windows and supports:
- RGB and Depth Images
- Motors
- Accelerometer
- LED
- Audio

Notice: for the newer Kinect v2 (XBox One), use libfreenect 2 instead.

%description -l pl.UTF-8
libfreenect to sterownik przestrzeni użytkownika dla kontrolera
Microsoft Kinect. Działa na Linuksie, OSX oraz Windows i obsługuje:
- obrazy RGB z głębią
- silniki
- akcelerometr
- LED
- dźwięk

Uwaga: do nowszego Kinecta v2 (XBox One) należy używać libfreenect2.

%package fakenect
Summary:	Fakenect mock library
Summary(pl.UTF-8):	Biblioteka atrapy fakenect
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description fakenect
Fakenect mock library.

%description fakenect -l pl.UTF-8
Biblioteka atrapy fakenect.

%package opencv
Summary:	OpenCV wrapper for libfreenect
Summary(pl.UTF-8):	Obudowanie OpenCV do biblioteki libfreenect
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description opencv
OpenCV wrapper for libfreenect.

%description opencv -l pl.UTF-8
Obudowanie OpenCV do biblioteki libfreenect.

%package -n OpenNI2-driver-freenect
Summary:	OpenNI2 driver for Microsoft Kinect
Summary(pl.UTF-8):	Sterownik do kontrolera Microsoft Kinect dla platformy OpenNI2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenNI2

%description -n OpenNI2-driver-freenect
OpenNI2 driver for Microsoft Kinect.

%description -n OpenNI2-driver-freenect -l pl.UTF-8
Sterownik do kontrolera Microsoft Kinect dla platformy OpenNI2.

%package devel
Summary:	Header files for libfreenect libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek libfreenect
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.18

%description devel
Header files for libfreenect libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libfreenect.

%package static
Summary:	Static libfreenect libraries
Summary(pl.UTF-8):	Statyczne biblioteki libfreenect
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libfreenect libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libfreenect.

%package -n python-freenect
Summary:	Python 2 interface to libfreenect
Summary(pl.UTF-8):	Interfejs Pythona 2 do libfreenect
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-freenect
Python 2 interface to libfreenect.

%description -n python-freenect -l pl.UTF-8
Interfejs Pythona 2 do libfreenect.

%package -n python3-freenect
Summary:	Python 3 interface to libfreenect
Summary(pl.UTF-8):	Interfejs Pythona 3 do libfreenect
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs

%description -n python3-freenect
Python 3 interface to libfreenect.

%description -n python3-freenect -l pl.UTF-8
Interfejs Pythona 3 do libfreenect.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '1s,/usr/bin/env python2,%{__python},' src/fwfetcher.py

%build
install -d build
cd build
%cmake .. \
	%{?with_opencv:-DBUILD_CV=ON} \
	-DBUILD_EXAMPLES=OFF \
	%{?with_python2:-DBUILD_PYTHON2=ON} \
	%{?with_python3:-DBUILD_PYTHON3=ON} \
	%{?with_openni2:-DBUILD_OPENNI2_DRIVER=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/fwfetcher.py \
	$RPM_BUILD_ROOT%{_datadir}/libfreenect

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	opencv -p /sbin/ldconfig
%postun	opencv -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libfreenect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreenect.so.0
%attr(755,root,root) %{_libdir}/libfreenect_sync.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreenect_sync.so.0
%dir %{_datadir}/libfreenect
%{_datadir}/libfreenect/fwfetcher.py

%files fakenect
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fakenect
%attr(755,root,root) %{_bindir}/fakenect-record
%dir %{_libdir}/fakenect
%attr(755,root,root) %{_libdir}/fakenect/libfakenect.so*
%{_mandir}/man1/fakenect.1*
%{_mandir}/man1/fakenect-record.1*

%if %{with opencv}
%files opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/freenect-cvdemo
%attr(755,root,root) %{_libdir}/libfreenect_cv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreenect_cv.so.0
%attr(755,root,root) %{_libdir}/libfreenect_cv.so
%endif

%if %{with openni2}
%files -n OpenNI2-driver-freenect
%defattr(644,root,root,755)
%dir %{_libdir}/OpenNI2-FreenectDriver
%attr(755,root,root) %{_libdir}/OpenNI2-FreenectDriver/libFreenectDriver.so*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreenect.so
%attr(755,root,root) %{_libdir}/libfreenect_sync.so
%{_includedir}/libfreenect
%{_pkgconfigdir}/libfreenect.pc
%{_datadir}/libfreenect/libfreenectConfig.cmake

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreenect.a
%{_libdir}/libfreenect_sync.a

%if %{with python2}
%files -n python-freenect
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/freenect.so
%endif

%if %{with python3}
%files -n python3-freenect
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/freenect.so
%endif
