%global cubrid_version 9.1.0
%global build_version  0212
%global cubrid_user    cubrid
%global cubridvardir    %{_localstatedir}/%{name}
%global cubridsharedata %{_datarootdir}/%{name}
%global debug_package %{nil}

Summary:       An open source database highly optimized for Web applications
Name:          cubrid
Version:       %{cubrid_version}.%{build_version}
Release:       2%{?dist}
License:       GPLv2+ and BSD
URL:           http://www.cubrid.org
Source0:       http://sourceforge.net/projects/cubrid/files/CUBRID-9.1.0/Linux/Fedora-RPM/%{name}-%{version}.2.tar.gz
Requires:      expect
Requires:      ncurses
Requires:      csh
Requires:      gc
Requires:      lzo
Requires:      pcre
BuildRequires: chrpath
BuildRequires: elfutils-libelf-devel
BuildRequires: ncurses-devel
BuildRequires: texinfo
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: libtool
BuildRequires: ant
BuildRequires: flex
BuildRequires: bison
BuildRequires: byacc
BuildRequires: gc-devel
BuildRequires: lzo-devel
BuildRequires: libedit-devel
BuildRequires: pcre-devel
BuildRequires: libaio-devel
BuildRequires: systemd-units

%description
CUBRID is a comprehensive GPL/BSD open source relational database management system highly optimized for Web Applications. CUBRID is being developed in C and provide buit-in support for high-availability, database sharding, online backup, and other features. JDBC, PHP/PDO, ODBC/OLEDB/.NET, Ruby, Python, Perl, C, and Node.js drivers are available to communicate with CUBRID Server.

%package devel
Summary:    Development files for CUBRID database.
Requires:   %{name}%{?_isa} = %{version}.%{release}

%description devel
%{summary}

%package demodb
Summary:    Sample CUBRID database named demodb.
Requires:   %{name}%{?_isa} = %{version}.%{release}

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
sed -i 's/\r//' README

export LDFLAGS="$LDFLAGS -Wl,--build-id -llzo2"
export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")

./autogen.sh
# We cannot use (%)configure instead of (./)configure because
# (%)configure sets everything including `libdir`, `bindir`, etc.
# If `libdir` is set, CUBRID installation will fail because at this
# moment CUBRID does not support this option. In fact, there are
# other options which are also not supported. CUBRID requires
# most of its libraries to exist under the same directory where
# it is installed. Thus, because we insist on using `./configure`,
# `rpmlint` generates the following warning mesage:
# `W: configure-without-libdir-spec`. This is expected.
./configure ${CUBRID_COMMON_CONFIGURE} --target=$(uname -m) --disable-static --disable-rpath --prefix=%{cubridsharedata}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}/profile.d

#move folders to right locations
if [ -d "%{buildroot}%{cubridsharedata}/bin" ]; then
    mv %{buildroot}%{cubridsharedata}/bin %{buildroot}%{_bindir}
    mv %{buildroot}%{cubridsharedata}/compat %{buildroot}%{_sbindir}
    mv %{buildroot}%{cubridsharedata}/lib %{buildroot}%{_libdir}
    mv %{buildroot}%{cubridsharedata}/conf %{buildroot}%{_sysconfdir}/cubrid
    mv %{buildroot}%{cubridsharedata}/include %{buildroot}%{_includedir}
fi

#remove non-necessary folders
rm -rf %{buildroot}%{cubridsharedata}/log
rm -rf %{buildroot}%{cubridsharedata}/var
rm -rf %{buildroot}%{cubridsharedata}/tmp
rm -rf %{buildroot}%{cubridsharedata}/databases

install -c -p -m 644 contrib/rpm/cubrid.sh %{buildroot}%{_sysconfdir}/profile.d/cubrid.sh
install -c -p -m 644 contrib/rpm/cubrid.csh %{buildroot}%{_sysconfdir}/profile.d/cubrid.csh

