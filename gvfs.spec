Summary:	Userspace virtual filesystem
Name:		gvfs
Version:	1.14.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gvfs/1.14/%{name}-%{version}.tar.xz
# Source0-md5:	43e7af7132c2425289321c2156655d1f
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	dbus-devel
BuildRequires:	fuse-devel
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libarchive-devel
BuildRequires:	libbluray-devel
BuildRequires:	libcdio-devel
BuildRequires:	libcdio-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libsecret-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libsoup-gnome-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	udev-glib-devel
BuildRequires:	udisks2-devel
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Requires:	udev
Requires:	udisks2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GVFS is a userspace virtual filesystem where mount runs as a separate
processes which you talk to via D-BUS. It contains a gio module that
seamlessly adds gvfs support to all applications using the gio API. It
also supports exposing the gvfs mounts to non-gio applications using
FUSE.

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

%package gphoto2
Summary:	libgphoto2 support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgphoto2-runtime

%description gphoto2
libgphoto2 support for gvfs.

%package obexftp
Summary:	obexftp support for gvfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	obex-data-server

%description obexftp
obexftp support for gvfs.

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
	--disable-schemas-compile	\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache
killall -q -USR1 gvfsd || :
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%postun
%update_gsettings_cache
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%post archive
killall -q -USR1 gvfsd || :

%post cdio
killall -q -USR1 gvfsd || :

%post dnssd
%update_gsettings_cache
killall -q -USR1 gvfsd || :

%postun dnssd
%update_gsettings_cache

%post fuse
killall -q -USR1 gvfsd || :

%post gphoto2
killall -q -USR1 gvfsd || :

%post obexftp
killall -q -USR1 gvfsd || :

%post smb
%update_gsettings_cache
killall -q -USR1 gvfsd || :

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
%attr(755,root,root) %{_libexecdir}/gvfsd-recent
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
%{_datadir}/gvfs/mounts/recent.mount
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount

%{_datadir}/glib-2.0/schemas/org.gnome.system.gvfs.enums.xml

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
%{_datadir}/GConf/gsettings/gvfs-dns-sd.convert
%{_datadir}/glib-2.0/schemas/org.gnome.system.dns_sd.gschema.xml

%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-fuse
%{_mandir}/man1/gvfsd-fuse.1*

%files gphoto2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfs-gphoto2-volume-monitor
%attr(755,root,root) %{_libexecdir}/gvfsd-gphoto2
%{_datadir}/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor

%files obexftp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-obexftp
%{_datadir}/gvfs/mounts/obexftp.mount

%files smb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gvfsd-smb
%attr(755,root,root) %{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount
%{_datadir}/GConf/gsettings/gvfs-smb.convert
%{_datadir}/glib-2.0/schemas/org.gnome.system.smb.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgvfs*.so.?
%attr(755,root,root) %{_libdir}/libgvfs*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgvfs*.so
%{_includedir}/gvfs-client

