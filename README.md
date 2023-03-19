# COCO-to-YOLO
## Overview
This repo can be used to extract the images and annotations(in yolo format) from the coco dataset, of the desired class ids.


## Data

If the coco dataset is not present in your local system, then the bash script "coco_download.sh" can be used to
download the dataset. The total size of the dataset is about 20GB(train images, val images, train annotations and val annotations).

```
bash coco_download.sh
```

## Usage guide

First generate the class names and ids corresponding to each class of the coco dataset.

If the coco dataset has been downloaded using the "coco_download.sh" script, then run the following command for generation of the class id and name txt file.

```
python gen_class_id.py
```

Incase the dataset is already present in your local system then pass the path of the "instances_train2017.json" file as an argument.

```
python gen_class_id.py /home/user/coco/annotations/instances_train2017.json
```
This will generate a txt file named "class_id_name.txt", which will contain the ids corresponding to each class name.

In the "coco_extract.yaml" config file, enter the classid (the "class_id_name.txt" file can be used as reference) of those classes whose images and annotations are to be extracted.

Example:

```
extract_id: [12,23]
```

The corresponding entries are of the annotation and image file paths. If the dataset is being downloaded using the accompanying download script, then these entries doesn't need to be changed or else provide the path to the annotations and images.

Once the config file is set properly, run the following command:

```
python run.py
```

This will generate a folder named "coco_to_yolo", containing the images and annotations(in yolo format).
