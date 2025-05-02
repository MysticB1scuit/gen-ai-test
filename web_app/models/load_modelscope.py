from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys
from modelscope.utils.constant import Tasks
from modelscope.hub.snapshot_download import snapshot_download
import torch
import os

def load_video_model():
    torch.manual_seed(42)

    model_dir = snapshot_download('damo/text-to-video-synthesis', revision='v1.1.0')

    pipe = pipeline(
        task=Tasks.text_to_video_synthesis,
        model=model_dir,
        model_revision='v1.1.0',
    )

    try:
        transformer_layers = pipe.model.clip_encoder.model.transformer.resblocks
        for layer in transformer_layers:
            original_forward = layer.attn.forward

            def patched_forward(*args, **kwargs):
                kwargs["attn_mask"] = None
                return original_forward(*args, **kwargs)

            layer.attn.forward = patched_forward

        print("[PATCH] Successfully patched all transformer layers to disable attn_mask")

    except Exception as e:
        print(f"[ERROR] Failed to patch transformer layers: {e}")
    
    print("[INFO] Using device:", "cuda" if torch.cuda.is_available() else "cpu")

    return pipe