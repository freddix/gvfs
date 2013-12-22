Summary:	Userspace virtual filesystem
Name:		gvfs
Version:	1.18.3
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gvfs/1.18/%{name}-%{version}.tar.xz
# Source0-md5:	3620baa478f1748bd32d2f47bcbe30d0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	dbus-devel
BuildRequires:	fuse-devel
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1:2.38.0
BuildRequires:	gnome-online-accounts-devel >= 3.10.0
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libarchive-devel
BuildRequires:	libbluray-devel
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	libgnome-keyring-devel >= 3.10.0
BuildRequires:	libgphoto2-devel
BuildRequires:	libmtp-devel
BuildRequires:	libsecret-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libsoup-gnome-devel >= 2.44.0
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	udev-glib-devel
BuildRequires:	udisks2-devel
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Requires:	udev
Requires:	udisks2
Suggests:	%{name}-backend-recent-files = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GVFS is a userspace virtual filesystem where mount runs as a separate
processes which you talk to via D-BUS. It contains a gio module that
seamlessly adds gvfs support to all applications using the gio API. It
also supports exposing the gvfs mounts to non-gio applications using
FUSE.

# depends on gtk+3
%package backend-recent-files
Summary:	Recent files backend
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description backend-recent-files
Recent files backend for use with GTK+ 3 applications.

%package archive
Summary:	libarchive support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description archive
libarchive support for gvfs.

%package cdio
Summary:	libcdio support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description cdio
libcdio support for gvfs.

%package dnssd
Summary:	dnssd support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi

%description dnssd
dnssd support for gvfs.

%package fuse
Summary:	FUSE support for gvfs
Group:		Libraries
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name} = %{version}-%{release}
Requires:	fuse

%description fuse
FUSE support for gvfs.

%package gnome-online-accounts
Summary:	GNOME Online Accounts support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-online-accounts

%description gnome-online-accounts
GNOME Online Accounts support for gvfs.

%package gphoto2
Summary:	libgphoto2 support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgphoto2-runtime

%description gphoto2
libgphoto2 support for gvfs.

%package mtp
Summary:	MTP support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libmtp-udev

%description mtp
MTP support for gvfs.

%package smb
Summary:	smb support for gvfs
Group:		Libraries
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name} = %{version}-%{release}

%description smb
smb support for gvfs.

%package libs
Summary:	gvfs libraries
Group:		Libraries

%description libs
gvfs libraries.

