%define name		tachyon
%define tachyondir	%{_datadir}/%{name}
# no 64 bits gl posix threads target
%define with_gl		0

Name:		%{name}
Group:		Graphics
License:	BSD
Summary:	Tachyon Parallel / Multiprocessor Ray Tracing System
Version:	0.98.9
Release:	%mkrel 4
Source:		http://jedi.ks.uiuc.edu/~johns/raytracer/files/0.98.9/tachyon-0.98.9.tar.gz
URL:		http://jedi.ks.uiuc.edu/~johns/raytracer/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libjpeg-devel
BuildRequires:	libnetpbm-devel
BuildRequires:	libpng-devel
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
%if %{with_gl}
BuildRequires:	GL-devel
%endif

Patch0:		tachyon-0.98.9-x86_64.patch
Patch1:		tachyon-0.98.9-sagemath.patch

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

%ifarch x86_64
%patch0 -p1
%endif
%patch1 -p1

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


%changelog
* Sat Nov 05 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.98.9-4mdv2012.0
+ Revision: 718345
- Rebuild with newer libpng

* Tue May 31 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.98.9-3
+ Revision: 682025
- Add patch from sagemath spkg.

* Mon Nov 22 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.98.9-2mdv2011.0
+ Revision: 599848
- Correct x86_64 crash with certain inputs

* Mon Nov 22 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.98.9-1mdv2011.0
+ Revision: 599822
- Update to latest upstream release

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 0.98-4mdv2010.0
+ Revision: 419819
- rebuild for new libjpeg v7

* Sat Jun 20 2009 Paulo Andrade <pcpa@mandriva.com.br> 0.98-3mdv2010.0
+ Revision: 387429
- Enable support for png and jpeg output.
  disable some of the "coolest" sagemath examples. I.e. try cut&paste
  of some of the samples at:
  	http://wiki.sagemath.org/pics
  that works after this patch.

* Fri May 08 2009 Paulo Andrade <pcpa@mandriva.com.br> 0.98-2mdv2010.0
+ Revision: 373542
+ rebuild (emptylog)

* Mon Mar 30 2009 Paulo Andrade <pcpa@mandriva.com.br> 0.98-1mdv2009.1
+ Revision: 362592
- Initial import of tachyon, version 0.98
  Tachyon Parallel / Multiprocessor Ray Tracing System
  http://jedi.ks.uiuc.edu/~johns/raytracer/
- tachyon

