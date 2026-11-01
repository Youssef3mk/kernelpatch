# All Global changes to build and install go here.

# Per the below section about \__spec_install_pre, any rpm

# environment changes that affect %%install need to go

# here before the %%install macro is pre-built.

# Disable frame pointers

%undefine \_include_frame_pointers

# Save default LTO flags before disabling (for use with kernel tools).

%global \_default_lto_cflags %{\_lto_cflags}

# Disable LTO in userspace packages (disabled for perf).

%global \_lto_cflags %{nil}

# Option to enable compiling with clang instead of gcc.

%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%endif

# Compile the kernel with LTO (only supported when building with clang).

%bcond_with clang_lto

%if %{with clang_lto} && %{without toolchain_clang}
%{error:clang_lto requires --with toolchain_clang}
%endif

# RPM macros strip everything in BUILDROOT, either with \__strip

# or find-debuginfo.sh. Make use of \__spec_install_post override

# and save/restore binaries we want to package as unstripped.

%define buildroot_unstripped %{\_builddir}/root_unstripped
%define buildroot_save_unstripped() 

(cd %{buildroot}; cp -rav --parents -t %{buildroot_unstripped}/ %1 || true) 

%{nil}
%define \__restore_unstripped_root_post 

echo "Restoring unstripped artefacts %{buildroot_unstripped} -> %{buildroot}" 

cp -rav %{buildroot_unstripped}/. %{buildroot}/ 

%{nil}

%global \__spec_install_pre %{\___build_pre}

%define uname_suffix() %{lua:
local flavour = rpm.expand('%{?1:+%{1}}')
flavour = flavour:gsub('-', '\_')
if flavour \~= '' then
print(flavour)
end
}

%define uname_variant() %{lua:
local flavour = rpm.expand('%{?1:%{1}}')
\_, \_, main, sub = flavour:find("(%w+)-(.\*)")
if main then
print("+" .. main)
end
}

%ifnarch i686
%define \_binary_payload w3T.xzdio
%endif

Summary: The Linux kernel
%if 0%{?fedora}
%define secure_boot_arch x86_64 aarch64
%else
%define secure_boot_arch x86_64 aarch64 s390x ppc64le
%endif

%ifarch %{secure_boot_arch}
%global signkernel 1
%else
%global signkernel 0
%endif

%global dtb_arches aarch64 riscv64
%global uki_arches x86_64 aarch64 riscv64

%if 0%{?centos}
%global sbat_suffix centos
%else
%if 0%{?fedora}
%global sbat_suffix fedora
%else
%global sbat_suffix rhel
%endif
%endif

%global signmodules 1
%global rhelkeys 1

%ifarch noarch
%global zipmodules 0
%else
%global zipmodules 1
%endif

%global compression xz
%global compression_flags --compress --check=crc32 --lzma2=dict=1MiB
%global compext xz

%if 0%{?fedora}
%define primary_target fedora
%else
%define primary_target rhel
%endif

%global package_name kernel
%global gemini 0
%global include_fedora 1
%global include_rhel 1
%global include_rt 1
%global include_automotive 0
%global patchlist_changelog 1
%global released_kernel 1
%define debugbuildsenabled 1

%define specrpmversion 6.12.11
%define specversion 6.12.11
%define patchversion 6.12
%define pkgrelease 200
%define kversion 6
%define tarfile_release 6.12.11
%define patchlevel 12
%define specrelease 200%{?buildid}%{?dist}
%define kabiversion 6.12.11
%define selftests_must_build 0

%define pkg_release %{specrelease}
%global \__provides_exclude_from ^%{\_libexecdir}/kselftests

%define with_stock        %{?\_without_stock:        0} %{?!\_without_stock:        1}
%{?\_with_up: %define with_stock 1}
%{?\_without_up: %define with_stock 0}

%define with_base      %{?\_without_base:      0} %{?!\_without_base:      1}
%define with_debug     %{?\_without_debug:     0} %{?!\_without_debug:     1}
%define with_zfcpdump  %{?\_without_zfcpdump:  0} %{?!\_without_zfcpdump:  1}
%define with_arm64_16k %{?\_with_arm64_16k:    1} %{?!\_with_arm64_16k:    0}
%define with_arm64_64k %{?\_without_arm64_64k: 0} %{?!\_without_arm64_64k: 1}

