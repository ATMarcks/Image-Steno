# Image-Steno

An RGB image stenography program that hides information within an image's RGB channels' least significant bit(s). Each pixel in an image hides 4 bits of information; one bit each in two of the channels and two bits from one channel. The channel in which two bits are hidden is psuedorandomly selected using an optional user-supplied seed. Adding RSA encryption and decryption will be implemented in the future.

## Install

Image-Steno requires the Python `Pillow` or `PIL` library and Pyton 3.4 or above. If you do not have `PIL` or `Pillow` installed the application will prompt you if you'd like to install library but it is recommended to install as the following before running:

'''
$ pip install Pillow
'''

## Usage

'''
usage: ImageSteno.py [-h] [-e] [-d] [-n] -i INPUT_FILE -o OUTPUT_FILE
                     [-r PRIVATE_KEY] [-u PUBLIC_KEY] [-p PLAINTEXT_FILE]
                     [-s SEED_FILE]
'''

## Examples

To encode an image without using a seed file and with no encryption:

`ImageSteno.py -e -n -i myimage.png -o codedimage.png -p textfile.txt`

To decode an image without using a seed file and with no encryption:

`ImageSteno.py -d -n -i codedimage.png -o textfile.txt`
