Name:           tilem
Version:        2.0
Release:        19%{?dist}
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
BuildRequires:  autoconf, gcc
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
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Mon Feb 07 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0-15
- rebuilt

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.0-8
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 01 2017 Ben Rosser <rosser.bjr@gmail.com> - 2.0-5
- Appdata file was incorrect; same screenshot listed twice.

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
