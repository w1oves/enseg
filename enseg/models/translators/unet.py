import torch.nn as nn
from mmcv.cnn import ConvModule, build_conv_layer
from mmcv.runner import load_checkpoint
from .modules import UnetSkipConnectionBlock, generation_init_weights
from ..builder import TRANSLATOR
from enseg.utils import get_root_logger
import torch


@TRANSLATOR.register_module()
class UnetGenerator(nn.Module):
    """Construct the Unet-based generator from the innermost layer to the
    outermost layer, which is a recursive process.

    Args:
        in_channels (int): Number of channels in input images.
        out_channels (int): Number of channels in output images.
        num_down (int): Number of downsamplings in Unet. If `num_down` is 8,
            the image with size 256x256 will become 1x1 at the bottleneck.
            Default: 8.
        base_channels (int): Number of channels at the last conv layer.
            Default: 64.
        norm_cfg (dict): Config dict to build norm layer. Default:
            `dict(type='BN')`.
        use_dropout (bool): Whether to use dropout layers. Default: False.
        init_cfg (dict): Config dict for initialization.
            `type`: The name of our initialization method. Default: 'normal'.
            `gain`: Scaling factor for normal, xavier and orthogonal.
            Default: 0.02.
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        num_down=8,
        base_channels=64,
        norm_cfg=dict(type="BN"),
        use_dropout=False,
        skip=0.0,
        noise_std=0.1,
        init_cfg=dict(type="normal", gain=0.02),
    ):
        super().__init__()
        # We use norm layers in the unet generator.
        assert isinstance(norm_cfg, dict), (
            "'norm_cfg' should be dict, but" f"got {type(norm_cfg)}"
        )
        assert "type" in norm_cfg, "'norm_cfg' must have key 'type'"
        self.skip = skip
        self.noise_std = noise_std
        self.add_noise_flag = False
        # add the innermost layer
        unet_block = UnetSkipConnectionBlock(
            base_channels * 8,
            base_channels * 8,
            in_channels=None,
            submodule=None,
            norm_cfg=norm_cfg,
            is_innermost=True,
        )
        # add intermediate layers with base_channels * 8 filters
        for _ in range(num_down - 5):
            unet_block = UnetSkipConnectionBlock(
                base_channels * 8,
                base_channels * 8,
                in_channels=None,
                submodule=unet_block,
                norm_cfg=norm_cfg,
                use_dropout=use_dropout,
            )
        # gradually reduce the number of filters
        # from base_channels * 8 to base_channels
        unet_block = UnetSkipConnectionBlock(
            base_channels * 4,
            base_channels * 8,
            in_channels=None,
            submodule=unet_block,
            norm_cfg=norm_cfg,
        )
        unet_block = UnetSkipConnectionBlock(
            base_channels * 2,
            base_channels * 4,
            in_channels=None,
            submodule=unet_block,
            norm_cfg=norm_cfg,
        )
        unet_block = UnetSkipConnectionBlock(
            base_channels,
            base_channels * 2,
            in_channels=None,
            submodule=unet_block,
            norm_cfg=norm_cfg,
        )
        # add the outermost layer
        self.model = UnetSkipConnectionBlock(
            out_channels,
            base_channels,
            in_channels=in_channels,
            submodule=unet_block,
            is_outermost=True,
            norm_cfg=norm_cfg,
        )

        self.init_type = (
            "normal" if init_cfg is None else init_cfg.get("type", "normal")
        )
        self.init_gain = 0.02 if init_cfg is None else init_cfg.get("gain", 0.02)

    def eval(self):
        self.add_noise_flag = False
        return super().eval()

    def train(self, mode: bool = True):
        if mode:
            self.add_noise_flag = True
        return super().train(mode=mode)

    def forward(self, x):
        x = self.model(x) + self.skip * x
        if self.add_noise_flag:
            x = x + torch.randn_like(x) * self.noise_std
        x = torch.clip(x, -1, 1)
        return x

    def init_weights(self, pretrained=None, strict=True):
        """Initialize weights for the model.

        Args:
            pretrained (str, optional): Path for pretrained weights. If given
                None, pretrained weights will not be loaded. Default: None.
            strict (bool, optional): Whether to allow different params for the
                model and checkpoint. Default: True.
        """
        if isinstance(pretrained, str):
            logger = get_root_logger()
            load_checkpoint(self, pretrained, strict=strict, logger=logger)
        elif pretrained is None:
            generation_init_weights(
                self, init_type=self.init_type, init_gain=self.init_gain
            )
        else:
            raise TypeError(
                "'pretrained' must be a str or None. "
                f"But received {type(pretrained)}."
            )