%if 0%{?fedora}
%define with_realtime  %{?\_with_realtime:  1} %{?!\_with_realtime:  0}
%define with_realtime_arm64_64k %{?\_with_realtime_arm64_64k: 1} %{?!\_with_realtime_arm64_64k: 0}
%else
%define with_realtime  %{?\_without_realtime:  0} %{?!\_without_realtime:  1}
%define with_realtime_arm64_64k %{?\_without_realtime_arm64_64k: 0} %{?!\_without_realtime_arm64_64k: 1}
%endif
%define with_automotive %{?\_with_automotive:  1} %{?!\_with_automotive:   0}

%define with_doc       %{?\_without_doc:       0} %{?!\_without_doc:       1}
%define with_headers   %{?\_without_headers:   0} %{?!\_without_headers:   1}
%define with_cross_headers   %{?\_without_cross_headers:   0} %{?!\_without_cross_headers:   1}
%define with_perf      %{?\_without_perf:      0} %{?!\_without_perf:      1}
%define with_libperf   %{?\_without_libperf:   0} %{?!\_without_libperf:   1}
%define with_tools     %{?\_without_tools:     0} %{?!\_without_tools:     1}
%define with_ynl      %{?\_without_ynl:      0} %{?!\_without_ynl:      1}
%define with_debuginfo %{?\_without_debuginfo: 0} %{?!\_without_debuginfo: 1}
%define with_kmap      %{?\_without_kmap:      0} %{?!\_without_kmap:      1}
%define with_kernel_abi_stablelists %{?\_without_kernel_abi_stablelists: 0} %{?!\_without_kernel_abi_stablelists: 1}
%define with_selftests %{?\_without_selftests: 0} %{?!\_without_selftests: 1}

%define with_baseonly  %{?\_with_baseonly:     1} %{?!\_with_baseonly:     0}
%define with_dbgonly   %{?\_with_dbgonly:      1} %{?!\_with_dbgonly:      0}
%define with_rtonly    %{?\_with_rtonly:       1} %{?!\_with_rtonly:       0}
%define with_automotiveonly %{?\_with_automotiveonly:       1} %{?!\_with_automotiveonly:       0}
%define with_automotive_build %{?\_with_automotive_build:   1} %{?!\_with_automotive_build:     0}
%define with_toolsonly %{?\_with_toolsonly:    1} %{?!\_with_toolsonly:    0}
%define with_kabichk   %{?\_without_kabichk:   0} %{?!\_without_kabichk:   1}
%define with_kabichk 0
%define with_kabidupchk %{?\_with_kabidupchk:  1} %{?!\_with_kabidupchk:   0}
%define with_kabidwchk %{?\_without_kabidwchk: 0} %{?!\_without_kabidwchk: 1}
%define with_kabidw_base %{?\_with_kabidw_base: 1} %{?!\_with_kabidw_base: 0}
%define with_vdso_install %{?\_without_vdso_install: 0} %{?!\_without_vdso_install: 1}
%define with_sparse    %{?\_with_sparse:       1} %{?!\_with_sparse:       0}
%define with_cross    %{?\_with_cross:         1} %{?!\_with_cross:        0}
%define with_release   %{?\_with_release:      1} %{?!\_with_release:      0}
%define with_verbose %{?\_with_verbose:        1} %{?!\_with_verbose:      0}
%define with_configchecks %{?\_without_configchecks:        0} %{?!\_without_configchecks:        1}
%define with_gcov %{?\_with_gcov:1}%{?!\_with_gcov:0}
%define with_vanilla %{?\_with_vanilla: 1} %{?!\_with_vanilla: 0}

%ifarch %{uki_arches}
%define with_efiuki %{?\_without_efiuki: 0} %{?!\_without_efiuki: 1}
%else
%define with_efiuki 0
%endif

