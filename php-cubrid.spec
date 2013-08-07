%define cubridname cubrid

Name:       php-cubrid
Version:    9.1.0.0001
Release:    1%{?dist}
Summary:    PHP API for CUBRID database
License:    GPLv2+ and BSD
URL:        http://www.cubrid.org
Source0:    https://sourceforge.net/projects/cubrid/files/CUBRID-9.1.0/Linux/Fedora-RPM/%{name}-%{version}.tar.gz

BuildRequires: %{cubridname}-devel
BuildRequires: php-devel
Requires:      php >= 5.3

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%description
This package installs the php_cubrid.so file required to connect to CUBRID
databases from within PHP code.

%prep
%setup -q

%build
phpize --clean
phpize
%configure --with-cubrid=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{php_extdir}
echo "moving to extensions directory :" %{php_extdir}

strip --strip-unneeded .libs/cubrid.so

mv  .libs/cubrid.so $RPM_BUILD_ROOT/%{php_extdir}  

%files
%{php_extdir}/cubrid.so

%doc

#make sure we register libraries in php ini 
%post
if [ -d %{_sysconfdir}/php.d ]; then
    CUBRID_INI=%{_sysconfdir}/php.d/cubrid.ini     
    echo  ";Enable cubrid php api module" > $CUBRID_INI
    echo "extension=cubrid.so" >> $CUBRID_INI
    echo "PHP ini changed to load CUBRID API. Check out: " $CUBRID_INI
else
    echo "cannot install php configuration in %{_sysconfdir}/php.d/cubrid.ini, please adjust your setup with extension=libphp_cubrid.so"
fi

%postun
rm -rf %{_sysconfdir}/php.d/cubrid.ini

%changelog
* Wed Jul 4 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.0004-1
We have added functions about lob object in this version and these functions have been tested carefully.
If you want to get more information about the bugs or if you need help, please go to
http://jira.cubrid.org/browse/APIS.
The following functions have been added:
- cubrid_lob2_new
- cubrid_lob2_bind
- cubrid_lob2_export
- cubrid_lob2_import
- cubrid_lob2_read
- cubrid_lob2_write
- cubrid_lob2_tell
- cubrid_lob2_tell64
- cubrid_lob2_seek
- cubrid_lob2_seek64
- cubrid_lob2_size
- cubrid_lob2_size64
- cubrid_lob2_close
Changed and Enhanced Features:
1) APIS-179: Remove the support of named placeholders for prepare statements
2) APIS-172: Remove the possibilities of the value of affected rows may not correct
3) APIS-171: Unify the request resource registered in cubrid_execute, cubrid_query and cubrid_unbuffered_query
Though the implements of cubrid_execute, cubrid_query and cubrid_unbuffered_query are different,
there are also some problems that these three functions all need to consider, such as when should the 
request resource be registered. We should register the request resource when the related objects are ready.
Fixed bugs:
1) APIS-176: Resolve the memory growth when continually execute SQL statements on one connection and don't close request.

* Wed Mar 23 2012 CUBRID Developers<contact@cubrid.org> - 8.4.1.0003-1
- APIS-52: Simplify the code of cubrid_client_encoding and cubrid_get_charset
- APIS-72: Unify the return value of some functions when they fail
- APIS-97: In PHP calling is_resource() function when = cubrid resource, always returns "Unknown"
- APIS-100: PHPinfo() displays DB engine, CCI(libcas) and PHP driver's version info
- APIS-103: Error: CCI, -13, Column index is out of range when calling cubrid_fetch_field()
- APIS-105: cubrid_field_type() returns "varchar(100)" instead of "varchar"
- APIS-106: cubrid_affected_rows() requires a different parameter than mysql_affected_rows()
- APIS-107: cubrid_fetch_field() return default value as empty string instead of NULL
- APIS-108: The resource parameter in cubrid_disconnect should be optional as in cubrid_close
- APIS-109: Make the return values of cubrid_move_cursor and cubrid_data_seek consistent with mysql_data_seek
- APIS-110: Modify return value of cubrid_num_fields
- APIS-111: cubrid_list_dbs() requires connection_id while in mysql_list_dbs() connection_id is optional
- APIS-117: cubrid_fetch_field will affect the cursor position which will influence the results of cubrid_fetch
- APIS-123: Return value of cubrid_fetch_lengths method is empty when record number is 1
- APIS-128: Passing field parameter in the form of tablename.fieldname to cubrid_result method will fail
- APIS-129: Getting value using cubrid_result method will fail when the column value in database is null
- APIS-132: Error message is empty when row number is out of range of cubrid_data_seek method
- APIS-135: Segment default will appear when calling cubrid_list_dbs() method
- APIS-147: Connect will success when passing a error passwd to cubrid_pconnect() method
- APIS-150: Return values are not good for cubrid_get_autocommit
