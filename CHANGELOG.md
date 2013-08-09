# CHANGELOG

## v9.1.0.0212.3

- Enabled debuginfo as suggested at
  https://bugzilla.redhat.com/show_bug.cgi?id=658754#c57. Had to
  modify CUBRID source code to make sure nginx httpd is built
  together with CUBRID Manager Server, not prebuilt.
- CUBRID is not supported on ARM architecture, so excluded it from builds.
- One more warning is "W: no-manual-page-for-binary". CUBRID does not
  have man pages, yet.
- One last warning message is
  "shared-lib-calls-exit /usr/lib64/libcubridesql.so.9.1.0 exit@GLIBC_2.2.5".
  We know about this and will make changes in the coming versions.

## v9.1.0.0212.2

- Enh: removed `systemd` as suggested by at [https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54](https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54).
- Enh: added `release` to version `Require` as suggested at [https://bugzilla.redhat.com/show_bug.cgi?id=658754#c55](https://bugzilla.redhat.com/show_bug.cgi?id=658754#c55).
- Enh: added code comments.
- Enh: for consistency, replaced `cubrid` user with `cubrid_user` as suggested at [https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54](https://bugzilla.redhat.com/show_bug.cgi?id=658754#c54).

## v9.1.0.0212.1

- New: added spec files for CUBRID 9.1.0, PHP and Python drivers.
