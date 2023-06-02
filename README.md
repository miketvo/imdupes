# Prototype: imdupes

Quickly detect and remove identical images.

<a style="align:center" href="https://github.com/miketvo/imdupes-prototype/releases/"><button>Download</button></a>

Syntax:

```text
usage: imdupes {detect,clean} [OPTIONS] DIRECTORY

Quickly detects and removes identical images. Has two modes:
	- 'detect' console prints the detected identical image paths/filenames
	- 'clean' removes the detected identical images, keeping only the first copy

positional arguments:
  {detect,clean}        run mode
  directory             target image directory

options:
  -h, --help            show this help message and exit
  -e REGEX, --exclude REGEX
                        exclude matched filenames based on REGEX pattern
  -r, --recursive       recursively search for images in subdirectories in
                        addition to the specified parent directory
  -V, --verbose         explain what is being done
  -f {absolute,prog-relative,dir-relative,filename}, --format {absolute,prog-relative,dir-relative,filename}
                        console output file path format, always applied to
                        detect mode and clean mode only when verbose is
                        enabled (default: dir-relative)
  -v, --version         show version information and exit

detect mode options:
  -o OUTPUT, --output OUTPUT
                        save the console output to the specified OUTPUT file
                        (overwriting if file already exist)

clean mode options:
  -i, --interactive     prompt before every file deletion and let the user
                        choose which file to delete

Note: This program ignores any non-image file in the target directory
```
