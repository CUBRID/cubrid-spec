# CUBRID spec files for Linux

This repository includes CUBRID spec files to build CUBRID, CUBRID PHP and Python drivers on Linux systems.

## Spec versions

There are different spec files for each version of CUBRID. The **master** branch of this repository is always for the latest version of CUBRID. The spec file for previous versions of CUBRID can be found in their respective branches. To see the full list of branches visit [https://github.com/CUBRID/cubrid-spec/branches](https://github.com/CUBRID/cubrid-spec/branches).

## How to build CUBRID using a spec file

### Download CUBRID source code

Download the source code archive which will be necessary in the next step in order to build the source RPM package. Choose from one of the following versions.

- [cubrid-9.1.0.0212.1.tar.gz](http://sourceforge.net/projects/cubrid/files/CUBRID-9.1.0/Linux/Fedora-RPM/cubrid-9.1.0.0212.1.tar.gz/download)
- [cubrid-8.4.3.0150.1.tar.gz](http://sourceforge.net/projects/cubrid/files/CUBRID-8.4.3/Linux/Fedora-RPM/cubrid-8.4.3.0150.1.tar.gz/download)
- [cubrid-8.4.1.2032.3.tar.gz](http://sourceforge.net/projects/cubrid/files/CUBRID-8.4.1/Linux/Fedora-RPM/cubrid-8.4.1.2032.3.tar.gz/download)

Once you download the archive, move it to `~/rpmbuild/SOURCE/` directory. This is where the `rpmbuild` tool will read the source archive from.

### Create source RPM file

The next step is to create an SRPM package out of the source archive using the rules defined in the **cubrid.spec** file.

	rpmbuild -bs cubrid.spec

The above command will create an SRPM package file and save it to `~/rpmbuild/SRPMS/cubrid-9.1.0.0212-1.fc19.src.rpm`. The name of the file may change based on the version of CUBRID you choose to build as well as the operating system.

At this point we have everything ready to start building our package.

### Find the Mock configuration file

Before sending the build job to Fedora Koji, it is best to try building on your local machine using `mock`. Mock can build the package on various types of hardware. In fact Koji uses Mock.

First, we should find a suitable Mock configuration file for our current system which is **Fedora 19 x86_64**.

	ls -l /etc/mock/fedora-19-*

The above command will list configuration files for Fedora 19. You will see the output similar to the following:

	$ ls -l /etc/mock/fedora-19-*
	-rw-r--r--. 1 root mock 1551 Apr 19 04:09 /etc/mock/fedora-19-arm.cfg
	-rw-r--r--. 1 root mock 1552 Apr 19 04:09 /etc/mock/fedora-19-armhfp.cfg
	-rw-r--r--. 1 root mock 1562 Apr 19 04:09 /etc/mock/fedora-19-i386.cfg
	-rw-r--r--. 1 root mock 1547 Apr 19 04:09 /etc/mock/fedora-19-ppc64.cfg
	-rw-r--r--. 1 root mock 1653 Apr 19 04:09 /etc/mock/fedora-19-ppc.cfg
	-rw-r--r--. 1 root mock 1546 Apr 19 04:09 /etc/mock/fedora-19-s390.cfg
	-rw-r--r--. 1 root mock 1548 Apr 19 04:09 /etc/mock/fedora-19-s390x.cfg
	-rw-r--r--. 1 root mock 1557 Apr 19 04:09 /etc/mock/fedora-19-x86_64.cfg

We need to jot down the name of the configuration file we will use further on. It is **fedora-19-x86_64**.

### Start the local build process

Now we are ready to build locally.

	cd ~/rpmbuild/SRPMS/
	mock -r fedora-19-x86_64 cubrid-9.1.0.0212-1.fc19.src.rpm

It should output something similar to:

	$ mock -r fedora-19-x86_64 cubrid-9.1.0.0212-1.fc19.src.rpm 
	INFO: mock.py version 1.1.32 starting...
	Start: init plugins
	INFO: selinux enabled
	Finish: init plugins
	Start: run
	INFO: Start(cubrid-9.1.0.0212-1.fc19.src.rpm)  Config(fedora-19-x86_64)
	Start: lock buildroot
	Start: clean chroot
	INFO: chroot (/var/lib/mock/fedora-19-x86_64) unlocked and deleted
	Finish: clean chroot
	Finish: lock buildroot
	Start: chroot init
	Start: lock buildroot
	Mock Version: 1.1.32
	INFO: Mock Version: 1.1.32
	INFO: calling preinit hooks
	INFO: enabled root cache
	Start: unpacking root cache
	Finish: unpacking root cache
	INFO: enabled yum cache
	Start: cleaning yum metadata
	Finish: cleaning yum metadata
	INFO: enabled ccache
	Start: device setup
	Finish: device setup
	Start: yum update
	Start: Outputting list of available packages
	Finish: Outputting list of available packages
	Finish: yum update
	Finish: lock buildroot
	Finish: chroot init
	INFO: Installed packages:
	Start: build phase for cubrid-9.1.0.0212-1.fc19.src.rpm
	Start: device setup
	Finish: device setup
	Start: build setup for cubrid-9.1.0.0212-1.fc19.src.rpm
	Finish: build setup for cubrid-9.1.0.0212-1.fc19.src.rpm
	Start: rpmbuild -bb cubrid-9.1.0.0212-1.fc19.src.rpm
	Start: Outputting list of installed packages
	Finish: Outputting list of installed packages
	Finish: rpmbuild -bb cubrid-9.1.0.0212-1.fc19.src.rpm
	Finish: build phase for cubrid-9.1.0.0212-1.fc19.src.rpm
	INFO: Done(cubrid-9.1.0.0212-1.fc19.src.rpm) Config(fedora-19-x86_64) 5 minutes 4 seconds
	INFO: Results and/or logs in: /var/lib/mock/fedora-19-x86_64/result
	Finish: run

### Send the build job to Koji

Now, after the local build is successful, we can send the build job to Koji. To tell Koji to build against the Fedora 19 repository, execute the following command.

	koji build --scratch f19 ~/rpmbuild/SRPMS/cubrid-9.1.0.0212-1.f19.src.rpm

Alternatively, we can try to build the same SRPM file against the latest Fedora repository which is **rawhide**:

	koji build --scratch rawhide ~/rpmbuild/SRPMS/cubrid-9.1.0.0212-1.f19.src.rpm

The list of repositories which CUBRID is successfully build against is:

- Fedora 20: **rawhide**
- Fedora 19: **f19**
- Fedora 18: **f18**

The output of the above command will be similar to the following:

	$ koji build --scratch f19 cubrid-9.1.0.0212-1.fc19.src.rpm
	Uploading srpm: cubrid-9.1.0.0212-1.fc19.src.rpm
	[====================================] 100% 00:04:58  47.97 MiB 164.52 KiB/sec
	Created task: 5788595
	Task info: http://koji.fedoraproject.org/koji/taskinfo?taskID=5788595
	Watching tasks (this may be safely interrupted)...
	5788595 build (f19, cubrid-9.1.0.0212-1.fc19.src.rpm): open (buildvm-07.phx2.fedoraproject.org)
	  5788597 buildArch (cubrid-9.1.0.0212-1.fc19.src.rpm, i686): open (buildvm-17.phx2.fedoraproject.org)
	  5788596 buildArch (cubrid-9.1.0.0212-1.fc19.src.rpm, x86_64): open (buildvm-18.phx2.fedoraproject.org)
	  5788597 buildArch (cubrid-9.1.0.0212-1.fc19.src.rpm, i686): open (buildvm-17.phx2.fedoraproject.org) -> closed
	  0 free  2 open  1 done  0 failed
	  5788596 buildArch (cubrid-9.1.0.0212-1.fc19.src.rpm, x86_64): open (buildvm-18.phx2.fedoraproject.org) -> closed
	  0 free  1 open  2 done  0 failed
	5788595 build (f19, cubrid-9.1.0.0212-1.fc19.src.rpm): open (buildvm-07.phx2.fedoraproject.org) -> closed
	  0 free  0 open  3 done  0 failed

	5788595 build (f19, cubrid-9.1.0.0212-1.fc19.src.rpm) completed successfully