# Prototype: Imdupes

Versatile image deduplicator.

---

## Download
See [Releases](https://github.com/miketvo/imdupes-prototype/releases/) for latest versions.

## Syntax

```text
usage: imdupes {scan,clean} ...

Quickly detects and removes identical images. Has two modes:
        - 'scan' scans and console prints detected identical image paths/filenames
        - 'clean' scans and removes detected identical images (keeping only the first copy by default)
See "imdupes {scan,clean} --help" for more information

options:
  -h, --help     show this help message and exit
  -v, --version  show version information and exit

run modes:
  {scan,clean}

Note: This program ignores any non-image file in the target directory
Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)
```

See below for detailed description of each mode and their arguments:

**Scan Mode:**

```text
usage: imdupes scan [options] directory [-o OUTPUT]

scan and console print detected identical image paths/filenames

positional arguments:
  directory             target image directory

options:
  -h, --help            show this help message and exit
  -m {grayscale-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}, --hashing-method {grayscale-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}
                        specify a hashing method (default: grayscale-hist-hashing)
  -a {max-dim,max-adim,avg-dim,avg-adim}, --auto-hash-size {max-dim,max-adim,avg-dim,avg-adim}
                        automatic hash size calculation (default: max-adim)
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
  -f {absolute,prog-relative,dir-relative,filename}, --format {absolute,prog-relative,dir-relative,filename}
                        console output file path format, (default: dir-relative)
  -S, --silent          no console output, -o/--output must be specified
  -o DUPFILE, --output DUPFILE
                        save the output to the specified DUPFILE (JSON formatted .imdup) file (overwriting if file
                        already exist)

Note: This program ignores any non-image file in the target directory
*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for
   identifying identical images; The smaller the hash size, the better the performance; sSmallest accepted hash size
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
  -m {grayscale-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}, --hashing-method {grayscale-hist-hashing,grayscale-hashing,rgb-hashing,rgba-hashing}
                        specify a hashing method (default: grayscale-hist-hashing)
  -a {max-dim,max-adim,avg-dim,avg-adim}, --auto-hash-size {max-dim,max-adim,avg-dim,avg-adim}
                        automatic hash size calculation (default: max-adim)
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
  -f {absolute,prog-relative,dir-relative,filename}, --format {absolute,prog-relative,dir-relative,filename}
                        console output file path format, ignored if -V/--verbose and -i/--interactive are both not
                        enabled (default: dir-relative)

Note: This program ignores any non-image file in the target directory
*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for
   identifying identical images; The smaller the hash size, the better the performance; sSmallest accepted hash size
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
| Blizzard Texture Format          | `.blp`                                                                  |                                                                          |
| Bitmap                           | `.bmp`, `.dib`                                                          |                                                                          |
| DirectDraw Surface               | `.dds`                                                                  |                                                                          |
| Encapsulated PostScript          | `.eps`                                                                  | User needs to have installed [Ghostscript](https://www.ghostscript.com/) |
| Graphics Interchange Format      | `.gif`                                                                  |                                                                          |
| Apple Icon Image                 | `.icns`                                                                 |                                                                          |
| Icon                             | `.ico`                                                                  |                                                                          |
| IM Magica                        | `.im`                                                                   |                                                                          |
| Joint Photographic Experts Group | `.jpg`, `.jpeg`, `.jpe`, `.jfif`, `.jif`                                |                                                                          |
| JPEG 2000                        | `.jp2`, `.j2k`, `.jpf`, `.jpm`, `.jpg2`, `.j2c`, `.jpc`, `.jpx`, `.mj2` |                                                                          |
| PiCture eXchange                 | `.pcx`                                                                  |                                                                          |
| Portable Network Graphics        | `.png`                                                                  |                                                                          |
| Portable Bitmap                  | `.pbm`                                                                  |                                                                          |
| Portable Graymap                 | `.pgm`                                                                  |                                                                          |
| Portable Pixmap                  | `.ppm`                                                                  |                                                                          |
| Portable Anymap                  | `.pnm`                                                                  |                                                                          |
| Silicon Graphics Image           | `.sgi`                                                                  |                                                                          |
| Seattle FilmWorks                | `.spi`                                                                  |                                                                          |
| Truevision TGA                   | `.tga`                                                                  |                                                                          |
| Tagged Image File Format         | `.tif`, `.tiff`                                                         |                                                                          |
| WebP                             | `.webp`                                                                 |                                                                          |
| X11 Bitmap                       | `.xbm`                                                                  |                                                                          |
| Cursor                           | `.cur`                                                                  |                                                                          |
| Flexible Image Transport System  | `.fits`, `.fit`, `.fts`                                                 |                                                                          |
| Multi-Picture Object             | `.mpo`                                                                  |                                                                          |
| Pixar Image File Format          | `.pxr`                                                                  |                                                                          |
| Adobe Photoshop Document         | `.psd`                                                                  |                                                                          |
| Sun Raster                       | `.ras`, `.sun`                                                          |                                                                          |
| X11 Pixmap                       | `.xpm`                                                                  |                                                                          |
