from typing import Dict

import torch.nn as nn
from enseg.core import add_prefix
from enseg.models import builder
from mmcv.runner import build_optimizer
from mmcv.runner.fp16_utils import auto_fp16
from torch.nn.parallel.distributed import _find_tensors

from ..builder import NETWORKS, TRANSLATOR, build_loss
from ..segmentors import EncoderDecoder
from enseg.core import add_prefix


@NETWORKS.register_module()
class UGEV1(EncoderDecoder):
    def __init__(
        self,
        seg,
        gen,
        rec,
        pretrained=None,
        train_cfg=None,
        test_cfg=None,
        init_cfg=None,
    ):
        assert isinstance(seg, dict)
        super().__init__(
            seg["encode"],
            seg["decode"],
            seg.get("aux", None),
            seg.get("neck", None),
            pretrained,
            train_cfg,
            test_cfg,
            init_cfg,
        )
        # self._seg_is_fixed = not seg["need_train"]
        self.gen = builder.build_translator(gen)
        if rec is not None:
            self._rec_accept_img = rec.pop("accept_img")
            self.rec = builder.build_translator(rec)
        else:
            self._rec_accept_img = []

    def train_step(self, data_batch, optimizer, ddp_reducer=None, **kwargs):
        dataA = data_batch
        low_img = dataA["img"]
        img_metas = dataA["img_metas"]
        gt_semantic_seg = dataA["gt_semantic_seg"]
        norm_cfg = img_metas[0]["img_norm_cfg"]
        losses_total = dict()
        optional_visuals = dict()
        # forward
        self._optim_zero(optimizer, "seg", "backbone", "gen", "rec")
        losses_gen, light_img = self.gen.forward_train(low_img, norm_cfg)
        losses_total.update(add_prefix(losses_gen, "gen"))
        losses_seg, seg_logits = self._seg_forward_train(
            self.extract_feat(light_img), img_metas, gt_semantic_seg
        )
        losses_total.update(losses_seg)
        if "low" in self._rec_accept_img:
            losses_rec_light, rec_light = self.rec.forward_train(light_img, norm_cfg)
            losses_total.update(add_prefix(losses_rec_light, "rec_light"))
            optional_visuals["photo/rec_light_img"] = rec_light
        if "light" in self._rec_accept_img:
            losses_rec_low, rec_low = self.rec.forward_train(low_img, norm_cfg)
            losses_total.update(add_prefix(losses_rec_low, "rec_low"))
            optional_visuals["photo/rec_low_img"] = rec_low
        loss_total, vars_total = self._parse_losses(losses_total)
        if ddp_reducer is not None:
            ddp_reducer.prepare_for_backward(_find_tensors(loss_total))
        loss_total.backward()
        self._optim_step(optimizer, "seg", "backbone", "gen", "rec")
        outputs = dict(
            loss=loss_total, log_vars=vars_total, num_samples=len(dataA["img_metas"]),
        )
        outputs["visual"] = {
            "photo/low": low_img,
            "photo/light": light_img,
            "seg/low": low_img,
            "seg/logits": seg_logits,
            "seg/gt": gt_semantic_seg,
            "img_metas": img_metas,
        }
        outputs["visual"].update(optional_visuals)

        for photo_name in outputs["visual"]:
            if photo_name == "img_metas":
                continue
            outputs["visual"][photo_name] = outputs["visual"][photo_name][0].detach()
        return outputs

    @staticmethod
    def _optim_zero(optims, *names):
        for name in names:
            if name in optims:
                optims[name].zero_grad()

    @staticmethod
    def _optim_step(optims, *names):
        for name in names:
            if name in optims:
                optims[name].step()

    def _seg_forward_train(self, x, img_metas, gt_semantic_seg):
        """Run forward function and calculate loss for decode head in
        training."""
        losses = dict()
        loss_decode, seg_logits = self.seg.forward_train(
            x, img_metas, gt_semantic_seg, self.train_cfg, output_pred=True
        )

        losses.update(add_prefix(loss_decode, "decode"))
        return losses, seg_logits

    def encode_decode(self, img, img_metas):
        img = self.gen(img, img_metas[0]["img_norm_cfg"])
        return super().encode_decode(img, img_metas)
