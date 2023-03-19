def coco2yolo(bbox_list, width, height):
	'''
	The bbox_list contains the bounding box parameters.
	Width and height are the dimensions of the original image.

	Return: a list with yolo formatted annotations(normalise entries) 
	'''
	xyolo = round((bbox_list[0] + bbox_list[2]/2) / width, 6)
	yyolo = round((bbox_list[1] + bbox_list[3]/2) / height,6)
	widthyolo = round(bbox_list[2] / width,6)
	heightyolo = round(bbox_list[3] / height,6)

	return [xyolo, yyolo, widthyolo, heightyolo]