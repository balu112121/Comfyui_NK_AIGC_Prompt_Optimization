# 南光AI一键负面提示词 – ComfyUI 插件

## ✨ 功能简介
- 根据正向提示词**一键生成**高质量负面提示词。
- **三种生成模式**：简易规则、专业规则、Ollama智能（模型根据基础模型自动选择）。
- **完整参数控制**：增强负面、随机强度、基础模型（支持 SD1.5, SDXL, SD3, FLUX1.0, FLUX2.0, QWEN-IMAGE, Z-IMAGE, WAN）、随机种、生成后控制。
- **全中文界面**，即插即用。

## 📦 安装方法
1. 将 `Comfyui_NK_AIGC_Prompt_Optimization` 文件夹放入 `ComfyUI/custom_nodes/`。
2. 重启 ComfyUI 或刷新浏览器。
3. 在节点菜单 **南光AI/提示词** 中找到 **南光AI一键负面提示词**。

## 🧩 参数说明
| 参数 | 说明 |
|:---|:---|
| **正向提示词** | 输入你的正向提示词（支持多行） |
| **生成模式** | 简易规则 / 专业规则 / Ollama智能 |
| **增强负面** | 0~1，追加极端负面词（如 extremely ugly） |
| **随机强度** | 0~1，从词库随机抽取额外负面词 |
| **基础模型** | 下拉选择：SD1.5, SDXL, SD3, FLUX1.0, FLUX2.0, QWEN-IMAGE, Z-IMAGE, WAN |
| **随机种** | -1随机，≥0固定 |
| **生成后控制** | randomize（打乱+变体）/ fixed（排序去重）/ none |

## 🚀 使用示例

### 南光AIGC绘画

南光AIGC-AIGC全能方案设计解决专家 VX:nankodesign2001

RH新人注册---
粉丝福利：https://pre.runninghub.cn/?inviteCode=t7ztfeiw-填入邀请码，领1000RH币，每天登录还有100币 邀请码：t7ztfeiw

仙宫云新人注册---
https://www.xiangongyun.com/register/MJAT43 新人注册仙宫云送5元代金券， 填写邀请码（输入我们的邀请码：MJAT43 ）还额外送3元代金券 完成后可以得到仙宫云8元账户余额，可以免费带你玩转5小时发高配4090 D显卡AIGC绘画。

DESIGN-AI新人注册---
DESIGN-AI神器-AI时代的设计生产力工具   https://d.design/?sharecode=_EhTWOtyEe；注册可获得现金奖励！

### 三大自媒体平台

小红书
https://www.xiaohongshu.com/user/profile/5fe63b41000000000100811d?m_source=itab

抖音
https://www.douyin.com/user/self?showTab=post

bilibili（B站）
https://space.bilibili.com/404783526


### 如果您受益于本项目，不妨请作者喝杯咖啡，您的支持是我最大的动力

<div style="display: flex; justify-content: left; gap: 20px;">
    <img src="https://github.com/balu112121/ComfyUI_NanKo_AI_Recognize/blob/main/Alipay.jpg" width="300" alt="支付宝收款码">
    <img src="https://github.com/balu112121/ComfyUI_NanKo_AI_Recognize/blob/main/WeChat.jpg" width="300" alt="微信收款码">
</div>

# 商务合作
如果您有定制工作流/节点的需求，或者想要学习插件制作的相关课程，请联系我
wechat:nankodesign2001