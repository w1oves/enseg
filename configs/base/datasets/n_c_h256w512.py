# dataset settings
dataset_type = "UnpairedDataset"
data_root = "/home/wzx/weizhixiang/ensegment/data/enseg/nightcity"
aux_type = "CityscapesDataset"
aux_root = "/home/wzx/weizhixiang/ensegment/data/enseg/cityscape"
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True
)
# img_norm_cfg = dict(
#     mean=[63.324, 56.269, 51.215], std=[42.391, 40.951, 39.013], to_rgb=True
# )
crop_size = (256, 512)
train_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(type="LoadAnnotations"),
    dict(type="Resize", img_scale=(1024, 512), ratio_range=(0.5, 2.0)),
    dict(type="RandomCrop", crop_size=crop_size, cat_max_ratio=0.75),
    dict(type="RandomFlip", prob=0.5),
    dict(type="PhotoMetricDistortion"),
    dict(type="Normalize", **img_norm_cfg),
    dict(type="Pad", size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type="DefaultFormatBundle"),
    dict(type="Collect", keys=["img", "gt_semantic_seg"]),
]
test_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(
        type="MultiScaleFlipAug",
        img_scale=(1024, 512),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type="Resize", keep_ratio=True),
            dict(type="RandomFlip"),
            dict(type="Normalize", **img_norm_cfg),
            dict(type="ImageToTensor", keys=["img"]),
            dict(type="Collect", keys=["img"]),
        ],
    ),
]
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir="image/train",
        ann_dir="label/train",
        pipeline=train_pipeline,
        aux_dataset=dict(
            type=aux_type,
            data_root=aux_root,
            img_dir="image/train",
            ann_dir="label/train",
            pipeline=train_pipeline,
        ),
    ),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir="image/val",
        ann_dir="label/val",
        pipeline=test_pipeline,
        aux_dataset=dict(
            type=aux_type,
            data_root=aux_root,
            img_dir="image/val",
            ann_dir="label/val",
            pipeline=test_pipeline,
        ),
    ),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir="image/test",
        ann_dir="label/test",
        pipeline=test_pipeline,
        aux_dataset=dict(
            type=aux_type,
            data_root=aux_root,
            img_dir="image/test",
            ann_dir="label/test",
            pipeline=test_pipeline,
        ),
    ),
)






























'''###____pretty_text____###'''



'''
dataset_type = 'UnpairedDataset'
data_root = '/home/wzx/weizhixiang/ensegment/data/enseg/nightcity'
aux_type = 'CityscapesDataset'
aux_root = '/home/wzx/weizhixiang/ensegment/data/enseg/cityscape'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
crop_size = (256, 512)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(type='Resize', img_scale=(1024, 512), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=(256, 512), cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size=(256, 512), pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1024, 512),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=4,
    train=dict(
        type='UnpairedDataset',
        data_root='/home/wzx/weizhixiang/ensegment/data/enseg/nightcity',
        img_dir='image/train',
        ann_dir='label/train',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations'),
            dict(type='Resize', img_scale=(1024, 512), ratio_range=(0.5, 2.0)),
            dict(type='RandomCrop', crop_size=(256, 512), cat_max_ratio=0.75),
            dict(type='RandomFlip', prob=0.5),
            dict(type='PhotoMetricDistortion'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size=(256, 512), pad_val=0, seg_pad_val=255),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img', 'gt_semantic_seg'])
        ],
        aux_dataset=dict(
            type='CityscapesDataset',
            data_root='/home/wzx/weizhixiang/ensegment/data/enseg/cityscape',
            img_dir='image/train',
            ann_dir='label/train',
            pipeline=[
                dict(type='LoadImageFromFile'),
                dict(type='LoadAnnotations'),
                dict(
                    type='Resize',
                    img_scale=(1024, 512),
                    ratio_range=(0.5, 2.0)),
                dict(
                    type='RandomCrop',
                    crop_size=(256, 512),
                    cat_max_ratio=0.75),
                dict(type='RandomFlip', prob=0.5),
                dict(type='PhotoMetricDistortion'),
                dict(
                    type='Normalize',
                    mean=[123.675, 116.28, 103.53],
                    std=[58.395, 57.12, 57.375],
                    to_rgb=True),
                dict(type='Pad', size=(256, 512), pad_val=0, seg_pad_val=255),
                dict(type='DefaultFormatBundle'),
                dict(type='Collect', keys=['img', 'gt_semantic_seg'])
            ])),
    val=dict(
        type='UnpairedDataset',
        data_root='/home/wzx/weizhixiang/ensegment/data/enseg/nightcity',
        img_dir='image/val',
        ann_dir='label/val',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1024, 512),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ],
        aux_dataset=dict(
            type='CityscapesDataset',
            data_root='/home/wzx/weizhixiang/ensegment/data/enseg/cityscape',
            img_dir='image/val',
            ann_dir='label/val',
            pipeline=[
                dict(type='LoadImageFromFile'),
                dict(
                    type='MultiScaleFlipAug',
                    img_scale=(1024, 512),
                    flip=False,
                    transforms=[
                        dict(type='Resize', keep_ratio=True),
                        dict(type='RandomFlip'),
                        dict(
                            type='Normalize',
                            mean=[123.675, 116.28, 103.53],
                            std=[58.395, 57.12, 57.375],
                            to_rgb=True),
                        dict(type='ImageToTensor', keys=['img']),
                        dict(type='Collect', keys=['img'])
                    ])
            ])),
    test=dict(
        type='UnpairedDataset',
        data_root='/home/wzx/weizhixiang/ensegment/data/enseg/nightcity',
        img_dir='image/test',
        ann_dir='label/test',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1024, 512),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ],
        aux_dataset=dict(
            type='CityscapesDataset',
            data_root='/home/wzx/weizhixiang/ensegment/data/enseg/cityscape',
            img_dir='image/test',
            ann_dir='label/test',
            pipeline=[
                dict(type='LoadImageFromFile'),
                dict(
                    type='MultiScaleFlipAug',
                    img_scale=(1024, 512),
                    flip=False,
                    transforms=[
                        dict(type='Resize', keep_ratio=True),
                        dict(type='RandomFlip'),
                        dict(
                            type='Normalize',
                            mean=[123.675, 116.28, 103.53],
                            std=[58.395, 57.12, 57.375],
                            to_rgb=True),
                        dict(type='ImageToTensor', keys=['img']),
                        dict(type='Collect', keys=['img'])
                    ])
            ])))
'''
