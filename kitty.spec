%global librsync_version 2.3.2

Name     : kitty
Version  : 0.26.0
Release  : 1
URL      : https://github.com/kovidgoyal/kitty
Source0  : https://github.com/kovidgoyal/kitty/archive/v%{version}.tar.gz#/kitty-%{version}.tar.gz
Source1  : https://github.com/librsync/librsync/archive/v%{librsync_version}/librsync-%{librsync_version}.tar.gz 
Summary  : A GPU-based terminal emulator
Group    : Development/Tools
License  : GPLv3
BuildRequires : ImageMagick-dev
BuildRequires : mesa-dev
BuildRequires : fontconfig-dev
BuildRequires : freetype-dev
BuildRequires : harfbuzz-dev
BuildRequires : libXcursor-dev
BuildRequires : libXrandr-dev
BuildRequires : libcanberra-dev
BuildRequires : lcms2-dev
BuildRequires : libpng-dev
BuildRequires : xkbcomp-dev
BuildRequires : libXaw-dev
BuildRequires : wayland-dev
BuildRequires : wayland-protocols-dev
BuildRequires : ncurses-dev
BuildRequires : pkgconfig(x11)
BuildRequires : pkgconfig(xpm)
BuildRequires : pkgconfig(xt)
BuildRequires : cmake
BuildRequires : openssl-dev


%description
A terminal emulator that uses OpenGL for rendering.
Supports terminal features like: graphics, Unicode,
true-color, OpenType ligatures, mouse protocol, focus tracking,
bracketed paste and so on, and which can be controlled by scripts.


%prep
%setup -q -a 1
sed -i 's|run_tool(\[.*docs.*\])||' setup.py
sed -i 's|copy_man_pages(ddir)||g' setup.py
sed -i 's|copy_html_docs(ddir)||g' setup.py
# script-without-shebang '__init__.py'
find -type f -name "*.py*" -exec chmod -x "{}"  \;
 
%build
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1646932528
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=auto "
export FCFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=auto "
export FFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=auto "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=auto "
pushd librsync-%{librsync_version}
cmake . -Bbuilddir -DCMAKE_BUILD_TYPE=Release
cmake --build builddir && cmake --install ./builddir --prefix /usr
popd


%install
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1646932528
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=auto "
export FCFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=auto "
export FFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=auto "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=auto "
python3 setup.py --verbose linux-package --prefix %{buildroot}%{_prefix}
mkdir -p %{buildroot}/usr/lib64 && cp -pr /usr/lib64/librsync* %{buildroot}/usr/lib64



%files
%defattr(-,root,root,-)
/usr/bin/kitty
/usr/lib64/librsync*
/usr/lib/kitty
/usr/share/applications/kitty*.desktop
/usr/share/icons/hicolor
/usr/share/terminfo
