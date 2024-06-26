%global livekit_ver 8645a138fb2ea72c4dab13e739b1f3c9ea29ac84

Name:           zed
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/zed-industries/zed/releases/latest | grep -oP '"tag_name": "v\K(.*)(?=")')
Release:        1
URL:            https://github.com/zed-industries/zed
Source0:        https://github.com/zed-industries/zed/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/livekit/protocol/archive/%{livekit_ver}/protocol-%{livekit_ver}.tar.gz
#Source0:        https://github.com/zed-industries/zed/archive/refs/heads/master.tar.gz
Summary:        Lightning-fast and Powerful Code Editor written in Rust
License:        AGPL-3.0-or-later
BuildRequires :  rustc
BuildRequires :  pkg-config
BuildRequires :  libxcb-dev
BuildRequires :  freetype-dev
BuildRequires :  fontconfig-dev
BuildRequires :  mesa-dev
BuildRequires :  libxkbcommon-dev
BuildRequires :  pango-dev
BuildRequires :  pkgconfig(wayland-client)
BuildRequires :  pkgconfig(wayland-cursor)
BuildRequires :  pkgconfig(wayland-protocols)
BuildRequires :  alsa-lib-dev
BuildRequires :  Vulkan-Headers-dev
BuildRequires :  openssl-dev
BuildRequires :  zstd-dev

%description
Code at the speed of thought - Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.


%prep
%setup -q -n zed-%{version} -a 1
# rm -rf crates/live_kit_server/protocol
# mv protocol-%%{livekit_ver} crates/live_kit_server/protocol


%build
unset https_proxy http_proxy
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx,+fma,+avx2 -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code  "
# --cfg gles    <= doesn't works, saved for the future
cargo build --release --package zed --package cli
strip target/release/Zed target/release/cli


%install
install -D -m755 target/release/Zed %{buildroot}/usr/bin/zed
install -D -m755 target/release/cli %{buildroot}/usr/bin/cli
# install -D -m0644 crates/zed/resources/*.desktop %%{buildroot}/usr/share/applications/zed.desktop
install -D -m0644 crates/zed/resources/app-icon.png %{buildroot}/usr/share/icons/hicolor/512x512/apps/zed.png


%files
%defattr(-,root,root,-)
/usr/bin/zed
/usr/bin/cli
#/usr/share/applications/*.desktop
/usr/share/icons/hicolor/512x512/apps/zed.png
