Name:       trdesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/trdesk/
mkdir -p %{buildroot}/usr/share/trdesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/trdesk %{buildroot}/usr/bin/trdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/trdesk/libsciter-gtk.so
install $HBB/res/rustdesk.service %{buildroot}/usr/share/trdesk/files/trdesk.service
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/trdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/trdesk.svg
install $HBB/res/rustdesk.desktop %{buildroot}/usr/share/trdesk/files/trdesk.desktop
install $HBB/res/rustdesk-link.desktop %{buildroot}/usr/share/trdesk/files/trdesk-link.desktop

%files
/usr/bin/trdesk
/usr/share/trdesk/libsciter-gtk.so
/usr/share/trdesk/files/trdesk.service
/usr/share/icons/hicolor/256x256/apps/trdesk.png
/usr/share/icons/hicolor/scalable/apps/trdesk.svg
/usr/share/trdesk/files/trdesk.desktop
/usr/share/trdesk/files/trdesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop trdesk || true
  ;;
esac

%post
cp /usr/share/trdesk/files/trdesk.service /etc/systemd/system/trdesk.service
cp /usr/share/trdesk/files/trdesk.desktop /usr/share/applications/
cp /usr/share/trdesk/files/trdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable trdesk
systemctl start trdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop trdesk || true
    systemctl disable trdesk || true
    rm /etc/systemd/system/trdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/trdesk.desktop || true
    rm /usr/share/applications/trdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
