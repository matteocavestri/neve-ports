pkgname = "neve-repo-main"
pkgver = "0.1"
pkgrel = 1
archs = [
    "aarch64",
    "loongarch64",
    "ppc64",
    "ppc64le",
    "riscv64",
    "x86_64",
]
build_style = "meta"
depends = ["apk-tools", "!base-nbuild"]
pkgdesc = "Neve base repository"
license = "custom:meta"
url = "https://neve-linux.fmpt.org"


def install(self):
    self.install_file(
        *self.find(
            self.files_path, f"{self.profile().arch}@neve-linux.fmpt.org-*.pub"
        ),
        "usr/lib/apk/keys",
    )
    self.install_file(
        self.files_path / "matteocavestri@fmpt.org.rsa.pub",
        "usr/lib/apk/keys",
    )
    self.install_file(
        self.files_path / "01-repo-main.list", "usr/lib/apk/repositories.d"
    )
    self.install_file(
        self.files_path / "02-repo-main-debug.list",
        "usr/lib/apk/repositories.d",
    )


@subpackage("neve-repo-main-debug")
def _(self):
    self.subdesc = "debug packages"
    self.depends = [self.parent]

    return ["usr/lib/apk/repositories.d/*-debug.list"]
