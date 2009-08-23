%define name		tachyon
%define tachyondir	%{_datadir}/%{name}
# no 64 bits gl posix threads target
%define with_gl		0

Name:		%{name}
Group:		Graphics
License:	BSD
Summary:	Tachyon Parallel / Multiprocessor Ray Tracing System
Version:	0.98
Release:	%mkrel 4
Source:		http://jedi.ks.uiuc.edu/~johns/raytracer/files/0.98.1/tachyon-0.98.1.tar.gz
URL:		http://jedi.ks.uiuc.edu/~johns/raytracer/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libjpeg-devel
BuildRequires:	libnetpbm-devel
BuildRequires:	libpng-devel
BuildRequires:	texlive
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
%if %{with_gl}
BuildRequires:	GL-devel
%endif

%description
Tachyon is a parallel ray tracing library, for use on distributed memory
parallel computers, shared memory computers, and clusters of workstations.
Tachyon supports MPI for distributed memory parallel computers, threads
for shared memory machines, and can support both simultaneously for
clusters of shared memory machines. Tachyon has been selected for inclusion
in the SPEC MPI2007 benchmark suite. Tachyon supports the typical ray tracer
features, most of the common geometric primitives, shading and texturing
modes, etc. It also supports less common features such as HDR image output,
ambient occlusion lighting, and support for various triangle mesh and
volumetric texture formats beneficial for molecular visualization (e.g.
rendering VMD scenes). 

%prep
%setup -q -n %{name}

%ifarch %{ix86}
%define target		linux-thr
%else
  %ifarch x86_64
  %define target	linux-64-thr
  %else
    echo 'must specify arch in spec'
    exit 1
  %endif
%endif


%build
pushd unix
    make USEJPEG=-DUSEJPEG JPEGLIB=-ljpeg				\
	USEPNG=-DUSEPNG PNGLIB="-lpng -lz"				\
%if %{with_gl}
	LINUX_GLX_INCS= LINUX_GLX_LIBS="-lGL -lGLU -lX11"
%endif
	%{target}

popd

pushd docs
make pdf
popd

%install
mkdir -p %{buildroot}/%{_bindir}
cp -fa compile/%{target}/%{name} %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_libdir}
cp -fa compile/%{target}/lib%{name}.a %{buildroot}/%{_libdir}

mkdir -p %{buildroot}%{tachyondir}
cp -fa scenes %{buildroot}%{tachyondir}
pushd %{buildroot}%{tachyondir}
    rm -fr CVS
    # broken symbolic links in tarball
    rm -f imaps tpoly vol
popd

mkdir -p %{buildroot}/%{_docdir}/%{name}
cp -fa README docs/%{name}.pdf %{buildroot}/%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/lib%{name}.a
%dir %{tachyondir}
%{tachyondir}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
