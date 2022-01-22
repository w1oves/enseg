_base_ = [
    "../base/models/upernet_swin.py",
    "../base/datasets/nightcity_h256w512.py",
    "../base/default_runtime.py",
    "../base/schedules/schedule_80k.py",
]
network = dict(
    pretrained="/home/wzx/weizhixiang/ensegment/pretrain/swin/mmlab/swin_base_patch4_window7_224_22k.pth",
    backbone=dict(
        pretrain_img_size=224,
        embed_dims=128,
        depths=[2, 2, 18, 2],
        num_heads=[4, 8, 16, 32],
    ),
    seg=dict(in_channels=[128, 256, 512, 1024], num_classes=19),
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
