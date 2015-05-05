import cv2 
import os
import numpy as np
import cPickle

def main():
	#move_pics()
	make_avg_background()
	#find_contours()


def move_pics():
	pics = dict()
	for folder in ['fly_with_food_stills', 'larvae_stills']:
		pics[folder] = []
		img_folder = 'videos_for_tracking/' + folder
		for root, dirs, filenames in os.walk(img_folder):
			for f in filenames:
				filename = os.path.join('videos_for_tracking', folder, f)
				larva_img = cv2.imread(filename, 0)
				pics[folder].append(larva_img)
				output_filename = os.path.join('output', folder, f)
				cv2.imwrite(output_filename, larva_img)
	cPickle.dump(pics, open('output/all_imgs.pickle', 'wb'))
	return pics

def make_avg_background():                	                    
	pics = cPickle.load(open('output/all_imgs.pickle', 'r'))
	for scene in pics.keys():
    # initialize accumulator destination
		cumulative_img = np.float64(pics[scene][0])
		cumulative_img /= 255.0
		cv2.imshow('init cumulative', cumulative_img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		for n in range(100):
			for i in range(len(pics[scene])):
				#pics[scene][i] = 255 - pics[scene][i]
				#cv2.imshow('img', pics[scene][i])
				#cv2.waitKey(0)
				#pics[scene][i] = cv2.cvtColor(pics[scene][i], cv2.COLOR_BGR2GRAY)
				cv2.accumulateWeighted(np.float64(pics[scene][i])/255.0, cumulative_img, .01)


		cv2.imshow('avg bkgd', cumulative_img)
		cv2.waitKey(0)
		output_filename = os.path.join('output', scene, 'background.jpg')
		cv2.imwrite(output_filename, cumulative_img*255.0)
		

main()

