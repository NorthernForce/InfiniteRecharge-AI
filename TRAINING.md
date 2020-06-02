# Training tfRecords:
**Note:** training should be done on a computer with reasonably powerful GPUs. Images should be limited in size (800x600 or so) to avoid maxing out the Jetson's RAM.  
Limit images to 4000x3000 on a computer with 16GB of RAM for successful training. Close all other background tasks.  
`$ cd /home/dlinano/nvdli-nano/models/resources`  
`$ python3 xml_to_csv.py`  

csv files end up in `../data`  

`$ cd ../research`  
`$ sudo python3 setup.py install`  

`$ cd ../resources`  

if adding more classes, modify this file before running. Remember to add to the if statement.  
`$ python3 generate_tfrecord.py --csv_input=../data/train_labels.csv --output_path=../data/train.record`
`$ python3 generate_tfrecord.py --csv_input=../data/test_labels.csv --output_path=../data/test.record`

**IMPORANT:** delete everything in the training folder *except* object-detection.pbtxt and ssd_mobilenet_v1_pets.config:  
this command begins training. Once average loss < 1.5ish then **Ctrl + C** will stop the training (Ideally loss less than 1):  
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