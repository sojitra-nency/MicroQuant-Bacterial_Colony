# -*- coding: utf-8 -*-
import cv2
from counter import cut, recognize, graph
import os


def main(fp, output='results'):
    if not os.path.exists(output):
        os.mkdir(output)
    for file in os.listdir(fp):
        fname = os.path.splitext(file)[0] + '_count.png'
        img = cv2.imread(os.path.join(fp, file), cv2.IMREAD_GRAYSCALE) / 255.0
        plate = cut(img, 0.1)
        num, dots = recognize(plate)
        graph(img, dots, show=False, fname=os.path.join(output, fname))
        print('count for {:^9}: {:3d}'.format(file, num))


if __name__ == '__main__':
    main('JERMS/peisister/20200109')
