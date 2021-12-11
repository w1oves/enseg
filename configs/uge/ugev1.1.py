_base_ = [
    "../base/datasets/nightcity_h256w512.py",
    "../base/default_runtime.py",
    "../base/models/ugev1.py",
    "../base/schedules/schedule_80k.py"
]

network=dict(
    loss_regular=None,
)