# TODO Neve Ports

## Packages

- [ ] `system`
  - [ ] Migrate main to system
  - [ ] `base-nbuild`
    - [ ] 

- [ ] Make main repo
  - [ ] Porting main-nbuild
    - [x] llvm
    - [x] apk-tools
    - [x] neveutils (fork from chimerautils)
    - [x] musl
    - [x] ncurses
    - [x] gmake
    - [x] libarchive
    - [x] fakeroot
    - [x] bc-gh
    - [x] resolvconf
    - [x] tzdb
  - [ ] Porting main-nbuild-host
- [ ] Make base-system package
- [ ] Make base-system-zfs package
- [ ] Make base-system-minimal package
- [ ] Make base-container package

## Build system

- [x] Rewrite cbuild to nbuild

## Infrastructure

## Msc

- [x] Only use /lib (not wordsize dir)
- [ ] Delete libexec in favour of /lib
