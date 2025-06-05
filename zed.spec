Name:           zed
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/zed-industries/zed/releases/latest | grep -oP '"tag_name": "v\K(.*)(?=")')
Release:        1
URL:            https://github.com/zed-industries/zed
#Source0:        https://github.com/zed-industries/zed/archive/refs/tags/v%%{version}.tar.gz
Source0:        https://github.com/huacnlee/zed/archive/97ec9c5e108b957df7c1918f1f4ba7d2b5281b4f.tar.gz
Summary:        Lightning-fast and Powerful Code Editor written in Rust
License:        AGPL-3.0-or-later
BuildRequires :  rustc llvm cmake
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
BuildRequires :  pkgconfig(libcurl)
BuildRequires :  pkgconfig(libgit2)
BuildRequires :  pkgconfig(sqlite3)
BuildRequires :  protobuf-dev
BuildRequires :  perl-local-lib perl-Module-Find perl-IPC-Run perl-File-Copy-Recursive 


%description
Code at the speed of thought - Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.


%prep
export DO_STARTUP_NOTIFY="true"
export APP_ICON="zed"
export APP_NAME="Zed"
export APP_CLI="zed"
export APP_ID="dev.zed.Zed"
export APP_ARGS="%U"
#%%setup -q -n zed-%%{version}
%setup -q -n zed-97ec9c5e108b957df7c1918f1f4ba7d2b5281b4f
envsubst < crates/zed/resources/zed.desktop.in > crates/zed/resources/zed.desktop




%build
unset https_proxy http_proxy
export RELEASE_VERSION=%{version}
export ZED_UPDATE_EXPLANATION="Please use the swupd or cf-zed-updater to update zed."
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx,+fma,+avx2 -C opt-level=3 -C codegen-units=1 -C panic=abort -C link-args=-Wl,--disable-new-dtags,-rpath,\$ORIGIN/../lib  "
# --cfg gles    <= doesn't works, saved for the future
export PROTOC=/usr/bin/protoc
export PROTOC_INCLUDE=/usr/include
cargo build --release --package zed --package cli
strip target/release/zed target/release/cli


%install
install -D -m0755 target/release/cli %{buildroot}/usr/bin/zed
install -D -m0755 target/release/zed %{buildroot}/usr/libexec/zed-editor
install -D -m0644 crates/zed/resources/zed.desktop %{buildroot}/usr/share/applications/zed.desktop
install -D -m0644 assets/icons/logo_96.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/zed.svg


%files
%defattr(-,root,root,-)
/usr/bin/zed
/usr/libexec/zed-editor
/usr/share/applications/zed.desktop
/usr/share/icons/hicolor/scalable/apps/zed.svg
