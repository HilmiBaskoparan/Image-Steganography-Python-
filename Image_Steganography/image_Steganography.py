# C:\Users\asus\Desktop\manzara.jpg

from PIL import Image

import imgstg


# Convert encoding data into 8-bit binary
# form using ASCII value of characters

def genData(data):
    # list of binary codes of given data
    list = []

    # add an item to end of list
    for i in data:
        list.append(format(ord(i), '08b'))
    return list

# Pixels are modified according to the 8-bit binary data and finally returned

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0

        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eigth pixel of every set tells whether to stop ot read further.
        # 0 means keep reading; 1 means the message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    changedPixels = []
    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        changedPixels.append((x,y))
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    return changedPixels

# Encode data into image
def encode(img,datafile,c):

    image = Image.open(img, 'r')
    if c == 0 :
        myfile = open(datafile)
        data = myfile.read()
    else:
        data = datafile

    if (len(data) == 0):
        from tkinter import messagebox
        messagebox.showinfo("WARNING", "Text data is empty !")
        return

    newimg = image.copy()
    #print(newimg)
    redPixels = encode_enc(newimg, data)

    new_img_name = img.split(".")[0]+"_encoded."+img.split(".")[1]

    newimg_redPixels = image.copy()
    pixels = newimg_redPixels.load()  # create the pixel map

    for x,y in redPixels:  # for every red pixel:
        pixels[x, y] = (255, 0, 0)


    #newim = Image.new(image.mode, image.size)

    #newim.putdata(pixels)
    newimg_redPixels.save(img.split(".")[0]+"_encoded_redpixelled."+img.split(".")[1])
    newimg_redPixels.save(img.split(".")[0]+"_encoded_decoded_redpixelled."+img.split(".")[1])
    #print("{} saved!".format(new_img_name))
    #print(img)
    #print(new_img_name)
    newimg.save(new_img_name)



# Decode the data in the image
def decode(img):

    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())
    #print('image data = ',imgdata)

    newimg = image.copy()
    # print(newimg)
    new_img_name = img.split(".")[0] + "_decoded." + img.split(".")[1]
    newimg.save(new_img_name)
    redPixels = []
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        #print(pixels)
        # string of binary data
        binstr = ''

        # 8 bitlik binary şeklinde çekilen pikseller i mod 2=0 ise 0, i mod 2=1 ise 1 eklenir.

        for i in pixels[:8]:
            #print('i = ',i)
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        #print('binstr = ',binstr)
        # binstr ile alınan binary değer ascii tablosundaki karşılığına atanır.
        if len(chr(int(binstr, 2))) != 0:
            data += chr(int(binstr, 2))

        #print('data = ',data)
        if (pixels[-1] % 2 != 0):
            a = open("decoded.txt","w")
            a.write(data)
            return data

        # Main Function

def main():
    '''
       a = int(input("\n>>>>> Welcome to Steganography <<<<<\n"
                     "1. To Encode\n2. To Decode\n3. Image Information\n0. Exit Program\n"))
       if (a == 1):
           encode()
           main()

       elif (a == 2):
           print("\nDecoded Message : \n", decode())
           main()

       elif (a == 3):
           img = input("Enter image name(with extension): ")
           image = Image.open(img, 'r')
           print("Image Format : ", image.format)
           print("Image Mode : ", image.mode)
           print("Image Size : ", image.size)
           height, width = image.size
           pix = height*width
           print("Image Pixels : ", pix)
           main()

       elif (a == 0):
           print("\n...You Terminated the Program...")
           return 0

       else:
           print("\nPlease Enter Correct Input!!")
           main()
    '''

if __name__ == '__main__':
    # Calling main function
    main()