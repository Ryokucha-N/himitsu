'''
(\__/) Code by Ryokucha-N
(=^.^) Version 0.2
(")(")
'''

from PIL import Image, ImageDraw
import wave
import struct
import os
from sys import argv
import math
#import time


def SaveInImg(input_image_path, input_datafile_path, output_image_path):
    image_rw = Image.open(input_image_path)
    w, h = image_rw.size

    max_file_size = w*h//2
    bytes_of_file_size = math.ceil( math.log(max_file_size, 2)/8 ) 
    max_file_size = max_file_size - bytes_of_file_size 
    
    file_size = os.path.getsize(input_datafile_path)

    if file_size > max_file_size:
        print("ERROR: file is too large, try using a larger image")
        return None    

    file_r = open(input_datafile_path,"rb")
    draw = ImageDraw.Draw(image_rw)
    pix = image_rw.load()

    for x in range(w):
        for y in range(h):

            #parameters for status bar
            p1 = int(30*((x*h+y)//2-bytes_of_file_size)/file_size)
            p2 = 30 - p1
            print("Saving...["+"#"*p1+"."*p2+"]"+str(int((100*(x*h+y)//2-bytes_of_file_size)/file_size))+"%")

            if (x*h+y)//2 < bytes_of_file_size:#ch is bytes of size
                ch = (file_size>>(8*(bytes_of_file_size-(x*h+y)//2-1)))%256
            elif (x*h+y)%2 == 0:#ch is data
                bit8 = file_r.read(1)
                if bit8 == b"":
                    print("Image save as "+output_image_path+"...")
                    image_rw.save(output_image_path)
                    return None
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

    image_rw.close()
    file_r.close()



def LoadFromImg(input_image_path, output_datafile_path):
    image_r = Image.open(input_image_path)
    w, h = image_r.size
    bytes_of_file_size = math.ceil(math.log(w*h//2, 2)/8) 
        
    file_w = open(output_datafile_path, "wb")
    file_size = 0
    pixel_arr_len = w*h - ((w*h) % 2)

    b = [0,0,0,0,0,0,0,0]

    for ipx in range(0,pixel_arr_len,2):
        px0 = image_r.getpixel((ipx//h, ipx%h))
        px1 = image_r.getpixel(((ipx+1)//h, (ipx+1)%h))
        
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
            #parameters for status bar
            p1 = int(30*(ipx//2-bytes_of_file_size)/file_size)
            p2 = 30 - p1
            print("Loading...["+"#"*p1+"."*p2+"]"+str(int(100*(ipx//2-bytes_of_file_size)/file_size))+"%")

            file_w.write(struct.pack(">B",ch))
            if ipx//2 == file_size+bytes_of_file_size-1:
                break

    image_r.close()
    file_w.close()




def SaveInWav(input_audio_path, input_datafile_path, output_audio_path):

    audio_r = wave.open(input_audio_path,'r')
    par = list(audio_r.getparams())
    par[3] = 0
    
    audio_w = wave.open(output_audio_path,'w')
    audio_w.setparams(tuple(par))

    file_r = open(input_datafile_path,'rb')
    file_size = os.path.getsize(input_datafile_path)

    max_file_size = audio_r.getnframes() * audio_r.getnchannels() // 800
    bytes_of_size_file = math.ceil(math.log(max_file_size,2)/8)
    max_file_size = max_file_size - bytes_of_size_file

    if audio_r.getnchannels() != 2:
        print("ERROR: stereo only")
    if max_file_size < file_size:
        print("ERROR: file is too large, try using a larger audio")
    else:
        for i in range(audio_r.getnframes()):
            frame = audio_r.readframes(1)

            j = i//100

            if i%100 == 0 and j//4 < file_size+bytes_of_size_file:
                l = struct.unpack(">H", frame[:2] )[0]
                r = struct.unpack(">H", frame[2:] )[0]

                if j%4 == 0:
                
                    if j/4 < bytes_of_size_file:
                        
                        ch = (file_size>>(8*(bytes_of_size_file-1-j//4%4)))%256
                    else:
                        ch = ord(file_r.read(1))

                    bit8 = [0]*8
                    for ii in range(8):
                        bit8[ii] = int(bool( ch&2**(7-ii) ))

                nl = struct.pack(">H", l - l%2 + bit8[j%4*2+0] )
                nr = struct.pack(">H", r - r%2 + bit8[j%4*2+1] )

                new_frame = nl+nr

            else:
                new_frame = frame
            print(i,"/",audio_r.getnframes())
            audio_w.writeframes(new_frame)

    audio_r.close()
    audio_w.close()
    file_r.close()



def LoadFromWav(input_audio_path, output_datafile_path):

    audio_r = wave.open(input_audio_path,'r')
    file_w = open(output_datafile_path,'wb')
    
    file_size = 0
    max_file_size = audio_r.getnframes() * audio_r.getnchannels() // 800
    bytes_of_size_file = math.ceil(math.log(max_file_size,2)/8)
    
    if audio_r.getnchannels() != 2:
        print("ERROR: stereo only")
    else:
    
        bit8 = [0]*8
        for i in range(audio_r.getnframes()//400):

            for ii in range(4):
                for iii in range(100):
                    frame = audio_r.readframes(1)

                    if iii == 0:
                        l = struct.unpack(">H", frame[:2] )[0]
                        r = struct.unpack(">H", frame[2:] )[0]

                bit8[ii%4*2+0] = l%2
                bit8[ii%4*2+1] = r%2

            ch = 0
            for ii in range(8):
                ch += bit8[ii]*2**(7-ii)
            if i < bytes_of_size_file:
                print(bit8)
                print(ch)
                print(file_size)                
                file_size += ch<<8*(bytes_of_size_file-i-1)
            elif i < bytes_of_size_file + file_size:
                file_w.write(struct.pack(">B",ch))
            else:
                break
                
    audio_r.close()
    file_w.close()






def ShowLogo():
    print()
    print(
    r"(\__/)" "                                 " r"(\__/)"  "\n"
    r"(=^.^)" "          H I M I T S U          " r"(^.^=)"  "\n"
    r'(")(")' "                                 " r'(")(")'  "\n"
    )
    print("Code by Ryokucha-N")


def SaveMenu(file_type):
    while True:
        print("\n")
        input_disgfile_path = input("Input "+file_type+" path> ")
        input_datafile_path = input("Input datafile path> ")
        output_disgfile_path = input("Output "+file_type+" path> ")
        print("\n")
        print(file_type+" path:",input_disgfile_path)
        print("Input datafile path:",input_datafile_path)
        print("Output "+file_type+" path:",output_disgfile_path)
        select = input("Correct? [Yes/No/Back]> ")
        print("\n")
        
        if select.lower() == "y" or select.lower() == "yes":
            if file_type == "Image":
                SaveInImg(input_disgfile_path, input_datafile_path, output_disgfile_path)
            elif file_type == "Audio":
                SaveInWav(input_disgfile_path, input_datafile_path, output_disgfile_path)
            break
        elif select.lower() == "n" or select.lower() == "no":
            continue
        else:
            break


def LoadMenu(file_type):
    while True:
        print("\n")
        input_disgfile_path = input("Input "+file_type+" path> ")
        output_datafile_path = input("Output datafile path> ")
        print("\n")
        print("Input "+file_type+" path:",input_disgfile_path)
        print("Output datafile path:",output_datafile_path)
        select = input("Correct? [Yes/No/Back]> ")
        print("\n")
    
        if select.lower() == "y" or select.lower() == "yes":
            if file_type == "Image":
                LoadFromImg(input_disgfile_path, output_datafile_path)
            elif file_type == "Audio":
                LoadFromWav(input_disgfile_path, output_datafile_path)
            break
        elif select.lower() == "n" or select.lower() == "no":
            continue
        else:
            break


def Interactive():
    ShowLogo()
    while True:
        print("\n")
        print("Select mode:")
        print("[1] Save file in image")
        print("[2] Load file from image")
        print()
        print("[3] Save file in audio")
        print("[4] Load file from audio")
        print()
        print("[0] Exit")
        select = input("> ")
                
        if select == "0":
            exit()
        elif select == "1":
            SaveMenu("Image")  
        elif select == "2":
            LoadMenu("Image")
        elif select == "3":
            SaveMenu("Audio")
        elif select == "4":
            LoadMenu("Audio")



def WithArgs():
    mode = argv[1]

    if "s" in mode:
        input_disgfile_path = argv[2]
        input_datafile_path = argv[3]
        output_disgfile_path = argv[4]

        if "i" in mode:
            SaveInImg(input_disgfile_path, input_datafile_path, output_disgfile_path)
        if "a" in mode:
            SaveInWav(input_disgfile_path, input_datafile_path, output_disgfile_path)
        
    elif "l" in mode:
        input_disgfile_path = argv[2]
        output_datafile_path = argv[3]
        
        if "i" in mode:
            LoadFromImg(input_disgfile_path, output_datafile_path)        
        if "a" in mode:
            LoadFromWav(input_disgfile_path, output_datafile_path)        





if len(argv) == 1:
    Interactive()
else:
    WithArgs()
