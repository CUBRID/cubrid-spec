%define cubrid_version 8.4.3
%define build_version  0150
%define file_version   1
%define cubrid_vendor  Search Solution Corporation
%define release        1
%define cubrid_user    cubrid
%define cubridcompatdir %{_sbindir}
%define cubridvardir    %{_localstatedir}/%{name}
%define cubridsharedata %{_datarootdir}/%{name}  
%define cubridmsgdir    %{cubridsharedata}/msg  
%define cubridjdbcdir   %{cubridsharedata}/jdbc
%define cubridjavadir   %{cubridsharedata}/java
%define libdir          %{_prefix}/lib

%if 0%{?fedora} > 16
%define java_version    1.7.0
%else
%define java_version    1.6.0
%endif

Summary:       An open source database highly optimized for Web applications
Name:          cubrid
Version:       %{cubrid_version}.%{build_version}
Release:       %{release}%{?dist}
License:       GPLv2+ and BSD
Group:         Applications/Databases
URL:           http://www.cubrid.org
Source0:       http://sourceforge.net/projects/cubrid/files/CUBRID-8.4.1/Linux/Fedora-RPM/%{name}-%{cubrid_version}.%{build_version}.%{file_version}.tar.gz
Requires:      expect
Requires:      ncurses
Requires:      csh
Requires:      gc
Requires:      lzo
Requires:      pcre
Requires:      python
BuildRequires: chrpath
BuildRequires: elfutils-libelf-devel
BuildRequires: ncurses-devel
BuildRequires: texinfo
BuildRequires: java-%{java_version}-openjdk-devel
BuildRequires: ant
BuildRequires: flex
BuildRequires: bison
BuildRequires: byacc
BuildRequires: gc-devel
BuildRequires: glibc-devel
BuildRequires: lzo-devel
BuildRequires: libedit-devel
BuildRequires: pcre-devel
BuildRequires: libaio-devel
%if 0%{?fedora} >= 15
BuildRequires: systemd-units
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%description
CUBRID is a comprehensive GPL/BSD open source relational database management
system highly optimized for Web Applications. CUBRID is being developed in 
C/C++. It includes HA, online backup, and other features, such as JDBC, PHP,
ODBC/.NET, Ruby & Python APIs.

%package devel 
Summary:    Development files for CUBRID database
Group:      Development/Libraries
Requires:   %{name} = %{cubrid_version}.%{build_version}

%description devel
%{summary}

%package demodb 
Summary:    Sample CUBRID database named demodb
Group:      Development/Libraries
Requires:   %{name} = %{cubrid_version}.%{build_version}

%description demodb
%{summary}

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch x86_64
    CFLAGS=" -m64 " 
    CUBRID_COMMON_CONFIGURE="${CUBRID_COMMON_CONFIGURE} --enable-64bit"
%endif

rm -f external/bison-2.3/config.status

export LDFLAGS="$LDFLAGS -Wl,--build-id -llzo2"
export JAVA_HOME=%{libdir}/jvm/java-%{java_version}

./configure ${CUBRID_COMMON_CONFIGURE} --with-demodir=%{cubridsharedata}/demo --with-compatdir=%{cubridcompatdir} --target=$(uname -m) --disable-static --disable-rpath  --prefix=%{_prefix}  --with-msgdir=%{cubridmsgdir} --with-jdbcdir=%{cubridjdbcdir} --with-jspdir=%{cubridjavadir} 

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}/cubrid
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{_sysconfdir}/profile.d
install -d %{buildroot}%{cubridsharedata}/demo/

install -c -m 644 contrib/rpm/cubrid.sh %{buildroot}%{_sysconfdir}/profile.d/cubrid.sh
install -c -m 644 contrib/rpm/cubrid.csh %{buildroot}%{_sysconfdir}/profile.d/cubrid.csh