%ifarch aarch64
%if 0%{?fedora}
%define with_dtbloader %{?\_without_dtbloader: 0} %{?!\_without_dtbloader: 1}
%else
%define with_dtbloader 0
%endif
%else
%define with_dtbloader 0
%endif

%if 0%{?fedora}
%define with_headers 0
%define with_cross_headers 0
%define with_kernel_abi_stablelists 0
%define with_arm64_64k 0
%define with_automotive 0
%endif

%if %{with_verbose}
%define make_opts V=1
%else
%define make_opts -s
%endif

%if %{with toolchain_clang}
%ifarch s390x ppc64le
%global llvm_ias 0
%else
%global llvm_ias 1
%endif
%global clang_make_opts HOSTCC=clang CC=clang LLVM_IAS=%{llvm_ias} LLVM=1
%global make_opts %{make_opts} %{clang_make_opts}
%endif

%if %{with_gcov}
%define with_debug 0
%define with_kabichk 0
%define with_kabidupchk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%endif

%if %{with_kabidw_base}
%define with_kabidwchk 0
%endif

%define make_target bzImage
%define image_install_path boot

%define KVERREL %{specversion}-%{release}.%{\_target_cpu}
%define KVERREL_RE %(echo %KVERREL | sed 's/+/\[+\]/g')
%define hdrarch %\_target_cpu
%define asmarch %\_target_cpu

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%if %{with_release}
%define debugbuildsenabled 1
%endif

%if !%{with_debuginfo}
%define \_enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug
%global \_build_id_links alldebug

%if %{with_baseonly}
%define with_debug 0
%define with_realtime 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

%if %{with_dbgonly}
%define with_base 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

%if %{with_rtonly}
%define with_realtime 1
%define with_realtime_arm64_64k 1
%define with_automotive 0
%define with_stock 0
%define with_debug 0
%ifarch s390x ppc64le riscv64
%define with_debuginfo 0
%define with_base 0
%endif
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_dtbloader 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%endif

%if %{with_automotiveonly}
%define with_automotive 1
%define with_realtime 0
%define with_stock 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_selftests 1
%endif

%if %{with_automotive_build}
%define with_automotive 1
%define with_selftests 1
%endif

%if %{with_toolsonly}
%define with_tools 1
%define with_stock 0
%define with_base 0
%define with_debug 0
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_automotive 0
%define with_cross_headers 0
%define with_doc 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_dtbloader 0
%define with_zfcpdump 0
%define with_vdso_install 0
%define with_kabichk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%define with_configchecks 0
%endif

%ifnarch x86_64 aarch64
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_automotive 0
%endif

%if %{with_automotive}
%global compression zstd
%global compression_flags --rm
%global compext zst
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_efiuki 0
%define with_dtbloader 0
%define with_doc 0
%define with_headers 0
%define with_cross_headers 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kabichk 0
%define with_kernel_abi_stablelists 0
%define with_kabidw_base 0
%define signkernel 0
%define signmodules 1
%define rhelkeys 0
%endif

%if %{zipmodules}
%global zipsed -e 's/.ko\$/.ko.%compext/'
%endif

%if !%{with_kabichk}
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

%if %{with_vdso_install}
%define use_vdso 1
%endif

%ifnarch noarch
%define with_kernel_abi_stablelists 0
%endif

%ifnarch noarch
%define with_doc 0
%define doc_build_fail true
%endif

%if 0%{?fedora}
%ifnarch aarch64 x86_64
%define with_debug 0
%endif
%endif

%define all_configs %{name}-%{specrpmversion}-\*.config

%ifarch noarch
%define with_stock 0
%define with_realtime 0
%define with_automotive 0
%define with_headers 0
%define with_cross_headers 0
%define with_tools 0
%define with_perf 0
%define with_libperf 0
%define with_selftests 0
%define with_debug 0
%endif

%ifnarch ppc64le
%define with_sparse 0
%endif

%ifnarch s390x
%define with_zfcpdump 0
%endif

%ifnarch aarch64
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_realtime_arm64_64k 0
%endif

%if 0%{?fedora}
%define with_zfcpdump 0
%endif

