# %%
import torch
import torch.nn as nn
from torchvision.models import resnet18, resnet50

# from solo.utils.backbones import (
#     swin_base,
#     swin_large,
#     swin_small,
#     swin_tiny,
#     vit_base,
#     vit_large,
#     vit_small,
#     vit_tiny,
# )

from solo.data.classification_dataloader import prepare_data

# change this if you wanna load a different model
my_backbone = "resnet18"

backbone_model = {
    "resnet18": resnet18,
    "resnet50": resnet50
}[my_backbone]

# initialize backbone
kwargs = {
    "cifar": False,  # <-- change this if you are running on cifar
    # "img_size": 224,  # <-- uncomment this when using vit/swin
    # "patch_size": 16,  # <-- uncomment this when using vit
}
cifar = kwargs.pop("cifar", False)
# swin specific
if "swin" in my_backbone and cifar:
    kwargs["window_size"] = 4

model = backbone_model(**kwargs)
if "resnet" in my_backbone:
    # remove fc layer
    model.fc = nn.Identity()
    if cifar:
        model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=2, bias=False)
        model.maxpool = nn.Identity()

ckpt_path = "/glb/hou/pt.sgs/data/ml_ai_us/uspcjc/codes/solo-learn/trained_models/simclr/ms1uc4fi/simclr-topsalt-ms1uc4fi-ep=10.ckpt"

state = torch.load(ckpt_path)["state_dict"]
for k in list(state.keys()):
    if "backbone" in k:
        state[k.replace("backbone.", "")] = state[k]
    del state[k]
model.load_state_dict(state, strict=False)

print(f"loaded {ckpt_path}")


train_loader, val_loader = prepare_data(
    dataset= "custom",
    train_data_path="/lus231/ua/export/saltcrawler/uspcjc/simclr_dataset",
    val_data_path="/lus231/ua/export/saltcrawler/uspcjc/simclr_val",
    batch_size=64,
    num_workers=4,
)

from solo.utils.auto_umap import OfflineUMAP

umap = OfflineUMAP()

# move model to the gpu
device = "cuda:0"
model = model.to(device)

# umap.plot(device, model, train_loader, 'im100_train_umap.pdf')
umap.plot(device, model, val_loader, 'im100_val_umap.pdf')