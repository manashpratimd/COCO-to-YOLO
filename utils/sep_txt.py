def get_txt_file(instance_dict,torv,root):
	'''Argument: instance_dict - train_dict or val_dict
				 torv - train or val, pass as string to state if it is for train or val.

	'''

	instance_dict = instance_dict
	torv = torv
	ROOT = root
	coco_to_yolo= ROOT/"coco_to_yolo"/"labels"/torv
	coco_to_yolo.mkdir(parents=True, exist_ok = True)
	file_name_list = list(instance_dict.keys())


	file_name_list.sort()

	count = 1
	for item in file_name_list:
		write_data = instance_dict[item]
		no_bbox = len(write_data) #gives the number of bounding boxes in the image

		with open(coco_to_yolo/f"Image_{count}.txt","w") as ff:
			for index,entry in enumerate(write_data):
				if index+1 < no_bbox:
					write_string = str(entry[0]) + " " + str(entry[1]) + " " + str(entry[2]) + " " + str(entry[3]) +  " " + str(entry[4]) +"\n"
					ff.write(write_string)

				else:
					write_string = str(entry[0]) + " " + str(entry[1]) + " " + str(entry[2]) + " " + str(entry[3]) + " " + str(entry[4])
					ff.write(write_string)

		count += 1