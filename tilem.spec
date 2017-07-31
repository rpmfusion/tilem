Name:           tilem
Version:        2.0
Release:        4%{?dist}
Summary:        Emulator and debugger for Texas Instruments Z80-based graphing calculators

License:        GPLv3+
URL:            http://lpg.ticalc.org/prj_tilem/
Source0:        http://www.ticalc.org/pub/unix/tilem.tar.bz2

# Appdata files.
Source1:        tilem.appdata.xml

# Patch to add -lm to libs via autoconf.
Patch0:         tilem-ac-check-libm.patch

BuildRequires:  libticonv-devel, libticalcs2-devel, libticables2-devel, libtifiles2-devel
BuildRequires:  glib2-devel, gtk2-devel
BuildRequires:  autoconf
BuildRequires:  libappstream-glib, desktop-file-utils

Requires:       hicolor-icon-theme

Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

%description
TilEm is an emulator and debugger for Texas Instruments Z80-based
graphing calculators.  It can emulate any of the following calculator
models:

TI-73 / TI-73 Explorer
TI-76.fr
TI-81
TI-82
TI-82 STATS / TI-82 STATS.fr
TI-83
TI-83 Plus / TI-83 Plus Silver Edition / TI-83 Plus.fr
TI-84 Plus / TI-84 Plus Silver Edition / TI-84 pocket.fr
TI-85
TI-86

TilEm fully supports all known versions of the above calculators (as
of 2012), and attempts to reproduce the behavior of the original
calculator hardware as faithfully as possible.

In addition, TilEm can emulate the TI-Nspire's virtual TI-84 Plus
mode.  This is currently experimental, and some programs may not work
correctly.

%prep
%autosetup -p1

%build
autoconf
%configure
%make_build

%install
%make_install

# Rename desktop file and validate it.
mv %{buildroot}%{_datadir}/applications/tilem2.desktop %{buildroot}%{_datadir}/applications/tilem.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/tilem.desktop

# Install appdata file and validate it.
mkdir %{buildroot}%{_datadir}/appdata/
cp -p %SOURCE1 %{buildroot}/%{_datadir}/appdata/
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%if 0%{?fedora} <= 24
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%if 0%{?fedora} <= 24
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%{_bindir}/tilem2
%{_datadir}/tilem2
%{_datadir}/applications/tilem.desktop
%{_datadir}/icons/hicolor/*/apps/tilem.png
%{_datadir}/mime/packages/tilem2.xml
%{_datadir}/appdata/tilem.appdata.xml
%license COPYING
%doc README NEWS CHANGELOG THANKS TODO


%changelog
* Mon Mar 13 2017 Ben Rosser <rosser.bjr@gmail.com> - 2.0-4
- Change license tag to GPLv3+
- Add desktop-database scriplets for Fedora < 25.
- Add Requires on hicolor-icon-theme.
- Renamed tilem2 desktop file to tilem.desktop, and validated it in install section.

* Tue Mar 07 2017 Ben Rosser <rosser.bjr@gmail.com> - 2.0-3
- Add appdata file to package.

* Thu Oct 13 2016 Ben Rosser <rosser.bjr@gmail.com> - 2.0-2
- Add autoconf BuildRequire, as we patch config.ac and need to rerun it.

* Thu Oct 13 2016 Ben Rosser <rosser.bjr@gmail.com> - 2.0-1
- Initial package.