import sys
import json
import os

if len(sys.argv) > 1:
	train_json_path = sys.argv[1]

elif os.path.isdir("./data/coco/annotations/instances_train2017.json"):
	
	train_json_path = "./data/coco/annotations/instances_train2017.json"

else:
	print("File cannot be located")
	sys.exit()



with open(train_json_path) as file_path:
		print("Loading json file...")
		data = json.load(file_path)


categories = data["categories"]

with open("class_id_name.txt", "w") as file:
	for entries in categories:
		file.write(str(entries["id"]))
		file.write(":")
		file.write(entries["name"])
		file.write("\n")

print("Text file generated.")