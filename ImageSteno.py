#!/usr/bin/python3.4

import sys, argparse, os.path
from pathlib import Path
from random import Random

try:
    import pip
except ImportError:
    pass
    #if they don't have pip then this is dealt with below
    #pip.main(['install', 'Pillow']) should be caught in a try/except

try:
    from PIL import Image
except ImportError:
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input(
            "This application requires the Pillow image library. Would you like to try download and install it through pip? (y/n)")
    if prompt == "n":
        sys.exit(1)
    else:
        try:
            pip.main(['install', 'Pillow'])
            try:
                from PIL import Image
            except ImportError:
                print("Could not import Pillow")
                sys.exit(1)
        except:
            print("Could not install Pillow through pip; try updating pip or installing outside of this program")
            sys.exit(1)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encode', help='Encode file', action='store_true')
    parser.add_argument('-d', '--decode', help='Decode file', action='store_true')
    parser.add_argument('-i', '--input-file', help='Input file location/name; should be an image filetype if you are encoding', required=True, type=str)
    parser.add_argument('-o', '--output-file', help='Output file location/name; should be an image filetype if you are decoding', required=True, type=str)
    parser.add_argument('-p', '--plaintext-file', help='Plaintext file location/name to be inserted within image', type=str, default="noArg")
    parser.add_argument('-s', '--seed-file', help='Seed file location/name', type=str, default="noArg")
    args = parser.parse_args()
    args.uses_system_input_seed = False
    validateArgs(args)
    validateFiles(args)

    if args.encode == True:
        encode(args)

    if args.decode == True:
        decode(args)

def decode(args):
    print("Decoding image...")

    #start file reads
    try:
        inputImage = Image.open(args.input_file)
    except:
        print("Could not load input image file " + args.input_file)
        sys.exit(1)
    #end file reads

    #run decode function
    textDecoded = decodingFunction(args, inputImage)

    try:
        outputPlaintext = open(args.output_file, "w")
        outputPlaintext.write(textDecoded)
        outputPlaintext.close()
    except:
        print("Could not write output text file " + args.output_file)
        sys.exit()

    print("Image successfully decoded")

def encode(args):
    print("Encoding image...")

    #start file reads
    try:
        textFile = open(args.plaintext_file, 'r')
        plaintext = textFile.read(); textFile.close()
    except:
        print("Could not load plaintext file " + args.plaintext_file +"; is it a text file?")
        sys.exit()

    try:
        inputImage = Image.open(args.input_file)
    except:
        print("Could not load input image file " + args.input_file)
        sys.exit()
    #end file reads

    #add a sequence at the end of the string to let the decoder know when to stop
    #should be obscured if using custom-set seed
    plaintext += "[STOP_SEQ]"
    plaintextBits = stringToBits(plaintext)  # should be in list form
    plaintextBitCount = len(plaintextBits)
    width, height = inputImage.size

    if (plaintextBitCount > width * height * 4): #we are going to be encoding 4 bits of data in every pixel
        print("Your image file " + args.input_file + "is too small for the text you provided to be encoded in the image")

    try:
        imageEncoded = encodingFunction(args, inputImage, plaintextBits, plaintextBitCount)
    except:
        print("Could not encode text file " + args.plaintext_file + " into image; does it contain non-ASCII or unicode characters?")
        sys.exit(1)

    inputFileExtension = args.input_file.split(".",1)[-1]
    outputFileExtension = args.output_file.split(".",1)[-1]
    #rembmer that args.input_file.split(".",1)[-1] returns a single-item list
    if inputFileExtension != outputFileExtension:
        print("Your output image file extension " + outputFileExtension + " does not match your input image file exension " + inputFileExtension)
        prompt = ""
        while (prompt != "y" and prompt != "n"):
            prompt = input("Would you like to replace (or add) the output file extension with the input file extension? (y/n)")
        if prompt == "y":
            outputFileName = (".").join([("").join(args.output_file.split(".",1)[0]), inputFileExtension])
        else:
            outputFileName = args.output_file
    else:
        outputFileName = args.output_file

    try:
        imageEncoded.save(outputFileName)
    except:
        print("Could not save output image file " + outputFileName)
        sys.exit(1)

    print("Image successfully encoded")