install -c -p -m 644 conf/cubrid.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf
install -c -p -m 644 conf/cubrid_broker.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid_broker.conf
install -c -p -m 644 conf/cubrid_ha.conf %{buildroot}%{_sysconfdir}/cubrid/cubrid_ha.conf
install -c -p -m 644 conf/cubrid.conf.large %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf.large
install -c -p -m 644 conf/cubrid.conf.small %{buildroot}%{_sysconfdir}/cubrid/cubrid.conf.small
install -c -p -m 644 cubridmanager/server/cmserver/conf/autoaddvoldb.conf %{buildroot}%{_sysconfdir}/cubrid/autoaddvoldb.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/autobackupdb.conf %{buildroot}%{_sysconfdir}/cubrid/autobackupdb.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/autoexecquery.conf %{buildroot}%{_sysconfdir}/cubrid/autoexecquery.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/autohistory.conf %{buildroot}%{_sysconfdir}/cubrid/autohistory.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/cm.conf %{buildroot}%{_sysconfdir}/cubrid/cm.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/cm.pass %{buildroot}%{_sysconfdir}/cubrid/cm.pass
install -c -p -m 644 cubridmanager/server/cmserver/conf/cmdb.pass %{buildroot}%{_sysconfdir}/cubrid/cmdb.pass
install -c -p -m 644 cubridmanager/server/cmserver/conf/cm_httpd.conf %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/cm_httpd.crt %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.crt
install -c -p -m 644 cubridmanager/server/cmserver/conf/cm_httpd.key %{buildroot}%{_sysconfdir}/cubrid/cm_httpd.key
install -c -p -m 644 cubridmanager/server/cmserver/conf/diagactivitytemplate.conf %{buildroot}%{_sysconfdir}/cubrid/diagactivitytemplate.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/diagstatustemplate.conf %{buildroot}%{_sysconfdir}/cubrid/diagstatustemplate.conf
install -c -p -m 644 cubridmanager/server/cmserver/conf/mime.types %{buildroot}%{_sysconfdir}/cubrid/mime.types

install -d %{buildroot}%{_unitdir}
install -c -p -m 644 contrib/init.d/cubrid.service %{buildroot}%{_unitdir}/cubrid.service

chmod -R ugo-x,ugo+rX %{buildroot}%{cubridsharedata}/msg

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}

find %{buildroot} -size 0 -delete

if [ ! -L %{buildroot}%{cubridsharedata}/log ]; then
    ln -s %{cubridvardir}/log %{buildroot}%{cubridsharedata}/log
    ln -s %{cubridvardir}/tmp %{buildroot}%{cubridsharedata}/tmp
    ln -s %{cubridvardir}/var %{buildroot}%{cubridsharedata}/var
    ln -s %{cubridvardir}/databases %{buildroot}%{cubridsharedata}/databases
fi

if [ ! -L "%{buildroot}%{cubridsharedata}/lib" ]; then
    ln -s %{_libdir} %{buildroot}%{cubridsharedata}/lib
fi

if [ ! -L "%{buildroot}%{cubridsharedata}/conf" ]; then
    ln -s %{_sysconfdir}/cubrid %{buildroot}%{cubridsharedata}/conf
fi

if [ ! -L "%{buildroot}%{cubridsharedata}/bin" ]; then
    ln -s %{_bindir} %{buildroot}%{cubridsharedata}/bin
fi

if [ ! -L "%{buildroot}%{cubridsharedata}/compat" ]; then
    ln -s %{_sbindir} %{buildroot}%{cubridsharedata}/compat
fi

chmod -x %{buildroot}%{cubridsharedata}/share/rpm/cubrid.sh
chmod -x %{buildroot}%{cubridsharedata}/share/rpm/cubrid.csh
chmod -x %{buildroot}%{cubridsharedata}/share/scripts/check_reserved.sql

if [ ! -f %{buildroot}%{_bindir}/cubrid_app ]; then
    install -c -p -m 755 %{buildroot}%{_bindir}/cubrid %{buildroot}%{_bindir}/cubrid_app
fi

if [ ! -f %{buildroot}%{_bindir}/csql_app ]; then
    install -c -p -m 755 %{buildroot}%{_bindir}/csql %{buildroot}%{_bindir}/csql_app
fi

install -c -p -m 755 contrib/scripts/cubrid %{buildroot}%{_bindir}/cubrid
install -c -p -m 755 contrib/scripts/csql %{buildroot}%{_bindir}/csql

chmod +x %{buildroot}%{cubridsharedata}/locales/loclib/build_locale.sh