%package devel
Summary:	Header files for GVFS library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for GVFS library.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-hal			\
	--disable-gdu			\
	--disable-obexftp		\
	--disable-schemas-compile	\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*,gio/modules/*}.la
%{__rm} $RPM_BUILD_ROOT%{_datadir}/GConf/gsettings/*.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache
killall -q -USR1 gvfsd >/dev/null 2>&1 || :
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%postun
%update_gsettings_cache
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%post archive
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%post cdio
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%post dnssd
%update_gsettings_cache
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%postun dnssd
%update_gsettings_cache

%post fuse
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%post gnome-online-accounts
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%post gphoto2
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%post smb
%update_gsettings_cache
killall -q -USR1 gvfsd >/dev/null 2>&1 || :

%postun smb
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f gvfs.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gvfs-*
%attr(755,root,root) %{_libdir}/gio/modules/libgioremote-volume-monitor.so
%attr(755,root,root) %{_libdir}/gio/modules/libgvfsdbus.so

%attr(755,root,root) %{_libexecdir}/gvfs-udisks2-volume-monitor
%attr(755,root,root) %{_libexecdir}/gvfsd
%attr(755,root,root) %{_libexecdir}/gvfsd-afp
%attr(755,root,root) %{_libexecdir}/gvfsd-afp-browse
%attr(755,root,root) %{_libexecdir}/gvfsd-computer
%attr(755,root,root) %{_libexecdir}/gvfsd-dav
%attr(755,root,root) %{_libexecdir}/gvfsd-ftp
%attr(755,root,root) %{_libexecdir}/gvfsd-http
%attr(755,root,root) %{_libexecdir}/gvfsd-localtest
%attr(755,root,root) %{_libexecdir}/gvfsd-metadata
%attr(755,root,root) %{_libexecdir}/gvfsd-network
%attr(755,root,root) %{_libexecdir}/gvfsd-sftp
%attr(755,root,root) %{_libexecdir}/gvfsd-trash

%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%dir %{_datadir}/gvfs/remote-volume-monitors
%dir %{_libexecdir}

%{_datadir}/dbus-1/services/gvfs-daemon.service
%{_datadir}/dbus-1/services/gvfs-metadata.service
%{_datadir}/dbus-1/services/org.gtk.Private.UDisks2VolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/udisks2.monitor

%{_datadir}/gvfs/mounts/afp-browse.mount
%{_datadir}/gvfs/mounts/afp.mount
%{_datadir}/gvfs/mounts/computer.mount
%{_datadir}/gvfs/mounts/dav+sd.mount
%{_datadir}/gvfs/mounts/dav.mount
%{_datadir}/gvfs/mounts/ftp.mount
%{_datadir}/gvfs/mounts/http.mount
%{_datadir}/gvfs/mounts/localtest.mount
%{_datadir}/gvfs/mounts/network.mount
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount

%{_datadir}/glib-2.0/schemas/org.gnome.system.gvfs.enums.xml

%{_prefix}/lib/tmpfiles.d/gvfsd-fuse-tmpfiles.conf

%{_mandir}/man1/gvfs-cat.1*
%{_mandir}/man1/gvfs-copy.1*
%{_mandir}/man1/gvfs-info.1*
%{_mandir}/man1/gvfs-ls.1*
%{_mandir}/man1/gvfs-mime.1*
%{_mandir}/man1/gvfs-mkdir.1*
%{_mandir}/man1/gvfs-monitor-dir.1*
%{_mandir}/man1/gvfs-monitor-file.1*
%{_mandir}/man1/gvfs-mount.1*
%{_mandir}/man1/gvfs-move.1*
%{_mandir}/man1/gvfs-open.1*
%{_mandir}/man1/gvfs-rename.1*
%{_mandir}/man1/gvfs-rm.1*
%{_mandir}/man1/gvfs-save.1*
%{_mandir}/man1/gvfs-set-attribute.1*
%{_mandir}/man1/gvfs-trash.1*
%{_mandir}/man1/gvfs-tree.1*
%{_mandir}/man1/gvfsd-metadata.1*
%{_mandir}/man1/gvfsd.1*
%{_mandir}/man7/gvfs.7*

%files backend-recent-files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-recent
%{_datadir}/gvfs/mounts/recent.mount

%files archive
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-archive
%{_datadir}/gvfs/mounts/archive.mount

%files cdio
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-burn
%attr(755,root,root) %{_libexecdir}/gvfsd-cdda
%{_datadir}/gvfs/mounts/burn.mount
%{_datadir}/gvfs/mounts/cdda.mount

%files dnssd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-dnssd
%{_datadir}/gvfs/mounts/dns-sd.mount
%{_datadir}/glib-2.0/schemas/org.gnome.system.dns_sd.gschema.xml

%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-fuse
%{_mandir}/man1/gvfsd-fuse.1*

%files gnome-online-accounts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfs-goa-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.Private.GoaVolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/goa.monitor

%files gphoto2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfs-gphoto2-volume-monitor
%attr(755,root,root) %{_libexecdir}/gvfsd-gphoto2
%{_datadir}/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor

%files mtp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfs-mtp-volume-monitor
%attr(755,root,root) %{_libexecdir}/gvfsd-mtp
%{_datadir}/dbus-1/services/org.gtk.Private.MTPVolumeMonitor.service
%{_datadir}/gvfs/mounts/mtp.mount
%{_datadir}/gvfs/remote-volume-monitors/mtp.monitor

%files smb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-smb
%attr(755,root,root) %{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount
%{_datadir}/glib-2.0/schemas/org.gnome.system.smb.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgvfs*.so.?
%attr(755,root,root) %{_libdir}/libgvfs*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgvfs*.so
%{_includedir}/gvfs-client

