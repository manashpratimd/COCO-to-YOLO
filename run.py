'''
This script extracts the class ids that are mentioned in the 'coco_extract.yaml' config file.

If the coco dataset is not present in your local system, then the bash script "coco_download.sh" can be used to
download the dataset. The total size of the dataset is about 20GB.
ex: bash coco_download.sh

The annotations and images are to be stored in a similar fashion as in the official website of the dataset
i.e. the images and annotations should go in coco/images/ and coco/annotations/ respectively. 

Entries in the "coco_extract.yaml" config file are to be filled as-

1)Extract id: Enter the ids of the classes from the coco dataset, that are to be extracted in yolo format. Look for the
			 id numbers in the "ms_coco_classnames.txt" file

2)Start_index: The index number of the first class in the annotations of the yolo "txt" file.(defalut 0)

3)Path_to_train: Enter the absolute path to the "coco/annotations/instance_train2017.json" file in your system.
 	ex- "/home/user/coco/annotations/instances_train2017.json"

4)Path_to_val: Enter the absolute path to the "coco/annotations/instance_val2017.json" file in your system.
	ex- "/home/user/coco/annotations/instances_val2017.json"

5)Train_image: Enter the path to "coco/images/train" directory in your system.
	ex- "/home/user/coco/images/train2017"

6)Val_image: Enter the path to Path to "coco/images/val" directory in your system.
	ex- "/home/user/coco/images/val2017"



The yolo formatted annotation will be stored in the labels folder.

The file heirarchy in which the folders will be generated is shown below.

FILE HEIRARCHY
--------------
(root directory)
coco_to_yolo
	|
	|--labels
	|	 |--train
	|	 |--val
	|
	|--images
		 |--train
		 |--val

The images will be stored as 'Image_x.jpg'.
x denotes the image number.

'''

import json
import shutil
import yaml
from pathlib import Path
from tqdm import tqdm


ROOT = Path(__file__).resolve().parent


from utils.bbox import coco2yolo
from utils.sep_img import get_image 
from utils.sep_txt import get_txt_file 

with open("coco_extract.yaml", 'r') as cx:
	new_dict = yaml.safe_load(cx)

id_to_extract = new_dict['extract_id'] # The list of ids to be extracted.

start_index = new_dict['start_index']

train_json_path = new_dict['Path_to_train']
val_json_path = new_dict['Path_to_val']
train_image_path = Path(new_dict['Train_image'])
val_image_path = Path(new_dict['Val_image'])


def get_dict(path):

	json_path = path
	with open(json_path) as file_path:
		data = json.load(file_path)

	categories = data["categories"]
	images = data["images"]
	id_name_list = []

	for entries in categories:
		if entries["id"] in id_to_extract:
			id_name_list.append(entries["name"])

	print(f"Extracting classes:{id_name_list}")
	#create dictionary to store the classes

	class_dict = {}
	for entry in id_name_list:
		class_dict[entry] = []

	'''
	In the 'annotations' key's value of the json file, we will look through each element.
	We will check the 'category_id' key.

	'''

	annotations = data["annotations"]

	for entry in tqdm(annotations):
		if entry["category_id"] in id_to_extract:
			for i,val in enumerate(id_to_extract):
				if val == entry["category_id"]: 
					index = i
			image_id_no = entry["image_id"]
			for item in images:
				#match the id in annotation to id in images and get file name.
				if item["id"] == image_id_no:
					image_name = item["file_name"]
					height = item["height"]
					width = item["width"]
					break
			value_dict = {"image_name":image_name, "bbox":entry["bbox"], "width":width, "height":height}
			class_dict[id_name_list[index]].append(value_dict)

	#Till here the class_dict, which contains the required classes as keys and image_name, bbox, width and height as its value.
	#-------------------------------------------------------------------------------------------------------------------------

	'''
	In the next part extract the unique image names and store it in list "names"
	'''
	names = []
	for key in class_dict.keys():
		for item in class_dict[key]:
			if item["image_name"] not in names:
				names.append(item["image_name"])


	'''
	Get bbox in each image.
	create a dictionary, where keys will be the name of each unique image and the values will be list of bounding boxes and 
	corresponding id of the instance.

	Id will start at the "start_index" which is specified in the "coco_extract.yaml" config file.
	'''

	instance_dict = {}
	for item in names:
		instance_dict[item] = []


	for item in names:
		for index, key in enumerate(class_dict.keys()):
			for entries in class_dict[key]:
				if item == entries["image_name"]:
					coco_bbox = entries["bbox"] # This contains the coco formatted bbox
					yolo_bbox = coco2yolo(coco_bbox, entries["width"], entries["height"])
					yolo_bbox.insert(0, index+start_index)
					instance_dict[item].append(yolo_bbox)

	return instance_dict

'''
This part generates the txt files and copies the images from the coco datset into another folder, following the 
heirarchy mentioned above.
The images will be renamed as "Image_2.jpg", "Image_3.jpg" etc.

'''
train_dict = get_dict(train_json_path)
val_dict = get_dict(val_json_path)



get_txt_file(train_dict,"train",ROOT)
get_txt_file(val_dict,"val",ROOT)


get_image(train_image_path,train_dict,"train",ROOT)
get_image(val_image_path,val_dict,"val",ROOT)