def decodingFunction(args, inputImage):
    decodeRandom = Random()  # make a unique Random instance

    #set seed
    if (args.seed_file == "noArg"):
        decodeRandom.seed("this could be anything")
    elif (args.uses_system_input_seed == True):
        decodeRandom.seed(args.seed_file)
    else:
        try:
            seedFile = open(args.seed_file, 'r')
            seed = seedFile.read()
            seedFile.close()  # for seed
            decodeRandom.seed(seed)
        except:
            print("Could not load seed file " + args.seed_file + "; is it a text file?")
            sys.exit()

    width, height = inputImage.size
    rgbInput = inputImage.convert("RGB")
    textDecoded = ""
    bitsGathered = 0
    bitList = []

    for y in range(1, height):
        for x in range(1, width):
            r, g, b = rgbInput.getpixel((x, y))
            randomTemp = decodeRandom.randint(0,2)
            #assign r, g, then b and firstbit secondbit
            if randomTemp == 0:
                lastTwoBitsR = r & 3
                bitList.append(lastTwoBitsR & 1)
                bitList.append((lastTwoBitsR & 2) >> 1)
                bitList.append(g & 1)
                bitList.append(b & 1)
                bitsGathered += 4
            elif randomTemp == 1:
                lastTwoBitsG = g & 3
                bitList.append(r & 1)
                bitList.append(lastTwoBitsG & 1)
                bitList.append((lastTwoBitsG & 2) >> 1)
                bitList.append(b & 1)
                bitsGathered += 4
            elif randomTemp == 2:
                lastTwoBitsB = b & 3
                bitList.append(r & 1)
                bitList.append(g & 1)
                bitList.append(lastTwoBitsB & 1)
                bitList.append((lastTwoBitsB & 2) >> 1)
                bitsGathered += 4
            #for every ASCII byte
            if(bitsGathered % 8 == 0):
                textDecoded += stringFromBits(bitList)
                bitList = []
                if(textDecoded.endswith("[STOP_SEQ]")):
                    textDecoded = textDecoded[:-10]
                    return textDecoded
    print("Reached end of file without encountering stop sequence; check if your file is encoded or if you have the right seed")
    sys.exit(1)

