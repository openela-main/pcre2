# Add readline edditing in pcre2test tool
%bcond_without pcre2_enables_readline

# Disable SELinux-frindly JIT allocator because it seems not to be fork-safe,
# https://bugs.exim.org/show_bug.cgi?id=1749#c45
%bcond_with pcre2_enables_sealloc

# This is stable release:
#%%global rcversion RC1
Name:       pcre2
Version:    10.32
Release:    %{?rcversion:0.}3%{?rcversion:.%rcversion}%{?dist}
%global     myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
# the library:                          BSD with exceptions
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text with exceptions and
#                                       Public Domain declaration
#                                       for testdata
#Bundled
# src/sljit:                            BSD
#Not distributed in any binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# cmake/COPYING-CMAKE-SCRIPTS:          BSD
# compile:                              GPLv2+ with exception
# config.guess:                         GPLv3+ with exception
# config.sub:                           GPLv3+ with exception
# configure:                            FSFUL and GPLv2+ with exception
# depcomp:                              GPLv2+ with exception
# INSTALL:                              FSFAP
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and (MIT or GPLv3+)
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFUL and FSFULLR and
#                                       GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# Makefile.in:                          FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:    BSD
URL:        http://www.pcre.org/
Source:     ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre2-10.10-Fix-multilib.patch
# Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
# a greater than 1 fixed quantifier, upstream bug #2320, bug#1628200,
# in upstream after 10.32
Patch1:     pcre2-10.32-Fix-subject-buffer-overread-in-JIT.-Found-by-Yunho-K.patch
# Fix caseless matching an extended class in JIT mode, upstream bug #2321,
# bug #1617960, in upstream after 10.32
Patch2:     pcre2-10.32-Fix-an-xclass-matching-issue-in-JIT.patch
# Fix matching a zero-repeated subroutine call at a start of a pattern,
# upstream bug #2332, bug: #1628200, in upstream after 10.32
Patch3:     pcre2-10.32-Fix-zero-repeated-subroutine-call-at-start-of-patter.patch
# Fix heap limit checking overflow in pcre2_dfa_match(), upstream bug #2334,
# bug#1628200, in upstream after 10.32
Patch4:     pcre2-10.32-Fix-heap-limit-checking-overflow-bug-in-pcre2_dfa_ma.patch
# 1/2 Fix CVE-2019-20454 (a crash when \X is used without UTF mode in a JIT),
# upstream bug #2399, bug #1734468, in upstream after 10.33
Patch5:     pcre2-10.32-Fix-crash-when-X-is-used-without-UTF-in-JIT.patch
# 2/2 Fix CVE-2019-20454 (a crash when \X is used without UTF mode in a JIT),
# upstream bug #2399, bug #1734468, in upstream after 10.33
Patch6:     pcre2-10.32-Forgot-this-file-in-previous-commit.-Fixes-JIT-non-U.patch
# Fix CVE-2022-1586 (Out-of-bounds read in compile_xclass_matchingpath)
# Downstream patch backport
# Ref: https://github.com/PCRE2Project/pcre2/commit/50a51cb7e67268e6ad417eb07c9de9bfea5cc55a
# https://github.com/PCRE2Project/pcre2/commit/d4fa336fbcc388f89095b184ba6d99422cfc676c
Patch7: pcre2-10.32-Fix-CVE-2022-1586
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
%if %{with pcre2_enables_readline}
BuildRequires:  readline-devel
%endif
Provides:       bundled(sljit)

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%package utf16
Summary:    UTF-16 variant of PCRE2
Provides:   bundled(sljit)
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf16
This is PCRE2 library working on UTF-16 strings.

