'''
(\__/) Code by Ryokucha-N
(='.') Version 0.1
(")(")
'''

from PIL import Image, ImageDraw
import struct
import os
import math
import time

def ShowLogo():
    print()
    print(
    r"(\__/)" "                                 " r"(\__/)"  "\n"
    r"(='.')" "          H I M I T S U          " r"('.'=)"  "\n"
    r'(")(")' "                                 " r'(")(")'  "\n"
    )
    print("Code by Ryokucha-N")
    

def SaveInImg(image, in_file_path, bytes_of_file_size, file_size, out_image_path):
    file = open(in_file_path,"rb")
    draw = ImageDraw.Draw(image)
    w = image.size[0]
    h = image.size[1]
    pix = image.load()

    for x in range(w):
        for y in range(h):

            #parameters for status bar
            p1 = int(30*(x*h+y)/(w*h))
            p2 = 30 - p1
            print("Saving...["+"#"*p1+"."*p2+"]"+str(int(100*(x*h+y)/(w*h)))+"%")

            if (x*h+y)//2 < bytes_of_file_size:#ch is bytes of size
                ch = (file_size>>(8*(bytes_of_file_size-(x*h+y)//2-1)))%256
            elif (x*h+y)%2 == 0:#ch is data
                bit8 = file.read(1)
                if bit8 == b"":
                    ch = 0
                else:
                    ch = ord(bit8)

            bit4 = (
            (ch&2**(3+4*((x*h+y)%2)))//2**(3+4*((x*h+y)%2)),
            (ch&2**(2+4*((x*h+y)%2)))//2**(2+4*((x*h+y)%2)),
            (ch&2**(1+4*((x*h+y)%2)))//2**(1+4*((x*h+y)%2)),
            (ch&2**(0+4*((x*h+y)%2)))//2**(0+4*((x*h+y)%2))
            )

            new_px = [0,0,0,0]
            for i in range(0,4):
                new_px[i] = pix[x, y][i] - pix[x, y][i]%2 + bit4[i]

            draw.point((x, y), tuple(new_px))

    print("Image save as "+out_image_path+"...")
    image.save(out_image_path)



def LoadFromImg(image, bytes_of_file_size, output_file_path):
    file = open(output_file_path, "wb")
    file_size = 0
    img_w, img_h = image.size
    pixel_arr_len = img_w*img_h - ((img_w*img_h) % 2)

    b = [0,0,0,0,0,0,0,0]

    for ipx in range(0,pixel_arr_len,2):
        px0 = image.getpixel((ipx//img_h, ipx%img_h))
        px1 = image.getpixel(((ipx+1)//img_h, (ipx+1)%img_h))
        
        for i in range(0,4):
            b[i] = px1[i] % 2
        for i in range(0,4):
            b[4+i] = px0[i] % 2

        ch = 0
        for i in range(8):
            ch += 2**(7-i)*b[i]

        if ipx//2 < bytes_of_file_size:
            file_size += ch<<(8*(bytes_of_file_size-(ipx//2)-1))
        else:
            file.write(struct.pack(">B",ch))
            if ipx//2 == file_size+bytes_of_file_size-1:
                break



def SaveMenu():
    while True:
        print("\n")
        input_image_path = input("Input image path> ")
        input_file_path = input("Input file path> ")
        output_image_path = input("Output image path> ")
        print("\n")
        print("Image path:      ",input_image_path)
        print("Input file path: ",input_file_path)
        print("Output image path:",output_image_path)
        select = input("Correct? [Yes/No/Back]> ")
        print("\n")

        if select == "" or select.lower() == "y" or select.lower() == "yes":
            input_image = Image.open(input_image_path)
            bytes_of_file_size = math.ceil(math.log(input_image.size[0]*input_image.size[1]//2, 2)/8) 
            max_file_size = input_image.size[0]*input_image.size[1]//2 - bytes_of_file_size 
            file_size = os.path.getsize(input_file_path)

            if file_size > max_file_size:
                print("ERROR: file is too large, try using a larger image")
                break
            else:
                SaveInImg(input_image, input_file_path, bytes_of_file_size, file_size, output_image_path)
                print("Done")
                print()
                break
        elif select.lower() == "n" or select.lower() == "no":
            pass 
        else:
            break



def LoadMenu():
    while True:
        print("\n")
        input_image_path = input("Input image path> ")
        output_file_path = input("Output file path> ")
        print("\n")
        print("Input image path:",input_image_path)
        print("Output file path:",output_file_path)
        select = input("Correct? [Yes/No/Back]> ")
        print("\n")
    
        if select == "" or select.lower() == "y" or select.lower() == "yes":
            input_image = Image.open(input_image_path)
            bytes_of_file_size = math.ceil(math.log(input_image.size[0]*input_image.size[1]//2, 2)/8) 
            LoadFromImg(input_image, bytes_of_file_size, output_file_path)        
            print("Done")
            print("\n")
            break
        elif select.lower() == "n" or select.lower() == "no":
            pass
        else:
            break




ShowLogo()
while True:
    print("\n")
    print("Select mode:")
    print("[1] Save file in image")
    print("[2] Load file from image")
    print()
    print("[0] Exit")
    select = input("> ")

    if select == "0":
        exit()
    elif select == "1":
        SaveMenu()  
    elif select == "2":
        LoadMenu()
