import cv2
import glob
import numpy as np
import time

# 종료 조건 설정
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

checkerboard_x = 10
checkerboard_y = 10


# 체커보드 3D 공간 상의 좌표 준비
cb_coord = np.zeros((checkerboard_x * checkerboard_y, 3), np.float32)
cb_coord[:, :2] = np.mgrid[0:checkerboard_x, 0:checkerboard_y].T.reshape(-1, 2)

#print(cb_coord)
