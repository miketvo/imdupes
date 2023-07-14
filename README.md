# Imdupes

Versatile image deduplicator.

---

## Download and Installation

### Install with [Scoop](https://scoop.sh/) (Windows)

```bash
scoop bucket add scoop-miketvo https://github.com/miketvo/scoop-miketvo
```

```bash
scoop install scoop-miketvo/imdupes
```

### Portable Binaries Downloads
See [Releases](https://github.com/miketvo/imdupes/releases/) for latest versions.

Download and extract the archive containing the `imdupes` executable for your operating system. Currently, these OSes are supported:

- Windows 7 or higher
- Any Linux Distro with Kernel version 5.15 or higher

## Syntax

```text
usage: imdupes {info,scan,clean} ...

Quickly detects and removes identical images. Has 3 modes:
        - 'info' collects and displays statistics and information of images in a directory
        - 'scan' scans and console prints detected identical image paths/filenames
        - 'clean' scans and removes detected identical images (keeping only the first copy by default)
See "imdupes {info,scan,clean} --help" for more information

options:
  -h, --help         show this help message and exit
  -v, --version      show version information and exit

run modes:
  {info,scan,clean}

Note: This program ignores any non-image file in the target directory
Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)
```

See below for detailed description of each mode and their arguments:

**Info Mode:**

```text
usage: imdupes info [options] directory

collect and display statistics and information of images in a directory

positional arguments:
  directory             target image directory

options:
  -h, --help            show this help message and exit
  -e REGEX, --exclude REGEX
                        exclude matched filenames based on REGEX pattern
  -r, --recursive       recursively search for images in subdirectories in addition to the specified parent directory
  -V {1,2}, --verbose {1,2}
                        explain what is being done
  -p {0,1,2}, --progress-bar {0,1,2}
                        specify verbose mode (-V/--verbose) progress bar detail level, 0 disables the progress bar
                        entirely (default: 2)
  -f {absolute,cwd-relative,target-dir-relative,filename}, --format {absolute,cwd-relative,target-dir-relative,filename}
                        console output file path format, (default: target-dir-relative)

Note: This program ignores any non-image file in the target directory
```

**Scan Mode:**

```text
usage: imdupes scan [options] directory [-o OUTPUT]

scan and console print detected identical image paths/filenames

positional arguments:
  directory             target image directory

options:
  -h, --help            show this help message and exit
  -m {color-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}, --hashing-method {color-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}
                        specify a hashing method (default: color-hist-hashing)
  -a {max-dim,max-dims-mean,avg-dim,avg-dims-mean}, --auto-hash-size {max-dim,max-dims-mean,avg-dim,avg-dims-mean}
                        automatic hash size calculation (default: max-dims-mean)
  -s HASH_SIZE, --hash-size HASH_SIZE
                        specify a preferred hash size (integer)*
  -e REGEX, --exclude REGEX
                        exclude matched filenames based on REGEX pattern
  -r, --recursive       recursively search for images in subdirectories in addition to the specified parent directory
  -V {1,2}, --verbose {1,2}
                        explain what is being done
  -p {0,1,2}, --progress-bar {0,1,2}
                        specify verbose mode (-V/--verbose) progress bar detail level, 0 disables the progress bar
                        entirely (default: 2)
  -H, --show-hash       show hash value of each duplication in output
  -f {absolute,cwd-relative,target-dir-relative,filename}, --format {absolute,cwd-relative,target-dir-relative,filename}
                        console output file path format, (default: target-dir-relative)
  -S, --silent          no console output, -o/--output must be specified
  -o DUPFILE, --output DUPFILE
                        save the output to the specified DUPFILE (JSON formatted .imdup) file (overwriting if file
                        already exist)

Note: This program ignores any non-image file in the target directory
*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for
   identifying identical images; The smaller the hash size, the better the performance; Smallest accepted hash size
   is 8
```

**Clean Mode:**

```text
usage: imdupes clean [options] input

scan and remove detected identical images (keeping only the first copy by default); deleted files are not
recoverable, proceed with caution

positional arguments:
  input                 a directory containing the target images to be processed and clean; or a valid JSON formatted
                        .imdup file containing duplicated image paths (can be generated using scan mode with
                        -o/--output
                         flag), in which case only the following flags are available:
                          -h/--help
                          -e/--exclude
                          -V/--verbose
                          -i/--interactive
                        see options below for more information

options:
  -h, --help            show this help message and exit
  -m {color-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}, --hashing-method {color-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}
                        specify a hashing method (default: color-hist-hashing)
  -a {max-dim,max-dims-mean,avg-dim,avg-dims-mean}, --auto-hash-size {max-dim,max-dims-mean,avg-dim,avg-dims-mean}
                        automatic hash size calculation (default: max-dims-mean)
  -s HASH_SIZE, --hash-size HASH_SIZE
                        specify a preferred hash size (integer)*
  -e REGEX, --exclude REGEX
                        exclude matched filenames based on REGEX pattern
  -r, --recursive       recursively search for images in subdirectories in addition to the specified parent directory
  -V {1,2}, --verbose {1,2}
                        explain what is being done
  -p {0,1,2}, --progress-bar {0,1,2}
                        specify verbose mode (-V/--verbose) progress bar detail level, 0 disables the progress bar
                        entirely (default: 2)
  -i, --interactive     prompt for every duplication and let the user choose which file to delete
  -f {absolute,cwd-relative,target-dir-relative,filename}, --format {absolute,cwd-relative,target-dir-relative,filename}
                        console output file path format, ignored if -V/--verbose and -i/--interactive are both not
                        enabled (default: target-dir-relative)

Note: This program ignores any non-image file in the target directory
*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for
   identifying identical images; The smaller the hash size, the better the performance; Smallest accepted hash size
   is 8
```

## Dupfiles

- Extension: `.imdup`
- Format: JSON
- Indent: 2 spaces

These files are JSON-formatted text file generated from running:

```bash
imdupes scan ... --output DUPFILE
````

They have the following format:

```json lines
[
  [
    "abspath/to/image/file",
    "abspath/to/image/file",
    "abspath/to/image/file",
    ...
  ],
  [
    "abspath/to/image/file",
    "abspath/to/image/file",
    "abspath/to/image/file",
    ...
  ],
  [
    "abspath/to/image/file",
    "abspath/to/image/file",
    "abspath/to/image/file",
    ...
  ],
  ...
]
```

They can then be further edited by the user for more fine control over which file is deleted, then loaded back into the `clean` mode for automated or interactive cleaning:

```bash
imdupes clean path/to/dupfile.imdup     # Automated cleaning
imdupes clean -i path/to/dupfile.imdup  # Interactive cleaning
```

When loaded into `clean` mode, all duplication will be sorted in order from the largest dimension to the smallest dimension, so that during automatic cleaning, only the largest file (1st copy) is kept, to ensure that the program preserve as much information as possible.

The user can also specify `-e/--exclude REGEX` flag when cleaning this way to further filtering.

## Supported Image File Formats

| File type                        | Extension                                                               | Note                                                                     |
|----------------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Blizzard Mipmap Format           | `.blp`                                                                  |                                                                          |
| Bitmap                           | `.bmp`, `.dib`                                                          |                                                                          |
| DirectDraw Surface               | `.dds`                                                                  |                                                                          |
| Encapsulated PostScript          | `.eps`                                                                  | User needs to have installed [Ghostscript](https://www.ghostscript.com/) |
| Graphics Interchange Format      | `.gif`                                                                  |                                                                          |
| Icon                             | `.ico`, `.icns`                                                         |                                                                          |
| Cursor                           | `.cur`                                                                  |                                                                          |
| LabEye Image Bitmap              | `.im`                                                                   |                                                                          |
| Joint Photographic Experts Group | `.jpg`, `.jpeg`, `.jpe`, `.jfif`, `.jif`                                |                                                                          |
| JPEG 2000                        | `.jp2`, `.j2k`, `.jpf`, `.jpm`, `.jpg2`, `.j2c`, `.jpc`, `.jpx`, `.mj2` |                                                                          |
| Picture Exchange                 | `.pcx`                                                                  |                                                                          |
| Portable Network Graphics        | `.png`                                                                  |                                                                          |
| Portable Bitmap                  | `.pbm`, `.pgm`, `.ppm`, `.pnm`                                          |                                                                          |
| Silicon Graphics Image           | `.sgi`                                                                  |                                                                          |
| SPIDER image                     | `.spi`                                                                  |                                                                          |
| Truevision TGA                   | `.tga`                                                                  |                                                                          |
| Tag Image File Format            | `.tif`, `.tiff`                                                         |                                                                          |
| WebP                             | `.webp`                                                                 |                                                                          |
| Flexible Image Transport System  | `.fits`, `.fit`, `.fts`                                                 |                                                                          |
| Pixar Image File Format          | `.pxr`                                                                  |                                                                          |
| Adobe Photoshop Document         | `.psd`                                                                  |                                                                          |
| Sun Raster                       | `.ras`, `.sun`                                                          |                                                                          |
| X Bitmap                         | `.xbm`                                                                  |                                                                          |
| X Pixmap                         | `.xpm`                                                                  |                                                                          |
