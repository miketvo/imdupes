# Prototype: imdupes

Quickly detect and remove identical images.

---

## Download
See [Releases](https://github.com/miketvo/imdupes-prototype/releases/) for latest versions.

## Syntax

```text
usage: imdupes {scan,clean} ...

Quickly detects and removes identical images. Has two modes:
        - 'scan' scans and console prints detected identical image paths/filenames
        - 'clean' scans and removes detected identical images, keeping only the first copy
See "imdupes scan --help" and "imdupes clean --help" for more information

options:
  -h, --help     show this help message and exit
  -v, --version  show version information and exit

run modes:
  {scan,clean}

Note: This program ignores any non-image file in the target directory
Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)
```