#remove .la libraries
rm -rf %{buildroot}%{_libdir}/*.la

#remove rpaths
chrpath -d %{buildroot}%{_bindir}/cm_admin
chrpath -d %{buildroot}%{_bindir}/cub_auto
chrpath -d %{buildroot}%{_bindir}/cub_job
chrpath -d %{buildroot}%{_bindir}/cub_js
chrpath -d %{buildroot}%{_bindir}/cubrid_rel
chrpath -d %{buildroot}%{_bindir}/broker_log_converter
chrpath -d %{buildroot}%{_bindir}/broker_monitor
chrpath -d %{buildroot}%{_bindir}/cub_master
chrpath -d %{buildroot}%{_bindir}/shard_proxy
chrpath -d %{buildroot}%{_bindir}/shard_broker
chrpath -d %{buildroot}%{_bindir}/cub_jobsa
chrpath -d %{buildroot}%{_bindir}/cub_commdb
chrpath -d %{buildroot}%{_bindir}/shard_broker_log_top
chrpath -d %{buildroot}%{_bindir}/loadjava
chrpath -d %{buildroot}%{_bindir}/shard_broker_monitor
chrpath -d %{buildroot}%{_bindir}/shard_broker_log_runner
chrpath -d %{buildroot}%{_bindir}/shard_cas
chrpath -d %{buildroot}%{_bindir}/cub_cas
chrpath -d %{buildroot}%{_bindir}/broker_log_top
chrpath -d %{buildroot}%{_bindir}/shard_admin
chrpath -d %{buildroot}%{_bindir}/cub_broker
chrpath -d %{buildroot}%{_bindir}/broker_log_runner
chrpath -d %{buildroot}%{_bindir}/cub_sainfo
chrpath -d %{buildroot}%{_bindir}/shard_broker_log_converter
chrpath -d %{buildroot}%{_bindir}/cubrid_esql
chrpath -d %{buildroot}%{_bindir}/cubrid_broker
chrpath -d %{buildroot}%{_bindir}/cub_cmserver
chrpath -d %{buildroot}%{_bindir}/broker_changer
chrpath -d %{buildroot}%{_bindir}/cub_server
chrpath -d %{buildroot}%{_bindir}/cub_jobfile
chrpath -d %{buildroot}%{_bindir}/shard_broker_changer
chrpath -d %{buildroot}%{_bindir}/migrate_90beta_to_91
chrpath -d %{buildroot}%{_sbindir}/get_disk_compat
chrpath -d %{buildroot}%{_sbindir}/load_noopt
chrpath -d %{buildroot}%{_sbindir}/convert_password
chrpath -d %{buildroot}%{_libdir}/libcmstat.so.%{cubrid_version}
chrpath -d %{buildroot}%{_libdir}/libshardbrokeradmin.so.%{cubrid_version}
chrpath -d %{buildroot}%{_libdir}/libcmdep.so.%{cubrid_version}
chrpath -d %{buildroot}%{_libdir}/libbrokeradmin.so.%{cubrid_version}
chrpath -d %{buildroot}%{_bindir}/cubrid_app

chmod +x %{buildroot}%{_bindir}/*
chmod +x %{buildroot}%{_sbindir}/*
chmod +x %{buildroot}%{_libdir}/*

%pre

if [ ! -z "`getent passwd $CUBRID_USER`" ] && [ -e %{_prefix}/bin/cubrid ]; then
    su -l -s $SHELL $CUBRID_USER -c ". /etc/profile.d/cubrid.sh; cubrid service stop > /dev/null 2>&1"
fi

#only on install (not on upgrade or reinstall)
if [ $1 -eq 1 ] ; then
    getent group %{cubrid_user} >/dev/null || groupadd -r %{cubrid_user}
    getent passwd %{cubrid_user} >/dev/null || useradd -r -g %{cubrid_user} -d %{_prefix}/share/cubrid -s /sbin/nologin -c "runs the cubrid database service" %{cubrid_user}
fi

%post
%systemd_post cubrid.service
/sbin/ldconfig

#only on install (not on upgrade or reinstall)
if [ $1 -eq 1 ] ; then
    mkdir -p %{cubridvardir}/log
    mkdir -p %{cubridvardir}/var
    mkdir -p %{cubridvardir}/tmp
    mkdir -p %{cubridvardir}/databases
    touch %{cubridvardir}/databases/databases.txt
    chown %{cubrid_user}:%{cubrid_user} -R %{cubridvardir}
    systemctl enable cubrid.service > /dev/null 2>&1
fi

#cubrid master service cannot start if folder is not owned by user cubrid
chown %{cubrid_user}:%{cubrid_user} %{cubridsharedata}

%preun
%systemd_preun cubrid.service
/sbin/ldconfig

if [ ! -z "`getent passwd $CUBRID_USER`" ] && [ -e %{_prefix}/bin/cubrid ]; then
    su -l -s $SHELL $CUBRID_USER -c ". /etc/profile.d/cubrid.sh; cubrid service stop > /dev/null 2>&1"
fi

if [ $1 -eq 0 ] ; then
    systemctl disable cubrid.service > /dev/null 2>&1
fi

%postun
%systemd_postun cubrid.service
/sbin/ldconfig

%post demodb
%{_prefix}/share/cubrid/demo/make_cubrid_demo.sh > /dev/null 2>&1
su -l -s $SHELL %{cubrid_user} -c ". /etc/profile.d/cubrid.sh; cubrid server start demodb > /dev/null 2>&1"

%postun demodb
su -l -s $SHELL %{cubrid_user} -c ". /etc/profile.d/cubrid.sh; cubrid server stop demodb > /dev/null 2>&1; cubrid deletedb demodb > /dev/null 2>&1"

%clean

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
%{_includedir}/DBGWConfigurationFwd.h
%{_includedir}/DBGWSynchronizedResource.h
%{_includedir}/DBGWWork.h
%{_includedir}/DBGWWorkFwd.h

%files demodb
# `demodb` demo database is not a sample database publicly
# available on the Internet. It is just a demo database
# distributed together with CUBRID binaries. `demodb`
# database can be installed only by cubrid user, and
# since the related files are stored in
# `/usr/share/cubrid/demo`, it is logical that they are
# owned by the same cubrid user.
%defattr(-,cubrid_user,cubrid_user,-)
%{cubridsharedata}/demo

%files
%doc CREDITS README

%{_bindir}/broker_changer
%{_bindir}/broker_log_converter
%{_bindir}/broker_log_runner
%{_bindir}/broker_log_top
%{_bindir}/broker_monitor
%{_bindir}/csql
%{_bindir}/cub_admin
%{_bindir}/cub_broker
%{_bindir}/cub_cas
%{_bindir}/cub_cmhttpd
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
%{_bindir}/make_locale.sh
%{_bindir}/migrate_90beta_to_91

%{_libdir}/libshardbrokeradmin.so
%{_libdir}/libshardbrokeradmin.so.9
%{_libdir}/libshardbrokeradmin.so.%{cubrid_version}
%{_libdir}/libcubridesql.so
%{_libdir}/libbrokeradmin.so
%{_libdir}/libcascci.so
%{_libdir}/libcmdep.so
%{_libdir}/libcubrid.so
%{_libdir}/libcubridcs.so
%{_libdir}/libcubridsa.so
%{_libdir}/libcmstat.so
%{_libdir}/libbrokeradmin.so.%{cubrid_version}
%{_libdir}/libbrokeradmin.so.9
%{_libdir}/libcascci.so.%{cubrid_version}
%{_libdir}/libcascci.so.9
%{_libdir}/libcmdep.so.%{cubrid_version}
%{_libdir}/libcmdep.so.9
%{_libdir}/libcubrid.so.0.0.0
%{_libdir}/libcubrid.so.0
%{_libdir}/libcubridcs.so.0.0.0
%{_libdir}/libcubridcs.so.0
%{_libdir}/libcubridsa.so.0.0.0
%{_libdir}/libcubridsa.so.0
%{_libdir}/libcmstat.so.%{cubrid_version}
%{_libdir}/libcmstat.so.9
%{_libdir}/libcubridesql.so.%{cubrid_version}
%{_libdir}/libcubridesql.so.9

%{_sbindir}/addvoldb
%{_sbindir}/backupdb
%{_sbindir}/checkdb
%{_sbindir}/commdb
%{_sbindir}/compactdb
%{_sbindir}/convert_password
%{_sbindir}/copydb
%{_sbindir}/createdb
%{_sbindir}/deletedb
%{_sbindir}/get_disk_compat
%{_sbindir}/installdb
%{_sbindir}/killtran
%{_sbindir}/load_noopt
%{_sbindir}/loaddb
%{_sbindir}/lockdb
%{_sbindir}/optimizedb
%{_sbindir}/renamedb
%{_sbindir}/restoredb
%{_sbindir}/spacedb
%{_sbindir}/sqlx
%{_sbindir}/start_cubrid
%{_sbindir}/start_server
%{_sbindir}/stop_cubrid
%{_sbindir}/stop_server
%{_sbindir}/uc
%{_sbindir}/unloaddb

%{_unitdir}/cubrid.service

%config(noreplace) %{_sysconfdir}/profile.d/cubrid.sh
%config(noreplace) %{_sysconfdir}/profile.d/cubrid.csh

%{cubridsharedata}/msg
%{cubridsharedata}/java
%{cubridsharedata}/jdbc
%{cubridsharedata}/share
%{cubridsharedata}/lib
%{cubridsharedata}/bin
%{cubridsharedata}/compat
%{cubridsharedata}/locales

%defattr(-,cubrid_user,cubrid_user,-)
%config(noreplace) %{_sysconfdir}/cubrid
%{cubridsharedata}/conf
%{cubridsharedata}/databases
%{cubridsharedata}/log
%{cubridsharedata}/tmp
%{cubridsharedata}/var

%changelog
* Wed Aug 07 2013 CUBRID Developers<contact@cubrid.org> - 9.1.0.0212-2
- Removed `systemd` as suggested by at
  https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54
- Added `release` to version `Require` as suggested at
  https://bugzilla.redhat.com/show_bug.cgi?id=658754#c55.
- Added code comments.
- For consistency, replaced `cubrid` user with `cubrid_user`
  as suggested at
  https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54.

* Mon Apr 01 2013 CUBRID Developers<contact@cubrid.org> - 9.1.0.0212-1
- Upgraded to 9.1.0.0212
- Changed the way the files are located
- Moved libraries to lib64 folder on 64 bit systems

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
