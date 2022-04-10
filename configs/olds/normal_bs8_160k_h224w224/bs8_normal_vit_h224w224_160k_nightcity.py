_base_ = [
    "../base/models/upernet_vit-b16_ln_mln.py",
    "../base/datasets/nightcity_h224w224.py",
    "../base/default_runtime.py",
    "../base/schedules/schedule_160k.py",
]
network = dict(
    pretrained="/home/wzx/weizhixiang/ensegment/pretrain/vit/mmlab/jx_vit_base_p16_224-80ecf9dd.pth",
    seg=dict(num_classes=19),
    backbone=dict(
        img_size=(224, 224),
    ),
)
lr_config = dict(
    _delete_=True,
    policy="poly",
    warmup="linear",
    warmup_iters=1500,
    warmup_ratio=1e-6,
    power=1.0,
    min_lr=0.0,
    by_epoch=False,
)
data = dict(samples_per_gpu=8, workers_per_gpu=8)
optimizer = dict(backbone=dict(lr=0.00048), seg=dict(lr=0.00048))





'''###____pretty_text____###'''



'''
False to Parse'''
