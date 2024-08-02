
## Training

For pretraining the backbone edit [simclr.yaml](scripts/pretrain/custom/simclr.yaml) Mainly update the train_path 
``
train_path: "/PATH/TO/DATASET/images" #remember to link only the images folder since this is no label training
``

python3 main_pretrain.py \
    # path to training script folder
    --config-path scripts/pretrain/custom/ \
    # training config name
    --config-name simclr.yaml
    # add new arguments (e.g. those not defined in the yaml files)
    # by doing ++new_argument=VALUE
    # pytorch lightning's arguments can be added here as well.
```
