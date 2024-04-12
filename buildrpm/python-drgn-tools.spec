# Copyright (c) 2024, Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
Name:           python-drgn-tools
Version:        0.8.0
Release:        1%{?dist}
Summary:        Helper scripts for drgn, containing the corelens utility

License:        UPL
URL:            https://github.com/oracle-samples/drgn-tools
Source0:        drgn-tools-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel

%global python_wheelname drgn_tools-%{version}-py3-none-any.whl

# The drgn dependency can be fulfilled by drgn with, or without, CTF support.
# However, drgn-tools is tied to a specific drgn release.
Requires:       drgn >= 0.0.25, drgn < 0.0.26

%description
drgn-tools extends the drgn debugger with scripts & helpers developed by the
Oracle Linux Sustaining team. It provides a program called "corelens" which
allows users to extract diagnostic information from a kernel core dump, or from
a running kernel image (via /proc/kcore).

%prep
%autosetup -n drgn-tools-%{version}
echo '__version__ = "%{version}"' > drgn_tools/_version.py
rm -rf drgn_tools/v2/

%build
%py3_build_wheel


%install
%py3_install_wheel %{python_wheelname}
gzip -k man/corelens.1
install -m644 -Dt %{buildroot}%{_mandir}/man1/ man/corelens.1.gz

# The DRGN script is an interactive CLI which is convenient for developers,
# but should not be part of general users' PATH. If necessary, it can be invoked
# manually with "python3 -m drgn_tools.cli"
rm %{buildroot}/usr/bin/DRGN

%files -n python-drgn-tools
%license LICENSE.txt
%{python3_sitelib}/drgn_tools-*.dist-info/
%{python3_sitelib}/drgn_tools/*
/usr/bin/corelens
%{_mandir}/man1/corelens.1.gz

%changelog
* Thu Feb 01 2024 Stephen Brennan <stephen.s.brennan@oracle.com> - 0.8.0-1
- Update to 0.8.0

* Wed Dec 20 2023 Stephen Brennan <stephen.s.brennan@oracle.com> - 0.6.0-1
- Initial packaging