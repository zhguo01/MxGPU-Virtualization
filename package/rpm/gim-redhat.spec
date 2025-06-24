%define version %(./dkms/get-version | cut -d- -f1)
%define release 1%{dist}

Name: gim
Version: %{version}
Release: %{release}
Summary: GIM driver for RHEL kvm.

License: MIT
URL: https://github.com/amd/mxgpu-virtualization
Source0: ./gim-%{version}.tar.gz
BuildArch: x86_64

BuildRequires: kernel-devel
BuildRequires: make
BuildRequires: gcc
BuildRequires: bc
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cmake
BuildRequires: gcc-c++

%description
This package provides the x86_64 kernel module GIM and amd-smi for supported AMD SR-IOV GPUs

%prep
%setup -q

%build
make all -j

%install
mkdir -p %{buildroot}/lib/modules/5.14.0-427.el9.x86_64/extra/gim
install -m 644 gim.ko %{buildroot}/lib/modules/5.14.0-427.el9.x86_64/extra/gim
mkdir -p %{buildroot}%{_libdir}
install -m 755 smi-lib/build/amdsmi/package/Release/amdsmi/libamdsmi.so %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
install -m 755 smi-lib/cli/cpp/build/amd-smi %{buildroot}%{_bindir}

%post
KERNEL_CURRENT=$(uname -r)
if [ "${KERNEL_CURRENT}" != "5.14.0-427.el9.x86_64" ];then
    if ! [ -L "/lib/modules/$(uname -r)/weak-updates/gim/gim.ko" ];then
        mkdir -p /lib/modules/$(uname -r)/weak-updates/gim
        cd /lib/modules/$(uname -r)/weak-updates/gim/
        ln -s /lib/modules/5.14.0-427.el9.x86_64/extra/gim/gim.ko
    fi
fi
/sbin/depmod -a
/sbin/modprobe gim

%triggerin -- kernel-core
if ! [ -L "/lib/modules/$(uname -r)/weak-updates/gim/gim.ko" ];then
    mkdir -p /lib/modules/$(uname -r)/weak-updates/gim
    cd /lib/modules/$(uname -r)/weak-updates/gim
    ln -s /lib/modules/5.14.0-427.el9.x86_64/extra/gim/gim.ko
fi

%postun
find /lib/modules -depth -type d -name gim -exec rm -rf {} \;
/sbin/modprobe -r gim
/sbin/depmod -a

%files
/lib/modules/5.14.0-427.el9.x86_64/extra/gim/gim.ko
%{_libdir}/libamdsmi.so
%{_bindir}/amd-smi

%changelog
* Mon Mar 17 2025 AMD <sriov@amd.com>
- Placeholder
