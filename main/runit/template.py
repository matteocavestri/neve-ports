pkgname = "runit"
pkgver = "2.2.0"
pkgrel = 1
build_style = "gnu-makefile"
configure_args = []
hostmakedepends = [
    "make",
    "pkg-config",
]
makedepends = []
depends = []
pkgdesc = "UNIX init scheme with service supervision"
license = "BSD-3-Clause"
url = "https://smarden.org/runit/"
source = [
    f"https://smarden.org/runit/runit-{pkgver}.tar.gz",
]
sha256 = [
    "95ef4d2868b978c7179fe47901e5c578e11cf273d292bd6208bd3a7ccb029290",
]
options = ["!check", "static"]


def install(self):
    # Extraction and setup
    self.unpack(f"runit-{pkgver}.tar.gz")
    self.mv(f"runit-{pkgver}/*", self.destdir)

    # Install default services
    self.install_dir("var")
    self.install_link("var/service", "run/runit/runsvdir/current")

    # Install binaries
    for f in [
        "chpst",
        "runit",
        "runit-init",
        "runsv",
        "runsvchdir",
        "runsvdir",
        "sv",
        "svlogd",
        "utmpset",
    ]:
        self.install_bin(f"src/{f}")

    # Install man pages
    for f in self.files_path.glob("man/*"):
        self.install_man(f)

    # Install bash-completion
    self.install_file(
        self.files_path / "sv", "usr/share/bash-completion/completions/sv"
    )

    # Install license
    self.install_file(
        self.files_path / "COPYING", "usr/share/licenses/runit/LICENSE"
    )

    # Ensure the proper file permissions for directories and files
    (self.destdir / "var/service").chmod(0o755)
    (self.destdir / "usr/bin").chmod(0o755)


@subpackage("runit-devel")
def _(self):
    self.subdesc = "Development files for runit"
    self.depends = []

    return [
        "usr/include/runit",
        "usr/lib/librunit*.so",
    ]


@subpackage("runit-doc")
def _(self):
    self.subdesc = "Documentation for runit"
    self.depends = []

    return [
        "usr/share/man/man*",
        "usr/share/doc/runit",
    ]