%ifarch i686
%define asmarch x86
%define hdrarch i386
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch ppc64le
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define use_vdso 0
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define kernel_image arch/s390/boot/bzImage
%define vmlinux_decompressor arch/s390/boot/vmlinux
%endif

%ifarch aarch64
%define asmarch arm64
%define hdrarch arm64
%define make_target vmlinuz.efi
%define kernel_image arch/arm64/boot/vmlinuz.efi
%endif

%ifarch riscv64
%define asmarch riscv
%define hdrarch riscv
%define make_target vmlinuz.efi
%define kernel_image arch/riscv/boot/vmlinuz.efi
%endif

%if %{nopatches}
%define with_configchecks 0
%endif

%if 0%{?fedora}
%define nobuildarches i386
%else
%define nobuildarches i386 i686
%endif

%ifarch %nobuildarches
%define with_stock 0
%define with_debug 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_automotive 0

%define with_debuginfo 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_selftests 0
%define \_enable_debug_packages 0
%endif

%ifnarch x86_64 ppc64le s390x aarch64 riscv64
%define with_kmap 0
%endif

%if 0%{?fedora}
%define cpupowerarchs %{ix86} x86_64 ppc64le aarch64 riscv64
%else
%define cpupowerarchs i686 x86_64 ppc64le aarch64 riscv64
%endif

%if 0%{?use_vdso}
%define \_use_vdso 1
%else
%define \_use_vdso 0
%endif

%define with_debug_meta 0
%if !%{debugbuildsenabled}
%if %{with_debug}
%define with_debug_meta 1
%endif
%define with_debug 0
%endif

%if %{with_stock} && %{with_base}
%define with_stock_base 1
%else
%define with_stock_base 0
%endif
%if %{with_realtime} && %{with_base}
%define with_realtime_base 1
%else
%define with_realtime_base 0
%endif
%if %{with_automotive} && %{with_base} && !%{with_automotive_build}
%define with_automotive_base 1
%else
%define with_automotive_base 0
%endif
%if %{with_arm64_16k} && %{with_base}
%define with_arm64_16k_base 1
%else
%define with_arm64_16k_base 0
%endif
%if %{with_arm64_64k} && %{with_base}
%define with_arm64_64k_base 1
%else
%define with_arm64_64k_base 0
%endif
%if %{with_realtime_arm64_64k} && %{with_base}
%define with_realtime_arm64_64k_base 1
%else
%define with_realtime_arm64_64k_base 0
%endif

%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027

Name: %{package_name}
License: ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND 0BSD AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSD-3-Clause-Clear AND CC0-1.0 AND GFDL-1.1-no-invariants-or-later AND GPL-1.0-or-later AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only OR CDDL-1.0) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-only) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-or-later) AND (GPL-2.0-only WITH Linux-syscall-note) AND GPL-2.0-or-later AND (GPL-2.0-or-later OR CC-BY-4.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND ISC AND LGPL-2.0-or-later AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND LGPL-2.1-only AND (LGPL-2.1-only WITH Linux-syscall-note) AND LGPL-2.1-or-later AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND (Linux-OpenIB OR GPL-2.0-only) AND (Linux-OpenIB OR GPL-2.0-only OR BSD-2-Clause) AND Linux-man-pages-copyleft AND MIT AND (MPL-1.1 OR GPL-2.0-only) AND (X11 OR GPL-2.0-only) AND (X11 OR GPL-2.0-or-later) AND Zlib AND (copyleft-next-0.3.1 OR GPL-2.0-or-later)
URL: https://www.kernel.org/
Version: %{specrpmversion}
Release: %{pkg_release}

%if 0%{?fedora}
ExclusiveArch: noarch x86_64 s390x aarch64 ppc64le riscv64
%else
ExclusiveArch: noarch i386 i686 x86_64 s390x aarch64 ppc64le riscv64
%endif
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: %{name}-core-uname-r = %{KVERREL}
Requires: %{name}-modules-uname-r = %{KVERREL}
Requires: %{name}-modules-core-uname-r = %{KVERREL}
Requires: ((%{name}-modules-extra-uname-r = %{KVERREL}) if %{name}-modules-extra-matched)
Suggests: %{name}-core = %{specversion}-%{release}
Provides: installonlypkg(kernel)
%endif

BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk, %compression

%ifarch x86_64 aarch64 riscv64
BuildRequires: zstd
%endif
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: kernel-rpm-macros
BuildRequires: glibc-static
%if %{with_headers} || %{with_cross_headers}
BuildRequires: rsync
%endif
%if %{with_doc}
BuildRequires: xmlto, asciidoc, python3-sphinx, python3-sphinx_rtd_theme
%endif
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_perf}
BuildRequires: zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel python3-setuptools
BuildRequires: capstone-devel
BuildRequires: elfutils-debuginfod-client-devel
BuildRequires: java-devel
%if 0%{?fedora} || 0%{?rhel} >= 11
BuildRequires: libbabeltrace2-devel
%endif
BuildRequires: libpfm-devel
BuildRequires: libtraceevent-devel
%ifnarch s390x
BuildRequires: numactl-devel
%endif
%ifarch aarch64
BuildRequires: opencsd-devel >= 1.0.0
%endif
%endif
%if %{with_tools}
BuildRequires: python3-docutils
BuildRequires: gettext ncurses-devel
BuildRequires: libcap-devel libcap-ng-devel
BuildRequires: python3-docutils
BuildRequires: libtraceevent-devel
BuildRequires: libtracefs-devel
BuildRequires: libbpf-devel
BuildRequires: bpftool
BuildRequires: clang

