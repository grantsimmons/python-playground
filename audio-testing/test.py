import pygame
import numpy as np
from scipy import signal
from scipy.fftpack import rfft, irfft, fftfreq
from matplotlib import pyplot as plt

freq = 11025
  
pygame.mixer.pre_init(buffer=8192)
pygame.mixer.init(size=32, buffer=8192, channels=1, frequency=freq * 16)
pygame.mixer.set_num_channels(1)

img_map = []
with open("lenna.512", "rb") as img:
    while (byte := img.read(1)):
        img_map.append(int.from_bytes(byte))

img_map_2d = np.array(img_map).reshape(512,512)

conv_map = np.array([[-1, 0, 1], 
                    [-1, 0, 1], 
                    [-1, 0, 1]])
test_map2 = signal.convolve2d(img_map_2d, conv_map, boundary='symm', mode='same')

#plt.imshow(img_map_2d, cmap='gray', vmin=0, vmax=255)
for y, yval in enumerate(test_map2):
    for x, xval in enumerate(yval):
        if np.abs(test_map2[y][x]) > 75:
            test_map2[y][x] = 1
        elif np.abs(test_map2[y][x]) > 25 and np.abs(test_map2[y][x]) < 76:
            test_map2[y][x] = 0.5
        else:
            test_map2[y][x] = 0

#plt.imshow(img_map_2d, cmap='gray')
#plt.show()


#Seeds
signal = np.sin(0 * np.pi * np.arange(freq) * 440 / (freq))
W = fftfreq(signal.size, d=(1/(freq)))
f_signal = rfft(signal)
buffer_t = signal.astype(np.float32)

test_f = []
#test_f.append(f_signal)

img_width = 512 #width of image, get from array size

outfile = open("test.txt", "w")

#for y, row in enumerate(test_map2[::-1]):
for y, row in enumerate(img_map_2d[::-1]):
    cut_f_signal = f_signal.copy()
    start_freq = 300 / 2
    stop_freq = 3000 / 2
    width = int((stop_freq - start_freq) / img_width)
    for i, n in enumerate(row): #i = [0, 512]
        #intensity = 2000
        intensity = 2000 / 255
        cut_f_signal[(W==(start_freq + (i*width)))] = int(intensity * n)

    cut_f_signal[(W>stop_freq)] = 0
    cut_f_signal[(W<start_freq)] = 0
    cut_signal = irfft(cut_f_signal)
    test_f.append(cut_f_signal)

    buffer_t = np.append(buffer_t, cut_signal.astype(np.float32))

    for i in cut_f_signal.astype(np.float32):
        outfile.write(str(i))
    
    outfile.write('\n')
#plt.imshow(test_f, cmap='gray', aspect='auto')
#plt.show()

plt.imshow(img_map_2d, cmap='gray')
plt.show()

#exit()
print(np.size(buffer_t))
sound = pygame.mixer.Sound(buffer_t)
sound.play(0)
print(int(sound.get_length()))
pygame.time.wait(int(sound.get_length() * 1000))

plt.imshow(img_map_2d, cmap='gray')
plt.show()