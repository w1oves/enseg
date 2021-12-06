_base_ = [
    "../base/datasets/n_c_h385w385.py",
    "../base/default_runtime.py",
    "../base/models/ensegv3.py",
    "../base/schedules/schedule_80k.py",
]

data = dict(samples_per_gpu=4, workers_per_gpu=2)

