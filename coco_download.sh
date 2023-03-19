#!/bin/bash

:'
 The heirarchy of the downloaded dataset:
(root directory)
   |
   |
   |--data
   		|
   		|--coco
   			|
   			|--images
   			|	|
   			|	|--train
   			|	|
   			|	|--val
			|
			|--annotations
'

    
mkdir -p ./data
cd ./data/
mkdir -p ./coco
cd ./coco
mkdir -p ./images
mkdir -p ./annotations
cd ./images
mkdir -p ./train  
mkdir -p ./val  

  
# Download the image data.
echo "Downloading MSCOCO train images ..." # around 19G
curl -LO http://images.cocodataset.org/zips/train2017.zip
echo "Downloading MSCOCO val images ..." # around 1G
curl -LO http://images.cocodataset.org/zips/val2017.zip

cd ../

# Download the annotation data.
cd ./annotations
echo "Downloading MSCOCO train/val annotations ..."
curl -LO http://images.cocodataset.org/annotations/annotations_trainval2017.zip
echo "Finished downloading. Now extracting ..."

# Unzip data
echo "Extracting train images ..."
unzip -qqjd ../images/train ../images/train2017.zip
echo "Extracting val images ..."
unzip -qqjd ../images/val ../images/val2017.zip
echo "Extracting annotations ..."
unzip -qqd .. ./annotations_trainval2017.zip

echo "Removing zip files ..."
rm ../images/train2017.zip
rm ../images/val2017.zip
rm ./annotations_trainval2017.zip