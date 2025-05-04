pkgname = "base-nbuild"
pkgver = "0.1"
pkgrel = 1
build_style = "meta"
pkgdesc = "Core package set for nbuild containers"
license = "custom:meta"
url = "https://neve-linux.fmpt.org"

# musl must be built first to provide shlibs for later packages during stage 0
depends = [
    "musl-devel",
    "llvm",
    "clang",
    "lld",
    "ncurses",
    "neveutils-extra",
    "apk-tools",
    "gmake",
    "libarchive-progs",
    "fakeroot-core",
    self.with_pkgver("base-nbuild-progs"),
]
# bootstrap-llvm is temporary until next llvm release, don't feel like rebuild
provides = [
    "bootstrap:nbuild=9999-r0",
    "bootstrap:llvm=9999-r0",
]
replaces = ["apk-tools"]
replaces_priority = 100

options = ["bootstrap", "brokenlinks"]

if self.stage > 0:
    depends += [
        "apk-tools-static-bin",
        "bc-gh",
        "resolvconf",
        "resolvconf-none",
        "tzdb",
    ]

if self.stage > 2:
    depends += ["ccache"]


def build(self):
    from nbuild.util import compiler

    self.cp(self.files_path / "nbuild-cross-cc.c", ".")
    self.cp(self.files_path / "nbuild-lld-wrapper.c", ".")

    cc = compiler.C(self)
    cc.invoke(["nbuild-cross-cc.c"], "nbuild-cross-cc")
    cc.invoke(["nbuild-lld-wrapper.c"], "nbuild-lld-wrapper")


def install(self):
    self.install_bin("nbuild-cross-cc")
    self.install_bin("nbuild-lld-wrapper")

    # replace regular ld and ld.lld symlinks
    self.install_link("usr/bin/ld.lld", "nbuild-lld-wrapper")
    self.install_link("usr/bin/ld64.lld", "nbuild-lld-wrapper")

    # different default apk config
    self.install_file(self.files_path / "config", "usr/lib/apk")


@subpackage("base-nbuild-progs")
def _(self):
    # make sure to use our wrapper symlinks
    self.replaces = ["lld"]
    self.replaces_priority = 100
    self.options = ["!scancmd"]

    return self.default_progs()