def encodingFunction(args, inputImage, plaintextBits, plaintextBitCount):
    encodeRandom = Random()  # make a unique Random instance

    if (args.seed_file == "noArg"):
        encodeRandom.seed("this could be anything")
    elif (args.uses_system_input_seed == True):
        encodeRandom.seed(args.seed_file)
    else:
        try:
            seedFile = open(args.seed_file, 'r')
            seed = seedFile.read()
            seedFile.close()
            encodeRandom.seed(seed)
        except:
            print("Could not load seed file " + args.seed_file + "; is it a text file?")
            sys.exit(1)

    rgbInput = inputImage.convert("RGB")
    width, height = rgbInput.size  # maybe works
    bitsImplemented = 0
    for y in range(1, height):
        for x in range(1, width):
            r, g, b = rgbInput.getpixel((x, y))
            randomTemp = encodeRandom.randint(0, 2)
            # set 2 LSBs of r integer, 1 LSB of g, and 1 LSB of b
            if randomTemp == 0:
                # assign first bit of r
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    r = r & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    r = r | 1; bitsImplemented += 1
                # assign second bit of r
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    r = (r & ~(1 << 1)) | (0 << 1); bitsImplemented += 1
                else:
                    r = (r & ~(1 << 1)) | (1 << 1); bitsImplemented += 1
                # assign first bit of g
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    g = g & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    g = g | 1; bitsImplemented += 1
                # assign first bit of b
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    b = b & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    b = b | 1; bitsImplemented += 1
            elif randomTemp == 1:
                # assign first bit of r
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    r = r & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    r = r | 1; bitsImplemented += 1
                # assign first bit of g
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    g = g & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    g = g | 1; bitsImplemented += 1
                # assign second bit of g
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    g = (g & ~(1 << 1)) | (0 << 1); bitsImplemented += 1
                else:
                    g = (g & ~(1 << 1)) | (1 << 1); bitsImplemented += 1
                # assign first bit of b
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    b = b & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    b = b | 1; bitsImplemented += 1
            elif randomTemp == 2:
                # assign first bit of r
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    r = r & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    r = r | 1; bitsImplemented += 1
                # assign first bit of g
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    g = g & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    g = g | 1; bitsImplemented += 1
                # assign first bit of b
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    b = b & ~1; bitsImplemented += 1
                else:  # if we need to put in a 1
                    b = b | 1; bitsImplemented += 1
                # assign second bit of b
                if plaintextBits[bitsImplemented] == 0:  # if we need to put in a zero
                    b = (b & ~(1 << 1)) | (0 << 1); bitsImplemented += 1
                else:
                    b = (b & ~(1 << 1)) | (1 << 1); bitsImplemented += 1
            #set the pixel itself
            pixelValue = (r, g, b)
            inputImage.putpixel((x, y), pixelValue)
            #this should work as it takes at least two pixels to represent one character
            if bitsImplemented >= plaintextBitCount:
                return inputImage

#https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def stringToBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

#https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def stringFromBits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def validateFiles(args):
    #does not need if, this is required input and is always checked
    try:
        if Path(args.input_file).is_file() == False:
            print("Input file " + args.input_file + " does not exist")
            sys.exit(2)
    except:
        print("Error reading input file " + args.input_file + "(do you have permissions?)")
        sys.exit(1)

    #if we are encoding we need to check plaintext file
    if args.encode == True:
        try:
            if Path(args.plaintext_file).is_file() == False:
                print("Plaintext file " + args.plaintext_file + " does not exist")
                sys.exit(2)
        except:
            print("Error reading plaintext file " + args.plaintext_file + "for encoding (do you have permissions?)")
            sys.exit(1)

def validateArgs(args):
    if args.encode == True and args.decode == True:
        print("You must choose to either encode or decode a file, not both")
        argErrorQuit(2)
    if args.input_file == "noArg":
        print("You must specify an input file")
        argErrorQuit(2)
    if args.output_file == "noArg":
        print("You must specify an output file")
        argErrorQuit(2)
    if args.encode == True and args.plaintext_file == "noArg":
        print("You must supply a plaintext file to be inserted into the image if you are encoding a file")
        argErrorQuit(2)
    if args.seed_file == "noArg":
        prompt = ""
        while (prompt != "q" and prompt != "e" and prompt != "d"):
            prompt = input("You did not select a seed file. Would you like use the default seed value, enter one, or quit? (d/e/q) ")
        if prompt == "q":
            sys.exit(2)
        elif prompt == "e":
            args.seed_file = input("Please enter the seed you would like to use: ")
            args.uses_system_input_seed = True
    if args.encode == False and args.decode == False:
        print("You must chose whether to encode or decode a file")
        sys.exit(2)
    if args.encode == True and args.input_file.lower().endswith(('.png', '.bmp')) == False:
        print("You may be trying to use an unsupported or lossy file format\n")
        print("Supported file formats are .png and .bmp\n")
        print("Encoding in a lossy format will likely result in an undecoeable image.\n")
        prompt = ""
        while (prompt != "y" and prompt != "n"):
            prompt = input("Would you like to continue anyway? (y/n) ")
        if prompt == "n":
            sys.exit(2)

def argErrorQuit():
    print("ImageSteno.py -e [encode] -d [decode] -i <inputimage> -o <outputfile> -p <plaintextfile> -s <seedfile>")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
