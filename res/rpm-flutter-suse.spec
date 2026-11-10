Name:       trdesk
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://trdesk.com
Vendor:     trdesk <info@trdesk.com>
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/trdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/trdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/rustdesk.service "%{buildroot}/usr/share/trdesk/files/trdesk.service"
install -Dm 644 $HBB/res/rustdesk.desktop "%{buildroot}/usr/share/trdesk/files/trdesk.desktop"
install -Dm 644 $HBB/res/rustdesk-link.desktop "%{buildroot}/usr/share/trdesk/files/trdesk-link.desktop"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/trdesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/trdesk.svg"

%files
/usr/share/trdesk/*
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
ln -sf /usr/share/trdesk/trdesk /usr/bin/trdesk
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
    rm /usr/bin/trdesk || true
    rmdir /usr/lib/trdesk || true
    rmdir /usr/local/trdesk || true
    rmdir /usr/share/trdesk || true
    rm /usr/share/applications/trdesk.desktop || true
    rm /usr/share/applications/trdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/trdesk || true
    rmdir /usr/local/trdesk || true
  ;;
esac
