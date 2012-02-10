%define oname pcre
%define pcre_major 0
%define libname	%mklibname pcre %{pcre_major}

Summary: 	Perl-compatible regular expression library
Name:	 	pcre0
Version:	8.21
Release:	2
License: 	BSD-Style
Group:  	File tools
URL: 		http://www.pcre.org/
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%oname-%version.tar.bz2
Source1:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%oname-%version.tar.bz2.sig
BuildRequires:	autoconf automake libtool
Patch1:		pcre-0.6.5-fix-detect-into-kdelibs.patch
Patch2:		pcre-linkage_fix.diff
# from debian:
Patch4:		pcre-pcreposix-glibc-conflict.patch

%description
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. 
This package contains a grep variant based on the PCRE library.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Perl-compatible regular expression library

%description -n	%{libname}
This package contains the shared library libpcre compat.

%prep
%setup -qn %{oname}-%{version}
%patch1 -p1 -b .detect_into_kdelibs
%patch2 -p0
%patch4 -p1 -b .symbol-conflict

# bork
perl -pi -e "s|ln -s|ln -snf|g" Makefile.am

%build
mkdir -p m4
autoreconf -fi
%configure2_5x \
	--disable-static \
	--enable-utf \
	--enable-unicode-properties \
	--enable-jit

%make

%check
export LC_ALL=C
# Tests, patch out actual pcre_study_size in expected results
#echo 'int main() { printf("%d", sizeof(pcre_study_data)); return 0; }' | \
#%{__cc} -xc - -include "pcre_internal.h" -I. -o study_size
#STUDY_SIZE=`./study_size`
#perl -pi -e "s,(Study size\s+=\s+)\d+,\${1}$STUDY_SIZE," testdata/testoutput*
make check

%install
rm -rf %{buildroot}

install -d %{buildroot}/%{_lib}
install -d %{buildroot}/%{_libdir}
mv %{buildroot}%{_libdir}/libpcre.so.%{pcre_major}.* %{buildroot}/%{_lib}/
pushd %{buildroot}%{_libdir}
    ln -s ../../%{_lib}/lib%{oname}.so.%{pcre_major}.* .
popd

%files -n %{libname}
/%{_lib}/libpcre.so.%{pcre_major}*
%{_libdir}/libpcre.so.%{pcre_major}*

