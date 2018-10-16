# globals for mpv
%global mpv_commit  ca73b609f6e15885f648b58f4de539105439bff6
%global mpv_short   %(c=%{mpv_commit}; echo ${c:0:7})
%global gver        .git%{mpv_short}

# globals for mpv-build
%global bld_commit  7608d209c3c32c8192feeee51b67c22547a1eb35
%global bld_short   %(c=%{bld_commit}; echo ${c:0:7})

# globals for ffmpeg
%global ffpg_commit 0a155c57bd8eb92ccaf7f5857dc6ab276d235846
%global ffpg_short   %(c=%{ffpg_commit}; echo ${c:0:7})

# globals for waf (required for mpv)
%global waf_release 2.0.9

# globals for libass
%global libass_release 0.14.0

%bcond_with system_libass

Name:       mpv
Version:    0.29.0
Release:    2%{?gver}%{dist}
Summary:    Movie player playing most video formats and DVDs
License:    GPLv2+
URL:        http://%{name}.io
Source0:    https://github.com/mpv-player/mpv-build/archive/%{bld_commit}.tar.gz#/mpv-build-%{bld_short}.tar.gz
Source1:    https://github.com/mpv-player/mpv/archive/%{mpv_commit}.tar.gz#/%{name}-%{mpv_short}.tar.gz
Source2:    https://github.com/FFmpeg/FFmpeg/archive/%{ffpg_commit}.tar.gz#/ffmpeg-%{ffpg_short}.tar.gz
Source3:    https://waf.io/waf-%{waf_release}
Source4:    https://github.com/libass/libass/releases/download/%{libass_release}/libass-%{libass_release}.tar.gz
Source5:    mpv-rpi.desktop
Patch:      use_tarball.patch
Patch1:     libass_fix.patch
Patch2:     python_fix.patch
ExclusiveArch: armv7hl

BuildRequires:  pkgconfig(alsa)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(enca)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libquvi-0.9)
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet) >= 0.0.5
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python-docutils
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Encode)

### libass
%if %{with system_libass}
BuildRequires:	enca-devel
BuildRequires:	fontconfig-devel
BuildRequires:	fribidi-devel
BuildRequires:	harfbuzz-devel
BuildRequires:	libpng-devel
BuildRequires:	automake >= 1.16.1
BuildRequires:	autoconf
%endif

### ffmpeg
BuildRequires:  xvidcore-devel
BuildRequires:  x264-devel
BuildRequires:  lame-devel
BuildRequires:  twolame-devel
BuildRequires:  yasm
BuildRequires:  ladspa-devel
BuildRequires:  libbs2b-devel
BuildRequires:  game-music-emu-devel
BuildRequires:  soxr-devel
BuildRequires:  libssh-devel
BuildRequires:  libvpx-devel
BuildRequires:  libvorbis-devel
BuildRequires:  opus-devel
BuildRequires:  libtheora-devel
BuildRequires:  freetype-devel
BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  python3-devel

### RPi mmal / omx support
BuildRequires:  raspberrypi-vc-libs-devel
BuildRequires:  raspberrypi-vc-libs
BuildRequires:  raspberrypi-vc-static
BuildRequires:  libomxil-bellagio-devel

Requires:   hicolor-icon-theme
Requires:   mpv-libs = %{version}-%{release}
Provides:   mplayer-backend
Provides:   mpv = %{version}-%{release}

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.


%package libs
Summary: Dynamic library for Mpv frontends
Provides: %{name}-libs = %{version}-%{release}
Provides: libmpv = %{version}-%{release}

%description libs
This package contains the dynamic library libmpv, which provides access to Mpv.


%package libs-devel
Summary: Development package for libmpv
Provides: %{name}-devel = %{version}-%{release}
Requires: mpv = %{version}-%{release}
Provides: libmpv-devel = %{version}-%{release}
Provides: %{name}-libs-devel = %{version}-%{release}

%description libs-devel
Libmpv development header files and libraries.


%prep
%setup -n mpv-build-%{bld_commit} -a1 -a2 -a4
%patch -p1
%patch1 -p1

mv -f %{name}-%{mpv_commit} %{name}
mv -f FFmpeg-%{ffpg_commit} ffmpeg
cp -f %{name}/LICENSE.GPL %{name}/Copyright $PWD/
%patch2 -p1

### Sorry we need avoid to compile some packages
%if %{with system_libass}
mv -f libass-0.14.0 libass
sed -i 's|1.15|1.16|g' libass/aclocal.m4
sed -i 's|1.15|1.16|g' libass/configure
%else
sed -i 's|scripts/libass-config|#scripts/libass-config|g' build
sed -i 's|scripts/libass-build|#scripts/libass-build|g' build
%endif

cp -f %{SOURCE3} %{name}/waf
chmod a+x %{name}/waf
sed -i 's|/usr/bin/env python|/usr/bin/python3|g' %{name}/waf


