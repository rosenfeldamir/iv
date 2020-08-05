import cv2
from glob import glob
import os
import sys

suffixes = ['.jpg', '.png']
assert len(sys.argv) > 1, 'must have at least one input argument'
input_ = sys.argv[1]


def get_input_list():
    inputs = []
    if os.path.isfile(input_):
        inputs = [input_]
    elif os.path.isdir(input_):
        inputs = []
        for s in suffixes:
            inputs.extend(glob(os.path.join(input_, '*' + s)))
        inputs = sorted(inputs)
    else:
        print('expected input to be file name or directory')
        exit(0)
    if len(inputs) == 0:
        print("Couldn't find any image files in specified path")
        exit(0)
    return inputs


EXIT_KEYS = [27, ord('q')]
LEFT_KEYS = [97, 81]
RIGHT_KEYS = [100, 83]


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


def main():
    inputs = get_input_list()
    win_name = 'iv minimal viewer'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(win_name, mouse_callback)
    img_index = 0
    I = cv2.imread(inputs[img_index])
    win_height = 720
    win_width = int(I.shape[1] * 720. / I.shape[0])
    cv2.resizeWindow(win_name, win_width, win_height)
    prev_index = img_index
    while (True):

        set_window_title(img_index, inputs, win_name)

        cv2.imshow(win_name, I)

        key = cv2.waitKey(0) & 0xFF
        if key in EXIT_KEYS:
            break
        elif key in LEFT_KEYS:
            img_index = (img_index - 1) % len(inputs)
        else:
            img_index = (img_index + 1) % len(inputs)
        if prev_index != img_index:
            I = cv2.imread(inputs[img_index])


def set_window_title(img_index, inputs, win_name):
    cur_img_path = inputs[img_index]
    window_caption = cur_img_path.split('/')[-1]
    cv2.setWindowTitle(win_name, window_caption)


if __name__ == '__main__':
    main()
