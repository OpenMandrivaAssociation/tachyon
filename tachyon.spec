%ifarch alpha ppc64 sparc64 x86_64
%define target linux-64
%else
%define target linux
%endif

%define variants thr thr-ogl
%define beta b6

Summary: Parallel / Multiprocessor Ray Tracing System
Name: tachyon
Version: 0.99
Release: 0.7.%{beta}%{?dist}
URL: http://jedi.ks.uiuc.edu/~johns/raytracer/
Source0: http://jedi.ks.uiuc.edu/~johns/raytracer/files/%{version}%{beta}/%{name}-%{version}%{beta}.tar.gz
# taken from Debian package
Source1: %{name}.1
Source2: %{name}.rpmlintrc
Patch0: %{name}-rpm.patch
Patch1: %{name}-shared.patch
License: BSD with advertising
BuildRequires: jpeg-devel
BuildRequires: latex2html
BuildRequires: pkgconfig(gl)
BuildRequires: png-devel
BuildRequires: texlive

%description
A portable, high performance parallel ray tracing system with
multithreaded implementation.

%package libs
Summary: Parallel / Multiprocessor Ray Tracing System library

%description libs
A portable, high performance parallel ray tracing system with
multithreaded implementation.  Tachyon is built as a C callable
library, which can be used with the included demo programs or within
your own application.

This package contains the shared library.

%package gl
Summary: Parallel / Multiprocessor Ray Tracing System with OpenGL display
Provides: %{name} = %{version}-%{release}

%description gl
A portable, high performance parallel ray tracing system with
multithreaded implementation.

This package contains OpenGL-enabled build.

%package devel
Summary: Development files for tachyon
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains development headers and libraries for developing
with tachyon.

%package docs
Summary: Documentation and example scenes for tachyon
Requires: %{name} = %{version}-%{release}

%description docs
This package contains documentation and example scenes for rendering
with tachyon.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .r
%patch1 -p1 -b .shared
find . -name CVS | xargs %{__rm} -r
# executable sources
chmod 644 src/hash.{c,h}
chmod 644 src/pngfile.h
chmod 644 demosrc/spaceball.c
chmod 644 demosrc/trackball.{c,h}
chmod 644 scenes/imaps/*

%build
pushd unix
for variant in %{variants} ; do
  %{__make} %{?_smp_mflags} OPTFLAGS="$RPM_OPT_FLAGS" %{target}-$variant
done
popd

pushd docs
%{__make} html pdf ps
popd

%install
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_libdir},{%{_datadir},%{_includedir}}/tachyon,%{_mandir}/man1}
for variant in %{variants} ; do
  install -pm755 compile/%{target}-$variant/tachyon $RPM_BUILD_ROOT%{_bindir}/tachyon-$variant
done
rename -- -thr "" $RPM_BUILD_ROOT%{_bindir}/*
mkdir -p docs/html
cp -pr docs/tachyon/*.{css,html,png} docs/html
cp -pr scenes $RPM_BUILD_ROOT%{_datadir}/tachyon/
install -pm644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/
echo ".so tachyon.1" > $RPM_BUILD_ROOT%{_mandir}/man1/tachyon-ogl.1
cp -a compile/%{target}-thr/libtachyon*.so $RPM_BUILD_ROOT%{_libdir}/
install -pm644 src/{hash,tachyon{,_dep},util}.h $RPM_BUILD_ROOT%{_includedir}/tachyon/

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%doc Copyright README
%{_libdir}/libtachyon-%{version}.so

%files gl
%{_bindir}/%{name}-ogl
%{_mandir}/man1/%{name}-ogl.1*

%files devel
%{_includedir}/tachyon
%{_libdir}/libtachyon.so

%files docs
%doc Changes docs/tachyon.pdf docs/tachyon.ps docs/html
%{_datadir}/tachyon