install -c -m 644 conf/cubrid.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf
install -c -m 644 conf/cubrid_broker.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid_broker.conf
install -c -m 644 conf/cubrid_ha.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid_ha.conf
install -c -m 644 conf/cubrid.conf.large %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf.large
install -c -m 644 conf/cubrid.conf.small %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf.small
install -c -m 644 cubridmanager/server/cmserver/conf/autoaddvoldb.conf %{buildroot}%{_sysconfdir}/cubrid/autoaddvoldb.conf
install -c -m 644 cubridmanager/server/cmserver/conf/autobackupdb.conf %{buildroot}%{_sysconfdir}/cubrid/autobackupdb.conf
install -c -m 644 cubridmanager/server/cmserver/conf/autoexecquery.conf %{buildroot}%{_sysconfdir}/cubrid/autoexecquery.conf
install -c -m 644 cubridmanager/server/cmserver/conf/autohistory.conf %{buildroot}%{_sysconfdir}/cubrid/autohistory.conf
install -c -m 644 cubridmanager/server/cmserver/conf/cm.conf %{buildroot}%{_sysconfdir}/cubrid/cm.conf
install -c -m 644 cubridmanager/server/cmserver/conf/cm.pass %{buildroot}%{_sysconfdir}/cubrid/cm.pass
install -c -m 644 cubridmanager/server/cmserver/conf/cmdb.pass %{buildroot}%{_sysconfdir}/cubrid/cmdb.pass
install -c -m 644 cubridmanager/server/cmserver/conf/cm_httpd.conf %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.conf
install -c -m 644 cubridmanager/server/cmserver/conf/cm_httpd.crt %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.crt
install -c -m 644 cubridmanager/server/cmserver/conf/cm_httpd.key %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.key
install -c -m 644 cubridmanager/server/cmserver/conf/diagactivitytemplate.conf %{buildroot}%{_sysconfdir}/cubrid/diagactivitytemplate.conf
install -c -m 644 cubridmanager/server/cmserver/conf/diagstatustemplate.conf %{buildroot}%{_sysconfdir}/cubrid/diagstatustemplate.conf

%if 0%{?fedora} >= 15
install -d %{buildroot}%{_unitdir}
install -c -m 644 contrib/init.d/cubrid.service %{buildroot}%{_unitdir}/cubrid.service
%else
install -d %{buildroot}%{_initddir}
install -c -m 755 contrib/init.d/cubrid %{buildroot}%{_initddir}/cubrid
%endif


chmod -R ugo-x,ugo+rX %{buildroot}%{cubridmsgdir}

chrpath -d %{buildroot}%{_bindir}/cm_admin
chrpath -d %{buildroot}%{_bindir}/cub_auto
chrpath -d %{buildroot}%{_bindir}/cub_job
chrpath -d %{buildroot}%{_bindir}/cub_js

find %{buildroot} -size 0 -delete

if [ ! -L %{buildroot}%{_prefix}/share/cubrid/log ]; then
    ln -s %{cubridvardir}/log %{buildroot}%{_prefix}/share/cubrid/log 
    ln -s %{cubridvardir}/tmp %{buildroot}%{_prefix}/share/cubrid/tmp
    ln -s %{cubridvardir}/var %{buildroot}%{_prefix}/share/cubrid/var
    ln -s %{cubridvardir}/databases %{buildroot}%{_prefix}/share/cubrid/databases
    ln -s %{libdir} %{buildroot}%{_prefix}/share/cubrid/lib
    ln -s %{_sysconfdir}/cubrid %{buildroot}%{_prefix}/share/cubrid/conf
    ln -s %{_prefix}/bin %{buildroot}%{_prefix}/share/cubrid/bin
    ln -s %{cubridcompatdir} %{buildroot}%{_prefix}/share/cubrid/compat
fi

if [ -d %{buildroot}%{_prefix}/share/rpm ]; then
    cp -R %{buildroot}%{_prefix}/share/rpm %{buildroot}%{cubridsharedata}/
    cp -R %{buildroot}%{_prefix}/share/init.d %{buildroot}%{cubridsharedata}/
    cp -R %{buildroot}%{_prefix}/share/scripts %{buildroot}%{cubridsharedata}/

    rm -rf %{buildroot}%{_prefix}/share/rpm
    rm -rf %{buildroot}%{_prefix}/share/init.d
    rm -rf %{buildroot}%{_prefix}/share/scripts

    chmod -x %{buildroot}%{cubridsharedata}/rpm/cubrid.sh
    chmod -x %{buildroot}%{cubridsharedata}/rpm/cubrid.csh
    chmod -x %{buildroot}%{cubridsharedata}/scripts/check_reserved.sql