%package utf32
Summary:    UTF-32 variant of PCRE2
Provides:   bundled(sljit)
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf32
This is PCRE2 library working on UTF-32 strings.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf16%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf32%{?_isa} = %{version}-%{release}

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel%{_isa} = %{version}-%{release}
Provides:   bundled(sljit)

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Requires:   %{name}%{_isa} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%prep
%setup -q -n %{name}-%{myversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit \
    --disable-pcre2grep-jit \
%else
    --enable-jit \
    --enable-pcre2grep-jit \
%endif
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
%if %{with pcre2_enables_sealloc}
    --enable-jit-sealloc \
%else
    --disable-jit-sealloc \
%endif
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
%if %{with pcre2_enables_readline}
    --enable-pcre2test-libreadline \
%else
    --disable-pcre2test-libreadline \
%endif
    --disable-rebuild-chartables \
    --enable-shared \
    --disable-silent-rules \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%check
make %{?_smp_mflags} check VERBOSE=yes

%ldconfig_scriptlets
%ldconfig_scriptlets utf16
%ldconfig_scriptlets utf32

%files
%{_libdir}/libpcre2-8.so.*
%{_libdir}/libpcre2-posix.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files utf16
%{_libdir}/libpcre2-16.so.*
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files utf32
%{_libdir}/libpcre2-32.so.*
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%files static
%{_libdir}/*.a
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE

%files tools
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%changelog
* Fri May 13 2022 Lukas Javorsky <ljavorsk@redhat.com> - 10.32-3
- Resolves: CVE-2022-1586

* Mon May 13 2019 Petr Pisar <ppisar@redhat.com> - 10.32-2
- Fix CVE-2019-20454 (a crash when \X is used without UTF mode in a JIT)
  (bug #1734468)

* Fri Dec 07 2018 Petr Pisar <ppisar@redhat.com> - 10.32-1
- 10.32 bump (bug #1628200)
- Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
  a greater than 1 fixed quantifier (bug #1628200)
- Fix matching a zero-repeated subroutine call at a start of a pattern
  (bug #1628200)
- Fix heap limit checking overflow in pcre2_dfa_match() (bug #1628200)

* Mon Sep 24 2018 Petr Pisar <ppisar@redhat.com> - 10.31-11
- Fix caseless matching an extended class in JIT mode (bug #1617960)

* Mon Sep 03 2018 Petr Pisar <ppisar@redhat.com> - 10.31-10
- Fix anchoring in conditionals with only one branch (bug #1617960)

* Thu Aug 16 2018 Petr Pisar <ppisar@redhat.com> - 10.31-9
- Recognize all Unicode space characters with /x option in a pattern
  (bug #1617960)
- Fix changing dynamic options (bug #1617960)
- Fix autopossessifying a repeated negative class with no characters less than
  256 that is followed by a positive class with only characters less than 255,
  (bug #1617960)
- Fix autopossessifying a repeated negative class with no characters less than
  256 that is followed by a positive class with only characters less than 256,
  (bug #1617960)

* Tue Jul 31 2018 Petr Pisar <ppisar@redhat.com> - 10.31-8
- Fix backtracking atomic groups when they are not separated by something with
  a backtracking point

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 10.31-7
- Fix checking that a lookbehind assertion has a fixed length if the
  lookbehind assertion is used inside a lookahead assertion
- Fix parsing VERSION conditions

* Mon Jul 02 2018 Petr Pisar <ppisar@redhat.com> - 10.31-6
- Fix global search/replace in pcre2test and pcre2_substitute() when the pattern
  matches an empty string, but never at the starting offset

* Mon Jun 25 2018 Petr Pisar <ppisar@redhat.com> - 10.31-5
- Fix bug when \K is used in a lookbehind in a substitute pattern

* Fri Mar 16 2018 Petr Pisar <ppisar@redhat.com> - 10.31-4
- Fix setting error offset zero for early errors in pcre2_pattern_convert()

* Mon Feb 26 2018 Petr Pisar <ppisar@redhat.com> - 10.31-3
- Add support to pcre2grep for binary zeros in -f files (upstream bug #2222)
- Fix compiler warnings in pcre2grep

* Tue Feb 20 2018 Petr Pisar <ppisar@redhat.com> - 10.31-2
- Fix returning unset groups in POSIX interface if REG_STARTEND has a non-zero
  starting offset (upstream bug #2244)
- Fix pcre2test -C to correctly show what \R matches
- Fix matching repeated character classes against an 8-bit string containting
  multi-code-unit characters

* Mon Feb 12 2018 Petr Pisar <ppisar@redhat.com> - 10.31-1
- 10.31 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.31-0.3.RC1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.31-0.3.RC1.1
- Switch to %%ldconfig_scriptlets

* Thu Feb 01 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.3.RC1
- Fix auto-possessification at the end of a capturing group that is called
  recursively (upstream bug #2232)

* Tue Jan 30 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.2.RC1
- Enlarge ovector array match data structure to be large enough in all cases
  (oss-fuzz #5415)

* Mon Jan 15 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.1.RC1
- 10.31-RC1 bump

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 10.30-5
- Fix handling \K in an assertion in pcre2grep tool and documentation
  (upstream bug #2211)
- Fix matching at a first code unit of a new line sequence if PCRE2_FIRSTLINE
  is enabled

* Fri Dec 22 2017 Petr Pisar <ppisar@redhat.com> - 10.30-4
- Fix pcre2_jit_match() to properly check the pattern was JIT-compiled
- Allow pcre2grep match counter to handle values larger than 2147483647,
  (upstream bug #2208)
- Fix incorrect first matching character when a backreference with zero minimum
  repeat starts a pattern (upstream bug #2209)

* Mon Nov 13 2017 Petr Pisar <ppisar@redhat.com> - 10.30-3
- Fix multi-line matching in pcre2grep tool (upstream bug #2187)

* Thu Nov 02 2017 Petr Pisar <ppisar@redhat.com> - 10.30-2
- Accept files names longer than 128 bytes in recursive mode of pcre2grep
  (upstream bug #2177)

* Tue Aug 15 2017 Petr Pisar <ppisar@redhat.com> - 10.30-1
- 10.30 bump

* Wed Aug 02 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.6.RC1
- Disable SELinux-friendly JIT allocator because it crashes after a fork
  (upstream bug #1749)

* Mon Jul 31 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.5.RC1
- Fix handling a hyphen at the end of a character class (upstream bug #2153)

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 10.30-0.4.RC1
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.3.RC1
- Fix applying local x modifier while global xx was in effect

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.30-0.2.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.2.RC1
- Fix a compiler warning in JIT code for ppc32

* Thu Jul 20 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.1.RC1
- 10.30-RC1 bump
- Heap-based matching implementation replaced stack-based one
- SELinux-friendly JIT enabled

* Fri Jun 16 2017 Petr Pisar <ppisar@redhat.com> - 10.23-8
- Fix DFA matching a lookbehind assertion that has a zero-length branch
  (PCRE2 oss-fuzz issue 1859)
- Fix returned offsets from regexec() when REG_STARTEND is used with starting offset
  greater than zero (upstream bug #2128)

* Tue May 09 2017 Petr Pisar <ppisar@redhat.com> - 10.23-7
- Fix a pcre2test crash on multiple push statements (upstream bug #2109)

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 10.23-6
- Fix CVE-2017-7186 in JIT mode (a crash when finding a Unicode property for
  a character with a code point greater than 0x10ffff in UTF-32 library while
  UTF mode is disabled) (bug #1434504)
- Fix an incorrect cast in UTF validation (upstream bug #2090)

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 10.23-5
- Fix DFA match for a possessively repeated character class (upstream bug #2086)
- Use a memory allocator from the pattern if no context is supplied to
  pcre2_match()

* Wed Mar 22 2017 Petr Pisar <ppisar@redhat.com> - 10.23-4
- Close serialization file in pcre2test after any error (upstream bug #2074)
- Fix a memory leak in pcre2_serialize_decode() when the input is invalid
  (upstream bug #2075)
- Fix a potential NULL dereference in pcre2_callout_enumerate() if called with
  a NULL pattern pointer when Unicode support is available (upstream bug #2076)
- Fix CVE-2017-8786 (32-bit error buffer size bug in pcre2test) (bug #1500717)

* Mon Mar 20 2017 Petr Pisar <ppisar@redhat.com> - 10.23-3
- Fix an internal error for a forward reference in a lookbehind with
  PCRE2_ANCHORED (oss-fuzz bug #865)
- Fix a pcre2test bug for global match with zero terminated subject
  (upstream bug #2063)

* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 10.23-2
- Handle memmory allocation failures in pcre2test tool
- Fix CVE-2017-7186 (a crash when finding a Unicode property for a character
  with a code point greater than 0x10ffff in UTF-32 library while UTF mode is
  disabled) (upstream bug #2052)

* Tue Feb 14 2017 Petr Pisar <ppisar@redhat.com> - 10.23-1
- 10.23 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.23-0.1.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Petr Pisar <ppisar@redhat.com> - 10.23-0.1.RC1
- 10.23-RC1 bump

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 10.22-10.1
- Rebuild for readline 7.x

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 10.22-10
- Fix an out-of-bound read in pcre2test tool within POSIX mode
  (upstream bug #2008)

* Tue Jan 03 2017 Petr Pisar <ppisar@redhat.com> - 10.22-9
- Fix compiling a class with UCP and without UTF

* Fri Dec 16 2016 Petr Pisar <ppisar@redhat.com> - 10.22-8
- Fix a crash when doing an extended substitution for \p, \P, or \X
  (upstream bug #1977)
- Fix a crash in substitution if starting offest was specified beyond the
  subject end (upstream bug #1992)

* Fri Dec 09 2016 Petr Pisar <ppisar@redhat.com> - 10.22-7
- Fix pcre2-config --libs-posix output (upstream bug #1924)
- Fix a memory leak and a typo in a documentation (upstream bug #1973)
- Fix a buffer overflow in partial match test for CRLF in an empty buffer
  (upstream bug #1975)
- Fix a crash in pcre2test when displaying a wide character with a set locate
  (upstream bug #1976)

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 10.22-6
- Fix faulty auto-anchoring patterns when .* is inside an assertion

* Mon Oct 24 2016 Petr Pisar <ppisar@redhat.com> - 10.22-5
- Document assert capture limitation (upstream bug #1887)
- Ignore offset modifier in pcre2test in POSIX mode (upstream bug #1898)

* Wed Oct 19 2016 Richard W.M. Jones <@redhat.com> - 10.22-4
- Disable the JIT on riscv64.

* Wed Oct 19 2016 Petr Pisar <ppisar@redhat.com> - 10.22-3
- Fix displaying a callout position in pcretest output with an escape sequence
  greater than \x{ff}
- Fix pcrepattern(3) documentation
- Fix miscopmilation of conditionals when a group name start with "R"
  (upstream bug #1873)
- Fix internal option documentation in pcre2pattern(3) (upstream bug #1875)
- Fix optimization bugs for patterns starting with lookaheads
  (upstream bug #1882)

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-2
- Fix matching characters above 255 when a negative character type was used
  without enabled UCP in a positive class (upstream bug #1866)

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-1
- 10.22 bump

* Thu Jun 30 2016 Petr Pisar <ppisar@redhat.com> - 10.22-0.1.RC1
- 10.22-RC1 bump
- libpcre2-posix library changed ABI
- Fix register overwite in JIT when SSE2 acceleration is enabled
- Correct pcre2unicode(3) documentation

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 10.21-6
- Fix repeated pcregrep output if -o with -M options were used and the match
  extended over a line boundary (upstream bug #1848)

* Fri Jun 03 2016 Petr Pisar <ppisar@redhat.com> - 10.21-5
- Fix a race in JIT locking condition
- Fix an ovector check in JIT test program
- Enable JIT in the pcre2grep tool

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 10.21-4
- Ship README in devel as it covers API and build, not general info
- Move UTF-16 and UTF-32 libraries into pcre-ut16 and pcre-32 subpackages

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 10.21-3
- Fix a typo in pcre2_study()

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> - 10.21-2
- Report unmatched closing parantheses properly
- Fix pcre2test for expressions with a callout inside a look-behind assertion
  (upstream bug #1783)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (upstream bug #1791)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.21-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 10.21-1
- 10.21 bump

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.2.RC1
- Adapt a test to French locale on RHEL

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.1.RC1
- 10.21-RC1 bump

* Mon Oct 26 2015 Petr Pisar <ppisar@redhat.com> - 10.20-3
- Fix compiling patterns with PCRE2_NO_AUTO_CAPTURE (upstream bug #1704)

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 10.20-2
- Fix compiling classes with a negative escape and a property escape
  (upstream bug #1697)
- Fix integer overflow for patterns whose minimum matching length is large
  (upstream bug #1699)

* Fri Jul 03 2015 Petr Pisar <ppisar@redhat.com> - 10.20-1
- 10.20 bump

* Fri Jun 19 2015 Petr Pisar <ppisar@redhat.com> - 10.20-0.1.RC1
- 10.20-RC1 bump
- Replace dependency on glibc-headers with gcc (bug #1230479)
- Preserve soname

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.10-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-3
- fixed Release field

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-2.1
- Backport fix for AArch64

* Tue May 05 2015 Petr Pisar <ppisar@redhat.com> - 10.10-2
- Package pcre2demo.c as a documentation for pcre2-devel

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 10.10-1
- PCRE2 library packaged

