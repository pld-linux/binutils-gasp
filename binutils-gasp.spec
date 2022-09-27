Summary:	GASP - old preprocessor for assembly programs
Summary(pl.UTF-8):	GASP - stary preprocesor dla programów w asemblerze
Name:		binutils-gasp
Version:	2.13.2.1a
Release:	1
Epoch:		5
License:	GPL v3+
Group:		Development/Tools
Source0:	https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	aeb6464c6e3584edc021f7a552ec4fbd
Patch0:		binutils-info.patch
Patch1:		binutils-relax_type.patch
URL:		http://www.sourceware.org/binutils/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
%ifarch sparc sparc32
BuildRequires:	sparc32
%endif
BuildRequires:	texinfo >= 4.2
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GASP - old preprocessor for assembly programs. It's officially
obsoleted, but it's still needed to build some packages.

%description -l pl.UTF-8
GASP - stary preprocesor dla programów w asemblerze. Jest oficjalnie
uznany za przestarzały, ale jest nadal potrzebny do zbudowania
niektórych pakietów.

%prep
%setup -q -n binutils-2.13.2.1
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.* .
CFLAGS="%{rpmcflags}"; export CFLAGS
CC="%{__cc}"; export CC
%ifarch sparc
sparc32 \
%endif
./configure %{_target_platform} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--sysconfdir=%{_sysconfdir} \
	--disable-debug \
	--disable-silent-rules \
	--disable-werror \
%ifarch sparc
	--enable-64-bit-bfd \
%endif
	--enable-build-warnings=,-Wno-missing-prototypes \
	--with-tooldir=%{_prefix} \
	--with-zlib

%{__make} -C libiberty
%{__make} -C bfd
%{__make} -C gas gasp-new
%{__make} -C gas/doc gasp.info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_infodir}}

install gas/gasp-new $RPM_BUILD_ROOT%{_bindir}/gasp
cp -p gas/doc/gasp.info* $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gasp
%{_infodir}/gasp.info*