%ifarch %{cpupowerarchs}
BuildRequires: swig
%endif

%ifnarch s390x
BuildRequires: pciutils-devel
%endif
%ifarch i686 x86_64
BuildRequires: libnl3-devel
%endif
%endif

%if %{with_tools} && %{with_ynl}
BuildRequires: python3-pyyaml python3-jsonschema python3-pip python3-setuptools >= 61
BuildRequires: (python3-wheel if python3-setuptools < 70)
%endif

BuildRequires: openssl-devel

%if %{with_selftests}
BuildRequires: clang llvm-devel fuse-devel zlib-devel binutils-devel python3-docutils python3-jsonschema
%ifarch x86_64 riscv64
BuildRequires: lld
%endif
BuildRequires: libasan-static
BuildRequires: libcap-devel libcap-ng-devel rsync libmnl-devel libxml2-devel
BuildRequires: liburing-devel
BuildRequires: libubsan
BuildRequires: numactl-devel
BuildRequires: xxd
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
BuildConflicts: rpm < 4.13.0.1-19
BuildConflicts: dwarves < 1.13

%undefine \_include_minidebuginfo
%undefine \_find_debuginfo_dwz_opts
%undefine \_unique_build_ids
%undefine \_unique_debug_names
%undefine \_unique_debug_srcs
%undefine \_debugsource_packages
%undefine \_debuginfo_subpackages

%global \_find_debuginfo_opts -r -q

%global \_missing_build_ids_terminate_build 1
%global \_no_recompute_build_ids 1
%endif
%if %{with_kabidwchk} || %{with_kabidw_base}
BuildRequires: kabi-dw
%endif

