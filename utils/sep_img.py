import shutil
from pathlib import Path

def get_image(path,instance_dict,torv,root):
	'''Arguments:
		path: the path where the images are stored from which we have to extract the required image. Either train or val
		instance_dict: either train or val
		torv: string. Either "train" or "val"
	'''
	
	instance_dict = instance_dict
	torv = torv
	ROOT = root
	coco_to_yolo = ROOT/"coco_to_yolo"/"images"/torv
	coco_to_yolo.mkdir(parents=True, exist_ok = True)


	image_name_list = list(instance_dict.keys()) #This list contains the name of images.
	image_name_list.sort() # have to sort before copying the files as the same is done in txt generation.

	count = 1

	for item in image_name_list:
		source = path/item
		dest = coco_to_yolo/f"Image_{count}.jpg"
		count += 1
		shutil.copyfile(source, dest)