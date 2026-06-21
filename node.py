"""
南光AI一键负面提示词 – 增强版
支持三种生成模式：简易规则、专业规则、Ollama智能（动态选择模型）
包含参数：增强负面、随机强度、基础模型、随机种、生成后控制
"""
import random
import re

class NK_AIGC_Prompt_Optimization:
    NODE_DISPLAY_NAME = "南光AI一键负面提示词"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "正向提示词": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "请输入正向提示词..."
                }),
                "生成模式": (["简易规则", "专业规则", "Ollama智能"], {
                    "default": "简易规则",
                    "tooltip": "选择负面提示词的生成策略"
                }),
                "增强负面": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 1,
                    "step": 0.1,
                    "tooltip": "负面词强度增强系数（0为不增强，1为最强）"
                }),
                "随机强度": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 1,
                    "step": 0.1,
                    "tooltip": "随机抽取额外负面词的比例"
                }),
                # ---------- 基础模型下拉列表（已更新） ----------
                "基础模型": (["SD1.5", "SDXL", "SD3", "FLUX1.0", "FLUX2.0", "QWEN-IMAGE", "Z-IMAGE", "WAN"], {
                    "default": "SD1.5",
                    "tooltip": "选择使用的基础模型，不同模型对负面词敏感度不同"
                }),
                "随机种": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": 0xFFFFFFFF,
                    "tooltip": "随机种子，-1表示完全随机，0及以上为固定种子"
                }),
                "生成后控制": (["randomize", "fixed", "none"], {
                    "default": "randomize",
                    "tooltip": "生成后处理方式：randomize=随机排序/变体, fixed=固定格式, none=不加额外处理"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("负向提示词",)
    FUNCTION = "生成负向提示词"
    CATEGORY = "南光AI/提示词"

    # ------------------- 基础通用负面词库 -------------------
    BASE_NEGATIVE = (
        "worst quality, low quality, normal quality, lowres, blurry, ugly, wrong, bad, "
        "deformed, mutated, disfigured, poorly drawn, bad anatomy, bad proportions, "
        "extra limbs, cloned face, gross proportions, malformed limbs, missing arms, "
        "missing legs, extra arms, extra legs, fused fingers, too many fingers, "
        "long neck, bad hands, bad feet, bad body, bad perspective, bad lighting"
    )

    # 专业规则额外词库（更全面）
    PRO_EXTRAS = {
        "face": "bad face, bad eyes, bad mouth, bad nose, asymmetrical face, ugly face",
        "hand": "bad hands, bad fingers, fused fingers, too many fingers, missing fingers",
        "body": "bad body, bad proportions, malformed limbs, extra limbs, unnatural pose",
        "animal": "bad animal anatomy, deformed animal, wrong proportions animal",
        "car": "bad vehicle, distorted car, wrong proportions car",
        "landscape": "bad perspective, distorted background, unnatural scene, flat depth",
        "clothing": "bad clothing, wrinkled fabric, wrong texture, cheap fabric",
        "hair": "bad hair, unrealistic hair, messy hair, straw hair",
        "skin": "bad skin, wrong skin tone, unhealthy skin, plastic skin",
        "building": "bad architecture, distorted building, wrong proportions building",
        "food": "bad food, unrealistic texture, wrong color, stale food",
        "art": "amateur art, beginner art, bad composition, cluttered, noisy",
        "color": "bad color, washed out, oversaturated, wrong hue",
        "light": "bad lighting, harsh shadows, overexposed, underexposed, flat lighting",
        "detail": "missing details, oversimplified, low detail, rough edges"
    }

    # 增强负面词库（随增强系数增加而追加）
    ENHANCE_TERMS = [
        "extremely ugly", "horrible", "terrible", "distorted", "grotesque",
        "unrecognizable", "poorly rendered", "worst ever", "hideous"
    ]

    # 随机后缀池（用于生成后控制 randomize）
    RANDOM_SUFFIXES = [
        "unpleasant", "unappealing", "undesirable", "flawed", "imperfect",
        "substandard", "inferior", "unsightly", "repulsive"
    ]

    # ------------------- 核心生成函数 -------------------
    def 生成负向提示词(
        self,
        正向提示词,
        生成模式,
        增强负面,
        随机强度,
        基础模型,
        随机种,
        生成后控制
    ):
        # 1. 根据模式生成基础负面词
        if 生成模式 == "简易规则":
            negative = self._generate_simple(正向提示词)
        elif 生成模式 == "专业规则":
            negative = self._generate_professional(正向提示词, 基础模型)
        elif 生成模式 == "Ollama智能":
            negative = self._generate_ollama(正向提示词, 基础模型)  # 传入基础模型
        else:
            negative = self.BASE_NEGATIVE

        # 2. 应用「增强负面」参数
        if 增强负面 > 0:
            enhance_count = max(1, int(len(self.ENHANCE_TERMS) * 增强负面))
            seed = 随机种 if 随机种 >= 0 else random.randint(0, 999999)
            rng = random.Random(seed + 999)
            selected_enhance = rng.sample(self.ENHANCE_TERMS, min(enhance_count, len(self.ENHANCE_TERMS)))
            negative += ", " + ", ".join(selected_enhance)

        # 3. 应用「随机强度」参数
        if 随机强度 > 0:
            all_pro_terms = []
            for v in self.PRO_EXTRAS.values():
                all_pro_terms.extend([t.strip() for t in v.split(",")])
            unique_terms = list(set(all_pro_terms))
            sample_size = max(1, int(len(unique_terms) * 随机强度 * 0.3))
            seed2 = 随机种 if 随机种 >= 0 else random.randint(0, 999999)
            rng2 = random.Random(seed2 + 888)
            selected_random = rng2.sample(unique_terms, min(sample_size, len(unique_terms)))
            if selected_random:
                negative += ", " + ", ".join(selected_random)

        # 4. 应用「生成后控制」
        if 生成后控制 == "randomize":
            parts = [p.strip() for p in negative.split(",") if p.strip()]
            seed3 = 随机种 if 随机种 >= 0 else random.randint(0, 999999)
            rng3 = random.Random(seed3 + 777)
            rng3.shuffle(parts)
            suffix = rng3.choice(self.RANDOM_SUFFIXES)
            parts.append(suffix)
            negative = ", ".join(parts)
        elif 生成后控制 == "fixed":
            parts = [p.strip() for p in negative.split(",") if p.strip()]
            parts = sorted(set(parts))
            negative = ", ".join(parts)

        # 最终去重
        final_parts = [p.strip() for p in negative.split(",") if p.strip()]
        final_unique = []
        seen = set()
        for p in final_parts:
            if p not in seen:
                final_unique.append(p)
                seen.add(p)
        final_negative = ", ".join(final_unique)

        return (final_negative,)

    # ---------- 简易规则 ----------
    def _generate_simple(self, prompt):
        if not prompt or not prompt.strip():
            return self.BASE_NEGATIVE
        prompt_lower = prompt.lower()
        extras = []
        if any(w in prompt_lower for w in ["face", "head", "eye", "mouth", "nose"]):
            extras.append("bad face, bad eyes, bad mouth, bad nose")
        if any(w in prompt_lower for w in ["hand", "finger", "palm"]):
            extras.append("bad hands, bad fingers, fused fingers, too many fingers")
        if any(w in prompt_lower for w in ["body", "figure", "torso", "leg", "arm"]):
            extras.append("bad body, bad proportions, malformed limbs, extra limbs")
        if any(w in prompt_lower for w in ["animal", "cat", "dog", "bird", "fish", "horse"]):
            extras.append("bad animal anatomy, deformed animal")
        if any(w in prompt_lower for w in ["car", "vehicle", "truck", "motorcycle", "bicycle"]):
            extras.append("bad vehicle, distorted car, wrong proportions")
        if any(w in prompt_lower for w in ["landscape", "scene", "background", "environment"]):
            extras.append("bad perspective, distorted background, unnatural scene")
        if any(w in prompt_lower for w in ["clothing", "dress", "shirt", "pants", "skirt"]):
            extras.append("bad clothing, wrinkled fabric, wrong texture")
        if any(w in prompt_lower for w in ["hair", "hairstyle"]):
            extras.append("bad hair, unrealistic hair, messy hair")
        if any(w in prompt_lower for w in ["skin", "complexion"]):
            extras.append("bad skin, wrong skin tone, unhealthy skin")
        if any(w in prompt_lower for w in ["building", "house", "architecture", "city"]):
            extras.append("bad architecture, distorted building, wrong proportions")
        if any(w in prompt_lower for w in ["food", "meal", "dish", "fruit", "vegetable"]):
            extras.append("bad food, unrealistic texture, wrong color")
        combined = ", ".join([self.BASE_NEGATIVE] + extras)
        return combined

    # ---------- 专业规则 ----------
    def _generate_professional(self, prompt, base_model):
        if not prompt or not prompt.strip():
            return self.BASE_NEGATIVE
        prompt_lower = prompt.lower()
        extras = []

        for key, value in self.PRO_EXTRAS.items():
            if key in prompt_lower:
                extras.append(value)

        # 根据基础模型添加特定的负面词（新增模型暂不特殊处理，走默认）
        if base_model == "SDXL":
            extras.append("low quality, worst quality, bad quality, jpeg artifacts, ugly, deformed")
        elif base_model == "SD3":
            extras.append("bad anatomy, bad hands, bad feet, extra digits, fused digits, missing digits")
        elif base_model == "SD1.5":
            extras.append("blurry, lowres, normal quality, worst quality, ugly")
        # 对于 FLUX, QWEN-IMAGE, Z-IMAGE, WAN 等，暂不加特定词，可后续扩展

        extras.append("bad composition, unbalanced, cluttered, no focus, boring")
        combined = ", ".join([self.BASE_NEGATIVE] + extras)
        return combined

    # ---------- Ollama 智能（动态选择模型） ----------
    def _generate_ollama(self, prompt, base_model):
        try:
            import requests
        except ImportError:
            print("[南光AI] 未安装 requests 库，回退到专业规则")
            return self._generate_professional(prompt, "SD1.5")

        if not prompt or not prompt.strip():
            return self.BASE_NEGATIVE

        # 根据基础模型选择 Ollama 模型（仅 SDXL 特殊，其余使用 llama3.2:3b）
        if base_model == "SDXL":
            ollama_model = "qwen:7b"
        else:
            ollama_model = "llama3.2:3b"

        try:
            system_prompt = (
                "你是一个Stable Diffusion提示词专家。请根据用户提供的正向提示词，生成一个英文负面提示词。"
                "只输出负面提示词本身，不要包含任何解释、括号或额外文字。"
                "负面提示词应该包含通用的画质缺陷词，以及针对该主题可能出现的具体缺陷词。"
                "使用英文，用逗号分隔。"
            )
            user_prompt = f"正向提示词: {prompt}\n\n生成的负面提示词:"

            payload = {
                "model": ollama_model,
                "prompt": f"{system_prompt}\n{user_prompt}",
                "stream": False,
                "options": {
                    "num_predict": 256,
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            }

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                result = re.sub(r'^["\']|["\']$', '', result)
                result = re.sub(r'[^\x00-\x7F]+', '', result)
                if result:
                    parts = [p.strip() for p in result.split(",") if p.strip()]
                    if parts:
                        return ", ".join(parts)
                return self._generate_professional(prompt, "SD1.5")
            else:
                print(f"[南光AI] Ollama 请求失败 ({response.status_code})，回退到专业规则")
                return self._generate_professional(prompt, "SD1.5")

        except requests.exceptions.ConnectionError:
            print("[南光AI] 无法连接 Ollama 服务 (http://localhost:11434)，请确保 Ollama 已启动。回退到专业规则。")
            return self._generate_professional(prompt, "SD1.5")
        except Exception as e:
            print(f"[南光AI] Ollama 调用异常: {e}，回退到专业规则")
            return self._generate_professional(prompt, "SD1.5")