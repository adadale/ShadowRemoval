import numpy as np
import cv2
import time
import sys  
sys.setrecursionlimit(1000000)
from main import timeit, get_size

### Configurations ###
DOWNSAMPLE = 2
SEED_ITER = 4
RATE = 0.5
CANNY = (50, 150)
COL_SEED = 200
######################

# def downsample(img, rate = RATE):
# 	dst = np.array(img[::int(1/rate),::int(1/rate),:], dtype=np.uint8)
# 	cv2.pyrDown(img, dst, (int(img.shape[1]*rate), int(img.shape[0]*rate)))
# 	return dst
downsample = lambda img, rate = RATE: cv2.pyrDown(img, np.array(img[::int(1/rate),::int(1/rate),:], dtype=np.uint8), (int(img.shape[1]*rate), int(img.shape[0]*rate)))
gray = lambda img: cv2.cvtColsbor(img, cv2.COLOR_BGR2GRAY)
dist = lambda x, y: sum((x-y)**2)

def detect(img, seed):
	seed = (seed[1], seed[0])
	shape = get_size(img)
	[Ms, Ml, Mshadow] = [np.zeros(shape, dtype=np.uint8) for i in range(3)]
	tmp = np.array(img)
	for i in range(DOWNSAMPLE):
		img_ds = downsample(tmp)
		tmp = img_ds
	seed_ds = (int(seed[0]*RATE**DOWNSAMPLE), int(seed[1]*RATE**DOWNSAMPLE))
	seed_pixel = img_ds[seed_ds]
	shape_ds = (int(shape[0]*RATE**DOWNSAMPLE), int(shape[1]*RATE**DOWNSAMPLE))
	edges = cv2.Canny(cv2.GaussianBlur(img, (3, 3), 0), CANNY[0], CANNY[1])
	seed_mask_ds = np.zeros(get_size(img_ds))
	seed_mask_ds[seed_ds] = 1
	vis = np.zeros(get_size(img_ds))
	directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
	def search(point, seed_pixel):
		if point[0] < 0 or point[1] < 0 or point[0] >= shape_ds[0] or point[1] >= shape_ds[1]:
			return
		if vis[point]:
			return
		elif edges[point]:
			return
		elif(dist(img_ds[point], seed_pixel) < COL_SEED):
			vis[point] = 1
			seed_mask_ds[point] = 1
			for i in range(4):
				search((point[0]+directions[i][0], point[1]+directions[i][1]), seed_pixel)
	for i in range(SEED_ITER):
		search(seed_ds, seed_pixel)
		seed_pixel = np.mean(np.mean(img_ds[np.where(seed_mask_ds == 1)], axis = 0), axis = 0)
	return seed_ds
	

def click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		seed = (x, y)
		print(seed)
		seeds = detect(img, seed)
		cv2.imshow('seeds', seeds)
		while(1):
			k = 0xFF & cv2.waitKey(1)
			if k == 27:
				cv2.destroyAllWindows()
				break

if __name__ == '__main__':
	img = cv2.imread('E:\\Chuan\\Pictures\\test.jpg')
	cv2.namedWindow('input')
	cv2.setMouseCallback('input', click)
	cv2.imshow('input', img)
	# dst = detect(img, seed)
	# cv2.imshow('dst', dst)
	while(1):
		k = 0xFF & cv2.waitKey(1)
		if k == 27:
			cv2.destroyAllWindows()
			break