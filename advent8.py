import numpy as np
from matplotlib import pyplot as plt

data = str(eval(open('input8.txt').read()))

layers = []
for i in range(100):
    layers.append(data[i*25*6: (i+1)*25*6])

res_layer = layers[np.argmin([layer.count('0') for layer in layers])]
print('Part1 -> ', res_layer.count('1')*res_layer.count('2'))

fn_image = []
for i in range(len(layers[0])):
    for layer_px in layers:
        if int(layer_px[i])!=2:
            fn_image.append(int(layer_px[i]))
            break
print('Part2')
plt.imshow(np.reshape(fn_image, [6,25]))
plt.show()