%build
### Set ffmpeg/libass/mpv flags
  _ffmpeg_options=(
    '--disable-programs'
    '--enable-ladspa'
    '--enable-libbs2b'
    '--enable-libgme'
    '--enable-libsoxr'
    '--enable-libssh'
    '--enable-libx264'
    '--enable-libxvid'
    '--enable-libmp3lame'
    '--enable-libtwolame'
    '--enable-libass'
    '--enable-libvpx'
    '--enable-libvorbis'
    '--enable-libopus'
    '--enable-libtheora'
    '--enable-libfreetype'
    '--enable-libv4l2'
    '--enable-openssl'
    '--enable-gpl'
    '--enable-nonfree'
    '--disable-runtime-cpudetect'
    '--arch=arm'
    '--cpu=armv7-a'
    '--enable-vfpv3'
    '--enable-thumb'
    '--enable-mmal'
    '--enable-omx'
    '--enable-omx-rpi'
    '--enable-neon'
    )

_mpv_options=(
    '--prefix=%{_prefix}'
    '--bindir=%{_bindir}'
    '--libdir=%{_libdir}'
    '--mandir=%{_mandir}'
    '--docdir=%{_docdir}/%{name}'
    '--confdir=%{_sysconfdir}/%{name}'
    '--disable-build-date'
    '--enable-libmpv-shared'
    '--enable-cdda'
    '--enable-dvb'
    '--enable-libarchive'
    '--enable-zsh-comp'
    '--disable-lgpl'
    '--enable-rpi'
)

echo ${_ffmpeg_options[@]} > ffmpeg_options
echo ${_mpv_options[@]} > mpv_options

export LIBRARY_PATH=/usr/lib/vc
export PKG_CONFIG_PATH=/usr/lib/vc/pkgconfig
export CPATH=/usr/include/vc/include

./rebuild -j4


%install
echo '#!/bin/sh
set -e

cd mpv
./waf install --destdir=%{buildroot}' > scripts/mpv-install
chmod a+x scripts/mpv-install

./install

pushd mpv
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}
popd


### desktop file modifications
# Launching mpv from the menu is useless on RPi as you don't get a usable window.
# As a compromise, force video output to X11, yes its SLOW but at least it works.
# h264 video is still partially accelerated (via h264_mmal) but gets ugly above 720p
# (or when resizing) due to slow x11 video output.
sed -i 's|mpv --player-operation-mode=pseudo-gui|mpv -vo=x11 --player-operation-mode=pseudo-gui|' \
%{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# Full RPi hardware acceleration is achieved via an overlay (ie no windows possible).
# In this case its best to force fullscreen playback and use a black background.
%{__install} -p %{SOURCE5} %{buildroot}/%{_datadir}/applications/
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-rpi.desktop


%post
/usr/bin/update-desktop-database &> /dev/null || :


%postun
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%license LICENSE.GPL Copyright
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf
%{_datadir}/zsh/site-functions/_mpv
%if 0%{?fedora} <= 28
%{_mandir}/man1/mpv.1.gz
%endif


%files libs
%license LICENSE.GPL Copyright
%{_libdir}/libmpv.so.*


%files libs-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc


%changelog
* Sat Aug 04 2018 Vaughan Agrez <devel at agrez dot net> 0.29.0-2.gitca73b60
- Modify default desktop file (use -vo=x11)
- Add 'full screen' desktop file (for full hardware acceleration)

* Fri Aug 03 2018 Vaughan Agrez <devel at agrez dot net> 0.29.0-1.gitca73b60
- Import into Fedberry (thanks UnitedRPMS)
- Refactor spec (armv7hl only build now)
- Update BuildRequires
- Update ffmpeg/mpv config flags to suit RPi hardware
- Disable pusleaudio

* Wed Jul 25 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.29.0-1.gitca73b60
- Updated to 0.29.0-1.gitca73b60

* Sun May 27 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.2-8.git7214f1f
- Automatic Mass Rebuild

* Wed May 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.2-7.git7214f1f
- Enabled Vulkan
- Libass bundled for F29/rawhide

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.2-6.git7214f1f
- Automatic Mass Rebuild

* Thu Apr 19 2018 Ivan Mironov <mironov DOT ivan AT gmail DOT com> 0.28.2-5.git7214f1f
- Enable OpenSSL to fix support of https streams
- Add "waf" into the source tarball (fixes build without network)

* Mon Feb 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.2-4.git7214f1f
- Automatic Mass Rebuild

* Fri Feb 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.2-3.git7214f1f
- Updated to 0.28.2-3.git7214f1f

* Tue Feb 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.0-9.gitdfac83a
- Rebuilt with Wayland support thanks to zakora

* Mon Feb 05 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.0-8.gitdfac83a
- Rebuilt for libcdio

* Sat Jan 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.28.0-7.gitdfac83a
- Updated to 0.28.0-7.gitdfac83a

* Wed Nov 15 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.27.0-4.git60df015
- Rebuilt for libbluray
- Deleted epoch tags

* Sat Oct 21 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.27.0-3.git60df015
- Updated to current commit

* Wed Oct 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.27.0-2.gitd18f7bb
- Automatic Mass Rebuild

* Fri Sep 15 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.27.0-1.gitd18f7bb
- Updated to 0.27.0-1.gitd18f7bb

* Thu Aug 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.26.0-1.git4db82f0
- Updated to 0.26.0-1.git4db82f0

* Mon Jun 12 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-3.git4e66356
- Updated to 0.25.0-3.git4e66356

* Sun May 21 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-2
- Rebuilt

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.25.0-1
- Rebuilt for libbluray

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.24.0-1
- Updated to 0.24.0-1
