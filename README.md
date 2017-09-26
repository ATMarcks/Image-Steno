# Image-Steno

Image-Steno is an RGB image stenography program that hides plaintext ASCII information within an image's RGB channels' least significant bit(s). Each pixel in an image hides 4 bits of information; one bit each in two of the channels and two bits from one channel. The channel in which two bits are hidden is psuedorandomly selected using an optional user-supplied seed via a file or terminal input.

It is highly recommended that you use lossless image formats such as BMP and PNG. You may use other file formats and lossy formats—as long as they are supported by Pillow—but the program will prompt you first and your encoded data will likely be lost during file compression.

## Install

Image-Steno requires the Python `Pillow` or `PIL` library and Pyton 3.4 or above. If you do not have `PIL` or `Pillow` installed the application will prompt you to install library via pip but it is recommended to install outside of the program as the following before running:

`$ pip install Pillow`


## Usage

```
usage: ImageSteno.py [-h] [-e] [-d] -i INPUT_FILE -o OUTPUT_FILE
                     [-p PLAINTEXT_FILE] [-s SEED_FILE]

  -h, --help            show this help message and exit
  -e, --encode          Encode file
  -d, --decode          Decode file
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input file location/name; should be an image filetype
                        if you are encoding
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file location/name; should be an image filetype
                        if you are decoding
  -p PLAINTEXT_FILE, --plaintext-file PLAINTEXT_FILE
                        Plaintext file location/name to be inserted within image
  -s SEED_FILE, --seed-file SEED_FILE
                        Seed file location/name
```

## Examples

To encode an image without using a seed file:

`ImageSteno.py -e -i startingimage.png -o codedimage.png -p textfile.txt`

To decode an image without using a seed file:

`ImageSteno.py -d -i codedimage.png -o textfile.txt`

To encode an image using a seed file:

`ImageSteno.py -e -i startingimage.png -o codedimage.png -p textfile.txt -s seedfile`

To decode an image using a seed file:

`ImageSteno.py -d -i codedimage.png -o textfile.txt -s seedfile`

## Seeding

Only users who have the seed can decode the file given they cannot obtain the original image or could not reconstruct the original image from the encoded image (i.e. avoid images that predictable chunks of the same color). 

Example of a good image with varied, unpredictable colors throughout:

![A good image](https://github.com/ATMarcks/Files/blob/master/Image-Steno/badimage.png?raw=true)

Example of a bad image with large, predictable chunks of the same color:

![A bad image](https://github.com/ATMarcks/Files/blob/master/Image-Steno/badimage.png?raw=true)
