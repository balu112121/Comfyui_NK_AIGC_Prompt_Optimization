"""
南光AI一键负面提示词 - ComfyUI 插件
注册节点到 ComfyUI
"""
from .node import NK_AIGC_Prompt_Optimization

NODE_CLASS_MAPPINGS = {
    "NK_AIGC_Prompt_Optimization": NK_AIGC_Prompt_Optimization,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NK_AIGC_Prompt_Optimization": "南光AI一键负面提示词",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]