fi

rm -rf %{buildroot}%{_prefix}/conf
rm -rf %{buildroot}%{_prefix}/log
rm -rf %{buildroot}%{_prefix}/tmp
rm -rf %{buildroot}%{_prefix}/var

if [ ! -f %{buildroot}%{_bindir}/cubrid_app ]; then
    install -c -m 755 %{buildroot}%{_bindir}/cubrid %{buildroot}%{_bindir}/cubrid_app
fi

if [ ! -f %{buildroot}%{_bindir}/csql_app ]; then
    install -c -m 755 %{buildroot}%{_bindir}/csql %{buildroot}%{_bindir}/csql_app
fi

install -c -m 755 contrib/scripts/cubrid %{buildroot}%{_bindir}/cubrid
install -c -m 755 contrib/scripts/csql %{buildroot}%{_bindir}/csql

#fix .la libraries
sed -i 's/-L\/home\/user\/rpmbuild\/BUILD\/cubrid-8.4.3.0150\/cci -L\/home\/user\/rpmbuild\/BUILD\/cubrid-8.4.3.0150\/cs //g' %{buildroot}%{libdir}/*.la

%pre

if [ ! -z "`getent passwd $CUBRID_USER`" ] && [ -e %{_prefix}/bin/cubrid ]; then
    su -l -s $SHELL $CUBRID_USER -c "cubrid service stop > /dev/null 2>&1"
fi

#only on install (not on upgrade or reinstall)
if [ $1 -eq 1 ] ; then
    getent group %{cubrid_user} >/dev/null || groupadd -r %{cubrid_user}
    getent passwd %{cubrid_user} >/dev/null || useradd -r -g %{cubrid_user} -d %{_prefix}/share/cubrid -s /sbin/nologin -c "runs the cubrid database service" %{cubrid_user}
fi

%post 
/sbin/ldconfig

#only on install (not on upgrade or reinstall)
if [ $1 -eq 1 ] ; then
    mkdir -p %{cubridvardir}/log
    mkdir -p %{cubridvardir}/var
    mkdir -p %{cubridvardir}/tmp
    mkdir -p %{cubridvardir}/databases
    chown %{cubrid_user}:%{cubrid_user} -R %{cubridvardir} 
    %if 0%{?fedora} >= 15
         systemctl enable cubrid.service > /dev/null 2>&1
    %else
         /sbin/chkconfig --add cubrid
    %endif
fi

#cubrid master service cannot start if folder is not owned by user cubrid
chown %{cubrid_user}:%{cubrid_user} %{cubridsharedata}

%post devel -p /sbin/ldconfig

%post demodb 
/sbin/ldconfig

%{_prefix}/share/cubrid/demo/make_cubrid_demo.sh > /dev/null 2>&1
su -l -s $SHELL %{cubrid_user} -c ". /etc/profile.d/cubrid.sh; cubrid server start demodb > /dev/null 2>&1"

%preun 

/sbin/ldconfig

if [ ! -z "`getent passwd $CUBRID_USER`" ] && [ -e %{_prefix}/bin/cubrid ]; then
    su -l -s $SHELL $CUBRID_USER -c "cubrid service stop > /dev/null 2>&1"
fi

if [ $1 -eq 0 ] ; then
    %if 0%{?fedora} >= 15
         systemctl disable cubrid.service > /dev/null 2>&1
    %else
         /sbin/chkconfig --del cubrid
    %endif
fi

%preun devel -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%postun demodb 
/sbin/ldconfig
su -l -s $SHELL %{cubrid_user} -c ". /etc/profile.d/cubrid.sh; cubrid server stop demodb > /dev/null 2>&1; cubrid deletedb demodb > /dev/null 2>&1"

%clean
rm -rf %{buildroot}

%files devel
%{_includedir}/cas_cci.h
%{_includedir}/cas_error.h
%{_includedir}/cm_dep.h
%{_includedir}/cm_stat.h
%{_includedir}/cubrid_esql.h
%{_includedir}/dbi.h
%{_includedir}/DBGWAdapter.h
%{_includedir}/DBGWClient.h
%{_includedir}/DBGWClientFwd.h
%{_includedir}/DBGWCommon.h
%{_includedir}/DBGWConfiguration.h
%{_includedir}/DBGWDataBaseInterface.h
%{_includedir}/DBGWError.h
%{_includedir}/DBGWLogger.h
%{_includedir}/DBGWMock.h
%{_includedir}/DBGWPorting.h
%{_includedir}/DBGWQuery.h
%{_includedir}/DBGWValue.h
%{_includedir}/cci_log.h
%{_includedir}/shard_key.h

%files demodb
%defattr(-,cubrid,cubrid,-)
%{cubridsharedata}/demo

%files
%doc COPYING CREDITS README

%defattr(-,root,root,-)
%{_bindir}/broker_changer
%{_bindir}/broker_log_converter
%{_bindir}/broker_log_runner
%{_bindir}/broker_log_top
%{_bindir}/broker_monitor
%{_bindir}/csql
%{_bindir}/cub_admin
%{_bindir}/cub_broker
%{_bindir}/cub_cas
%{_bindir}/cub_commdb
%{_bindir}/cub_jobsa
%{_bindir}/cub_master
%{_bindir}/cub_sainfo
%{_bindir}/cub_server
%{_bindir}/cubrid
%{_bindir}/csql_app
%{_bindir}/cubrid_app
%{_bindir}/cubrid_broker
%{_bindir}/cubrid_esql
%{_bindir}/cubrid_rel
%{_bindir}/loadjava
%{_bindir}/cm_admin
%{_bindir}/cub_auto
%{_bindir}/cub_job
%{_bindir}/cub_js
%{_bindir}/cub_cmserver
%{_bindir}/cub_jobfile
%{_bindir}/shard_admin
%{_bindir}/shard_broker
%{_bindir}/shard_broker_changer
%{_bindir}/shard_broker_log_converter
%{_bindir}/shard_broker_log_runner
%{_bindir}/shard_broker_log_top
%{_bindir}/shard_broker_monitor
%{_bindir}/shard_cas
%{_bindir}/shard_proxy

%{libdir}/libshardbrokeradmin.la
%{libdir}/libshardbrokeradmin.so
%{libdir}/libshardbrokeradmin.so.8
%{libdir}/libshardbrokeradmin.so.%{cubrid_version}
%{libdir}/libbrokeradmin.la
%{libdir}/libcascci.la
%{libdir}/libcmdep.la
%{libdir}/libcmstat.la
%{libdir}/libcubrid.la
%{libdir}/libcubridcs.la
%{libdir}/libcubridesql.la
%{libdir}/libcubridesql.so
%{libdir}/libcubridsa.la
%{libdir}/libbrokeradmin.so
%{libdir}/libcascci.so
%{libdir}/libcmdep.so
%{libdir}/libcubrid.so
%{libdir}/libcubridcs.so
%{libdir}/libcubridsa.so
%{libdir}/libcmstat.so
%{libdir}/libbrokeradmin.so.%{cubrid_version}
%{libdir}/libbrokeradmin.so.8
%{libdir}/libcascci.so.%{cubrid_version}
%{libdir}/libcascci.so.8
%{libdir}/libcmdep.so.%{cubrid_version}
%{libdir}/libcmdep.so.8
%{libdir}/libcubrid.so.%{cubrid_version}
%{libdir}/libcubrid.so.8
%{libdir}/libcubridcs.so.%{cubrid_version}
%{libdir}/libcubridcs.so.8
%{libdir}/libcubridsa.so.%{cubrid_version}
%{libdir}/libcubridsa.so.8
%{libdir}/libcmstat.so.%{cubrid_version}
%{libdir}/libcmstat.so.8
%{libdir}/libcubridesql.so.%{cubrid_version}
%{libdir}/libcubridesql.so.8

%{cubridcompatdir}/addvoldb
%{cubridcompatdir}/backupdb
%{cubridcompatdir}/checkdb
%{cubridcompatdir}/commdb
%{cubridcompatdir}/compactdb
%{cubridcompatdir}/convert_password
%{cubridcompatdir}/copydb
%{cubridcompatdir}/createdb
%{cubridcompatdir}/deletedb
%{cubridcompatdir}/get_disk_compat
%{cubridcompatdir}/installdb
%{cubridcompatdir}/killtran
%{cubridcompatdir}/load_noopt
%{cubridcompatdir}/loaddb
%{cubridcompatdir}/lockdb
%{cubridcompatdir}/optimizedb
%{cubridcompatdir}/renamedb
%{cubridcompatdir}/restoredb
%{cubridcompatdir}/spacedb
%{cubridcompatdir}/sqlx
%{cubridcompatdir}/start_cubrid
%{cubridcompatdir}/start_server
%{cubridcompatdir}/stop_cubrid
%{cubridcompatdir}/stop_server
%{cubridcompatdir}/uc
%{cubridcompatdir}/unloaddb

%if 0%{?fedora} >= 15
    %{_unitdir}/cubrid.service
%else
    %{_initddir}/cubrid
%endif

%config(noreplace) %{_sysconfdir}/profile.d/cubrid.sh
%config(noreplace) %{_sysconfdir}/profile.d/cubrid.csh

%{cubridsharedata}/msg
%{cubridsharedata}/java
%{cubridsharedata}/jdbc
%{cubridsharedata}/init.d
%{cubridsharedata}/rpm
%{cubridsharedata}/scripts
%{cubridsharedata}/lib
%{cubridsharedata}/bin
%{cubridsharedata}/compat

%defattr(-,cubrid,cubrid,-)
%config(noreplace) %{_sysconfdir}/cubrid
%{cubridsharedata}/conf
%{cubridsharedata}/databases
%{cubridsharedata}/log
%{cubridsharedata}/tmp
%{cubridsharedata}/var

%changelog
* Mon Nov 26 2012 CUBRID Developers<contact@cubrid.org> - 8.4.3.0150-1
- Upgraded to 8.4.3.0150
- Added new files
- Fixed bug within source cm_server_interface.cpp file

* Thu Aug 23 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.6004-1
- Fixed bug in init.d cubrid script

* Fri Jul 27 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.5002-1
- Changed cubrid script to avoid permission errors
- Added csql redirect script to avoid standalone problems
- Fixed demodb post/postun scripts to run commands as cubrid user
- Set root:root as user/group for files in /usr/share that only require read access

* Wed Jul 11 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.2032-4
- Edited macros for share and include folders
- changed address in include/system.h to avoid incorrect-fsf-address
- removed strip commands to avoid empty-debuginfo-package error.
- removing strip commands now gives warnings: "W: unstripped-binary-or-object"

* Tue Jul 10 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.2032-3
- Edited cubrid.sh and cubrid.csh files

* Fri Jul 6 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.2032-2
- Added 'StandardOutput=syslog' and 'TimeoutSec=300' to cubrid systemd file
- Removed SysV script for Fedora >= 15
- Removed chkconfig calls for Fedora >= 15

* Thu Jul 5 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.2032-1
- Added conditionals to recognize java version (1.7.0 since Fedora 17, 1.6.0 up to Fedora 16)
- Removed 'service start' from the post install section
- Added file_version to keep track of source file

* Fri Jun 29 2012 CUBRID Developers<contact@cubrid.org>
- Moved {_bindir}/cubrid inside the source archive
- Removed userdel call from postun
- Removed unnecessary dependencies (glibc-devel, libstdc++-devel)
- Set root as user and group for libraries and executables
- Removed message after installation (no news is good news)
- Added systemctl calls in scripts
