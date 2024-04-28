Name:           zed
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/zed-industries/zed/releases/latest | grep -oP '"tag_name": "v\K(.*)(?=")')
Release:        1
URL:            https://github.com/zed-industries/zed
Source0:        https://github.com/zed-industries/zed/archive/refs/tags/v%{version}.tar.gz
#Source0:        https://github.com/zed-industries/zed/archive/refs/heads/master.tar.gz
Summary:        Lightning-fast and Powerful Code Editor written in Rust
License:        AGPL-3.0-or-later
BuildRequires:  rustc
BuildRequires:  pkg-config
BuildRequires:  libxcb-dev
BuildRequires:  freetype-dev
BuildRequires:  fontconfig-dev
BuildRequires:  mesa-dev
BuildRequires:  libxkbcommon-dev
BuildRequires:  pango-dev
BuildRequires:  wayland-dev wayland-protocols-dev
BuildRequires:  alsa-lib-dev
BuildRequires:  Vulkan-Headers-dev
BuildRequires:  openssl-dev
BuildRequires:  zstd-dev

%description
Code at the speed of thought - Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.


%prep
# lapce-%{version}
%setup -q -n zed-%{version}


%build
unset https_proxy http_proxy
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx,+fma,+avx2 -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code "
cargo build --release --frozen --all-features


%install
install -D -m755 target/release/Zed %{buildroot}/usr/bin/Zed
# install -D -m0644 extra/linux/*.desktop %%{buildroot}/usr/share/applications/*.desktop
# install -D -m0644 extra/images/logo.png %{buildroot}/usr/share/pixmaps/zed.png
strip  --strip-debug %{buildroot}/usr/bin/*

%files
%defattr(-,root,root,-)
/usr/bin/Zed
#/usr/share/applications/*.desktop
#/usr/share/pixmaps/*.png