# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define cubridname cubrid

Name:		python-cubrid
Version:	8.4.3.0001
Release:	1%{?dist}
Summary:	Python API for CUBRID database
License:	GPLv2+ and BSD
URL:		http://www.cubrid.org
Source0:	https://sourceforge.net/projects/cubrid/files/CUBRID-8.4.3/Linux/Fedora-RPM/%{name}-%{version}.tar.gz

BuildRequires:	python-devel
BuildRequires:	%{cubridname}-devel
Requires:	python >= 2.5

%description
This package installs the cubrid.so file required to connect to CUBRID
databases from within Python code.

%prep
%setup -q

%build
# Remove CFLAGS=... for noarch packages (unneeded)
CUBRID=/usr/include CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
CUBRID=/usr/include %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

strip --strip-unneeded $RPM_BUILD_ROOT%{python_sitearch}/_cubrid.so
 
%files
%doc
# For arch-specific packages: sitearch
%{python_sitearch}/*

%changelog
* Wed Mar 23 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.0001-1
APIS-91 - Fetchone get numeric data's type is not correct
APIS-93 - The format of Cubrid Date/Time/Timestamp string are different from Python's
