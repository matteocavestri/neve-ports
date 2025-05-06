pkgname = "curl"
pkgver = "8.13.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-optimize",
    "--enable-ares",
    "--enable-ipv6",
    "--enable-threaded-resolver",
    "--enable-websockets",
    "--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt",
    "--with-fish-functions-dir=/usr/share/fish/vendor_completions.d",
    "--with-libidn2",
    "--with-libpsl",
    "--with-libssh2",
    "--with-nghttp2",
    "--with-nghttp3",
    "--with-openssl-quic",
    "--with-ssl",
    "--with-zlib",
    "--with-zsh-functions-dir=/usr/share/zsh/site-functions/",
    "--with-zstd",
    "ac_cv_path_NROFF=/usr/bin/mandoc",
    "ac_cv_sizeof_off_t=8",
]
hostmakedepends = ["automake", "pkgconf", "perl", "mandoc", "slibtool"]
makedepends = [
    "c-ares-devel",
    "libidn2-devel",
    "libpsl-devel",
    "libssh2-devel",
    "nghttp2-devel",
    "nghttp3-devel",
    "openssl3-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
checkdepends = [
    "nghttp2-progs",
    # FIXME: probably caused by weird config shenanigans
    # "openssh",
    "python",
]
depends = ["ca-certificates"]
pkgdesc = "Command line tool for transferring data with URL syntax"
license = "MIT"
url = "https://curl.haxx.se"
source = f"{url}/download/curl-{pkgver}.tar.xz"
sha256 = "4a093979a3c2d02de2fbc00549a32771007f2e78032c6faa5ecd2f7a9e152025"
hardening = ["vis", "!cfi"]


def post_install(self):
    self.install_license("COPYING")

    # patch curl-config for cross
    if not self.profile().cross:
        return

    with open(self.destdir / "usr/bin/curl-config") as inf:
        with open(self.destdir / "usr/bin/curl-config.new", "w") as outf:
            for ln in inf:
                ln = ln.replace(f"-L{self.profile().sysroot / 'usr/lib'} ", "")
                ln = ln.replace(f"{self.profile().triplet}-", "")
                outf.write(ln)

    self.rename("usr/bin/curl-config.new", "curl-config")
    self.chmod(self.destdir / "usr/bin/curl-config", 0o755)


def init_check(self):
    # upstream recommends cpucores*7 as a good starting point
    self.make_check_env["TFLAGS"] = f"-j{self.make_jobs * 7}"


@subpackage("curl-libs")
def _(self):
    self.pkgdesc = "Multiprotocol file transfer library"
    # transitional
    self.provides = [self.with_pkgver("libcurl")]

    return self.default_libs()


@subpackage("curl-devel")
def _(self):
    self.depends += makedepends
    self.pkgdesc = "Multiprotocol file transfer library"
    # transitional
    self.provides = [self.with_pkgver("libcurl-devel")]

    return self.default_devel()
