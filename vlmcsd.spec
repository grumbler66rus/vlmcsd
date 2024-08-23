Summary: vlmcsd - the KMS server
Name: vlmcsd
Version: 1113
Release: 0
License: GPL
Source: svn1113.tar.gz
URL: https://github.com/Wind4/vlmcsd/archive/refs/tags/svn1113.tar.gz
Provides: vlmcs
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: Other

%global debug_package %{nil}

%description
vlmcsd is the daemon for the KMS server (emulator of the Microsoft KMS server).
vlmcs is test program for the KMS server.

%prep
#mkdir ~/rpmbuild/SOURCES
#cd ~/rpmbuild/SOURCES; wget https://github.com/Wind4/vlmcsd/archive/refs/tags/svn1113.tar.gz
#git clone -b svn1113  https://github.com/Wind4/vlmcsd.git
%setup -q -n vlmcsd-svn1113

%build
make

%install
install -d %{buildroot}{/usr/sbin,/usr/bin,/etc,/usr/lib/systemd/system}
install -d %{buildroot}/usr/share/man/man{1,5,7,8}
install -m 0755 bin/vlmcsd %{buildroot}/usr/sbin/
install -m 0755 bin/vlmcs %{buildroot}/usr/bin/
install -m 0644 etc/vlmcsd.* %{buildroot}/etc/
install -m 0644 man/*1 %{buildroot}/usr/share/man/man1
install -m 0644 man/*5 %{buildroot}/usr/share/man/man5
install -m 0644 man/*7 %{buildroot}/usr/share/man/man7
install -m 0644 man/*8 %{buildroot}/usr/share/man/man8
cat <<SYSTEMDFILE > %{buildroot}/usr/lib/systemd/system/vlmcsd.service
[Unit]
Description=KMS server
After=network.target
[Service]
Type=simple
#User=nobody
ExecStart=/usr/sbin/vlmcsd -D -u nobody
[Install]
WantedBy=multi-user.target
SYSTEMDFILE

%post
systemctl daemon-reload

%preun
systemctl disable --now vlmcsd.service

%files
/etc/vlmcsd.*
/usr/bin/vlmcs*
/usr/sbin/vlmcs*
/usr/share/man/man?/vlm*
/usr/lib/systemd/system/vlmcsd.service
