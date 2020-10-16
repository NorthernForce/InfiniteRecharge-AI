# Training tfRecords:
**Note:** training should be done on a computer with reasonably powerful GPU(s). Images should be limited in size (400x300 or so) to avoid maxing out the Jetson's RAM.  

**Important:** Before training, run the changeXMLImagePaths.py file (with an updated path) to ensure the XML files can be found.  
Limit images to 2000x1500 or less on a computer with 16GB of RAM for stable training. Close all other background tasks.  
`$ cd /home/dlinano/nvdli-nano/models/resources`  
`$ python3 xml_to_csv.py`  

CSV files end up in `../data`  

`$ cd ../research`  
`$ sudo python3 setup.py install`  

`$ cd ../resources`  

Remember to change the path to images in the generate_tfrecord.py file.  
If adding more classes, modify this file before running. Remember to add to the if statement.  
`$ python3 generate_tfrecord.py --csv_input=../data/train_labels.csv --output_path=../data/train.record`  
`$ python3 generate_tfrecord.py --csv_input=../data/test_labels.csv --output_path=../data/test.record`  

**IMPORANT:** delete everything in the training folder *except* object-detection.pbtxt, ssd_mobilenet_v1_pets.config *and* any checkpoint files that you may want to keep training your model further in the future (if you have compatible checkpoint files, the training script will resume from the latest file).  
This command begins training. Once average loss < 1.5ish then **Ctrl + C** will stop the training (Ideally loss less than 1):  
`$ cd ../research/object_detection/legacy`  
`$ python3 train.py --logtostderr --train_dir=../../../training --pipeline_config_path=../../../training/ssd_mobilenet_v1_pets.config`  


**After training:**  
make sure to change `model.ckpt-#####` in the command below to the latest checkpoint in `../training` folder  
`$ cd /home/dlinano/nvdli-nano/models/research/object_detection`  
```
$ python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path ../../training/ssd_mobilenet_v1_pets.config \
    --trained_checkpoint_prefix ../../training/model.ckpt-##### \
    --output_directory ../../powercell_graph
```