%if %{signkernel}%{signmodules}
BuildRequires: openssl
%if %{signkernel}
%if 0%{?rhel}%{?centos} && !0%{?eln}
BuildRequires: system-sb-certs
%endif
%ifarch x86_64 aarch64 riscv64
BuildRequires: nss-tools
BuildRequires: pesign >= 0.10-4
%endif
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{\_build_arch}-linux-gnu, gcc-%{\_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{\_build_arch}-linux-gnu-
%define \__strip %{\_build_arch}-linux-gnu-strip
%endif

%if %{with_perf}
BuildRequires: xmlto
%endif
%if %{with_perf} || %{with_tools}
BuildRequires: asciidoc
%endif

%if %{with toolchain_clang}
BuildRequires: clang
BuildRequires: lld
%endif

%if %{with clang_lto}
BuildRequires: llvm
BuildRequires: lld
%endif

%if %{with_efiuki}
BuildRequires: dracut
BuildRequires: binutils
BuildRequires: lvm2
BuildRequires: systemd-udev >= 252-1
BuildRequires: xfsprogs e2fsprogs dosfstools
BuildRequires: tpm2-tools
%endif

%if %{with_dtbloader}
BuildRequires: stubble
%endif

%if %{with_efiuki} || %{with_dtbloader}
BuildRequires: systemd-boot-unsigned
BuildRequires: systemd-ukify
%if 0%{?rhel}%{?centos} && !0%{?eln}
%if 0%{?centos}
BuildRequires: centos-sb-certs >= 9.0-23
%else
BuildRequires: redhat-sb-certs >= 9.4-0.1
%endif
%endif
%endif

# Upstream Kernel Source Tarball

Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{tarfile_release}.tar.xz

Source1: Makefile.rhelver
Source2: %{name}.changelog

Source10: redhatsecurebootca5.cer
Source13: redhatsecureboot501.cer

%if %{signkernel}
%ifarch ppc64le
%define signing_key_filename kernel-signing-ppc.cer
%endif
%ifarch s390x
%define signing_key_filename kernel-signing-s390.cer
%endif

%if 0%{?fedora}%{?eln}
%define secureboot_ca_0 %{SOURCE10}
%define secureboot_key_0 %{SOURCE13}
%define secureboot_key_uki_0 %{secureboot_key_0}
%endif

%if 0%{?rhel} && !0%{?eln}
%define secureboot_ca_0 %{\_datadir}/pki/sb-certs/secureboot-ca-%{\_arch}.cer
%define secureboot_key_0 %{\_datadir}/pki/sb-certs/secureboot-kernel-%{\_arch}.cer
%define secureboot_key_uki_0 %{\_datadir}/pki/sb-certs/secureboot-uki-virt-%{\_arch}.cer
%endif

%endif

Source20: mod-denylist.sh
Source21: mod-sign.sh
Source22: filtermods.py

%define modsign_cmd %{SOURCE21}

%if 0%{?include_rhel}
Source24: %{name}-aarch64-rhel.config
Source25: %{name}-aarch64-debug-rhel.config
Source27: %{name}-ppc64le-rhel.config
Source28: %{name}-ppc64le-debug-rhel.config
Source29: %{name}-s390x-rhel.config
Source30: %{name}-s390x-debug-rhel.config
Source31: %{name}-s390x-zfcpdump-rhel.config
Source32: %{name}-x86_64-rhel.config
Source33: %{name}-x86_64-debug-rhel.config

Source42: %{name}-aarch64-64k-rhel.config
Source43: %{name}-aarch64-64k-debug-rhel.config

Source44: %{name}-riscv64-rhel.config
Source45: %{name}-riscv64-debug-rhel.config
%endif

%if 0%{?include_rhel} || 0%{?include_automotive}
Source23: x509.genkey.rhel
Source34: def_variants.yaml.rhel
Source41: x509.genkey.centos
%endif

%if 0%{?include_fedora}
Source50: x509.genkey.fedora

Source52: %{name}-aarch64-fedora.config
Source53: %{name}-aarch64-debug-fedora.config
Source54: %{name}-aarch64-16k-fedora.config
Source55: %{name}-aarch64-16k-debug-fedora.config
Source56: %{name}-ppc64le-fedora.config
Source57: %{name}-ppc64le-debug-fedora.config
Source58: %{name}-s390x-fedora.config
Source59: %{name}-s390x-debug-fedora.config
Source60: %{name}-x86_64-fedora.config
Source61: %{name}-x86_64-debug-fedora.config
Source700: %{name}-riscv64-fedora.config
Source701: %{name}-riscv64-debug-fedora.config

Source62: def_variants.yaml.fedora
%endif

Source70: partial-kgcov-snip.config
Source71: partial-kgcov-debug-snip.config
Source72: partial-clang-snip.config
Source73: partial-clang-debug-snip.config
Source74: partial-clang_lto-x86_64-snip.config
Source75: partial-clang_lto-x86_64-debug-snip.config
Source76: partial-clang_lto-aarch64-snip.config
Source77: partial-clang_lto-aarch64-debug-snip.config
Source78: partial-clang-s390x-snip.config
Source79: partial-clang-s390x-debug-snip.config
Source80: generate_all_configs.sh
Source81: process_configs.sh

Source82: dtbloader.sbat.template
Source83: uki.sbat.template
Source84: uki-addons.sbat.template
Source85: kernel.sbat.template

Source86: dracut-virt.conf

Source87: flavors

Source151: uki_create_addons.py
Source152: uki_addons.json

Source100: rheldup3.x509
Source101: rhelkpatch1.x509
Source102: nvidiagpuoot001.x509
Source103: rhelimaca1.x509
Source104: rhelima.x509
Source105: rhelima_centos.x509
Source106: fedoraimaca.x509
Source107: nvidiajetsonsoc.x509
Source108: nvidiabfdpu.x509

%if 0%{?fedora}%{?eln}
%define ima_ca_cert %{SOURCE106}
%endif

%if 0%{?rhel} && !0%{?eln}
%define ima_ca_cert %{SOURCE103}
%endif

%if 0%{?centos}
%define ima_signing_cert %{SOURCE105}
%else
%define ima_signing_cert %{SOURCE104}
%endif

%define ima_cert_name ima.cer

Source200: check-kabi

Source201: Module.kabi_aarch64
Source202: Module.kabi_ppc64le
Source203: Module.kabi_s390x
Source204: Module.kabi_x86_64
Source205: Module.kabi_riscv64

Source210: Module.kabi_dup_aarch64
Source211: Module.kabi_dup_ppc64le
Source212: Module.kabi_dup_s390x
Source213: Module.kabi_dup_x86_64
Source214: Module.kabi_dup_riscv64

Source300: kernel-abi-stablelists-%{kabiversion}.tar.xz
Source301: kernel-kabi-dw-%{kabiversion}.tar.xz

%if 0%{?include_rt}
%if 0%{?include_rhel}
Source474: %{name}-aarch64-rt-rhel.config
Source475: %{name}-aarch64-rt-debug-rhel.config
Source476: %{name}-aarch64-rt-64k-rhel.config
Source477: %{name}-aarch64-rt-64k-debug-rhel.config
Source478: %{name}-x86_64-rt-rhel.config
Source479: %{name}-x86_64-rt-debug-rhel.config
%endif
%if 0%{?include_fedora}
Source480: %{name}-aarch64-rt-fedora.config
Source481: %{name}-aarch64-rt-debug-fedora.config
Source482: %{name}-aarch64-rt-64k-fedora.config
Source483: %{name}-aarch64-rt-64k-debug-fedora.config
Source484: %{name}-x86_64-rt-fedora.config
Source485: %{name}-x86_64-rt-debug-fedora.config
Source486: %{name}-riscv64-rt-fedora.config
Source487: %{name}-riscv64-rt-debug-fedora.config
%endif
%endif

%if 0%{?include_automotive}
%if %{with_automotive_build}
Source488: %{name}-aarch64-rhel.config
Source489: %{name}-aarch64-debug-rhel.config
Source490: %{name}-x86_64-rhel.config
Source491: %{name}-x86_64-debug-rhel.config
%else
Source488: %{name}-aarch64-automotive-rhel.config
Source489: %{name}-aarch64-automotive-debug-rhel.config
Source490: %{name}-x86_64-automotive-rhel.config
Source491: %{name}-x86_64-automotive-debug-rhel.config
%endif
%endif

Source2002: kvm_stat.logrotate
Source2100: kmap.py

Source3000: merge.py
Source3001: kernel-local
%if %{patchlist_changelog}
Source3002: Patchlist.changelog
%endif

Source4000: README.rst
Source4001: rpminspect.yaml
Source4002: gating.yaml

%if !%{nopatches}
Patch1: patch-%{patchversion}-redhat.patch
%endif

Patch999999: linux-kernel-test.patch
Patch100: kernel.patch

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system. The kernel handles the basic functions of the
operating system: memory allocation, process allocation, device I/O, and
other core tasks.

%if %{with_doc}
%package doc
Summary: Various documentation files from the Linux kernel source
Group: Documentation
BuildArch: noarch
%description doc
This package contains documentation files from the kernel source.
%endif