"""Core analysis pipeline that combines local CV heuristics and a vision LLM."""

from __future__ import annotations

import colorsys
from typing import Any, Dict, Optional

import numpy as np
from PIL import Image

from src.color_extractor import ColorExtractor
from src.image_preprocessor import ImagePreprocessor
from src.llm_client import LLMClient
from src.local_model import LocalFabricModel, get_local_model_client
from src.prompt_templates import FABRIC_ANALYSIS_PROMPT


DEFAULT_DOMINANT_COLOR = {"name": "Unknown", "hex": "#888888", "rgb": (136, 136, 136)}
QUALITY_SCORE_BONUS_FABRICS = {"Denim", "Wool Blend", "Wool"}
STRUCTURED_FABRICS = {"Denim", "Wool Blend", "Wool", "Leather"}
DELICATE_FABRICS = {"Silk Blend", "Silk", "Satin"}
HIGH_PILLING_FABRICS = {"Wool Blend", "Wool", "Fleece", "Chenille"}
MEDIUM_PILLING_FABRICS = {"Cotton Blend", "Polyester Blend", "Linen Blend", "Cotton", "Polyester", "Linen", "Viscose"}
NATURAL_FIBER_FABRICS = {"Cotton Blend", "Linen Blend", "Wool Blend", "Denim", "Cotton", "Linen", "Wool", "Terrycloth"}
SHEEN_HEAVY_FABRICS = {"Silk Blend", "Silk", "Satin", "Velvet"}
INTERIOR_FRIENDLY_LIGHTWEIGHTS = {"Cotton Blend", "Linen Blend", "Cotton", "Linen", "Terrycloth"}


class FabricAnalyzer:
    """Run end-to-end analysis for a fabric image."""

    def __init__(
        self,
        llm_provider: Optional[str] = None,
        llm_client: Optional[LLMClient] = None,
        local_model_client: Optional[LocalFabricModel] = None,
    ):
        self._llm_client = llm_client
        self._local_model_client = local_model_client
        self.llm_provider = llm_provider
        self.color_extractor = ColorExtractor(n_colors=6)
        self.preprocessor = ImagePreprocessor()

    @property
    def llm_client(self) -> LLMClient:
        if self._llm_client is None:
            self._llm_client = LLMClient(provider=self.llm_provider)
        return self._llm_client

    @property
    def local_model_client(self) -> LocalFabricModel:
        if self._local_model_client is None:
            self._local_model_client = get_local_model_client()
        return self._local_model_client

    def analyze(self, image: Image.Image, mode: str = "ai") -> Dict[str, Any]:
        processed = self.preprocessor.resize_for_analysis(image.copy())
        enhanced = self.preprocessor.enhance_image(processed)

        color_palette = self.color_extractor.extract_palette(image)
        harmony = self.color_extractor.get_color_harmony(color_palette)
        image_info = self.preprocessor.get_image_info(image)

        normalized_mode = self._normalize_mode(mode)
        if normalized_mode == "heuristic":
            analysis_body = self._analyze_locally(image, color_palette, harmony)
            model_used = "local-heuristics"
        elif normalized_mode == "trained":
            analysis_body = self._analyze_with_local_model(image, color_palette, harmony)
            model_used = self.local_model_client.model_name
        else:
            analysis_body = self.llm_client.analyze_image(enhanced, FABRIC_ANALYSIS_PROMPT)
            model_used = self.llm_client.provider

        return self._build_analysis_result(
            analysis_body=analysis_body,
            color_palette=color_palette,
            harmony=harmony,
            image_info=image_info,
            model_used=model_used,
            analysis_mode=normalized_mode,
        )

    def _normalize_mode(self, mode: str) -> str:
        if mode in {"local", "heuristic"}:
            return "heuristic"
        if mode == "trained":
            return "trained"
        return "ai"

    def _build_analysis_result(
        self,
        analysis_body: Dict[str, Any],
        color_palette: list[dict],
        harmony: str,
        image_info: Dict[str, Any],
        model_used: str,
        analysis_mode: str,
    ) -> Dict[str, Any]:
        return {
            "llm_analysis": analysis_body,
            "color_palette": {
                "colors": color_palette,
                "harmony_type": harmony,
                "dominant_color": color_palette[0] if color_palette else None,
            },
            "image_info": image_info,
            "analysis_metadata": {
                "model_used": model_used,
                "analysis_mode": analysis_mode,
                "color_clusters": len(color_palette),
            },
        }

    def _analyze_locally(self, image: Image.Image, palette: list[dict], harmony: str) -> Dict[str, Any]:
        return self._build_local_analysis(image=image, palette=palette, harmony=harmony)

    def _analyze_with_local_model(self, image: Image.Image, palette: list[dict], harmony: str) -> Dict[str, Any]:
        prediction = self.local_model_client.predict(image)
        return self._build_local_analysis(image=image, palette=palette, harmony=harmony, model_prediction=prediction)

    def _build_local_analysis(
        self,
        image: Image.Image,
        palette: list[dict],
        harmony: str,
        model_prediction: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        metrics = self._compute_visual_metrics(image)
        dominant = self._dominant_color(palette)
        pattern = self._infer_pattern(metrics, palette)
        texture = self._infer_texture(metrics)
        fabric = (
            self._infer_fabric(metrics, pattern, texture, dominant)
            if model_prediction is None
            else self._fabric_from_model_prediction(model_prediction)
        )
        quality = self._infer_quality(metrics, fabric)
        summary_source = "trained" if model_prediction is not None else "heuristic"
        summary = self._overall_summary(
            fabric,
            pattern,
            texture,
            dominant,
            quality,
            harmony,
            source=summary_source,
            model_confidence=None if model_prediction is None else model_prediction["confidence"],
        )

        analysis = {
            "fabric_type": fabric,
            "pattern": pattern,
            "texture": texture,
            "quality_assessment": quality,
            "care_instructions": self._care_instructions_for(fabric["primary"]),
            "occasion_suitability": self._occasion_suitability(fabric["primary"], pattern["type"], texture["weight"]),
            "season_recommendation": self._season_recommendation(texture, fabric),
            "price_range": self._price_range_for(fabric["primary"], quality["score"]),
            "sustainability": self._sustainability_for(fabric["primary"]),
            "styling_suggestions": self._styling_suggestions(fabric["primary"], pattern["type"], dominant["name"]),
            "interior_use": self._interior_use(fabric["primary"], texture["weight"]),
            "fun_fact": self._fun_fact_for(fabric["primary"]),
            "overall_summary": summary,
        }
        if model_prediction is not None:
            analysis["model_prediction"] = model_prediction
        return analysis

    def _dominant_color(self, palette: list[dict]) -> Dict[str, Any]:
        if palette:
            return palette[0]
        return DEFAULT_DOMINANT_COLOR.copy()

    def _fabric_from_model_prediction(self, prediction: Dict[str, Any]) -> Dict[str, str]:
        label = prediction["label"]
        return {
            "primary": label,
            "sub_type": f"Locally trained model prediction ({prediction['architecture']})",
            "blend_composition": "Image-only prediction; exact blend not verified.",
            "confidence": self._confidence_label(prediction["confidence"]),
        }

    def _confidence_label(self, value: float) -> str:
        percentage = round(value * 100, 1)
        if value >= 0.8:
            level = "high"
        elif value >= 0.55:
            level = "medium"
        else:
            level = "low"
        return f"{level} ({percentage}%)"

    def _compute_visual_metrics(self, image: Image.Image) -> Dict[str, float]:
        sample = image.copy().resize((256, 256), Image.Resampling.LANCZOS)
        rgb = np.array(sample).astype(np.float32)
        gray = np.array(sample.convert("L")).astype(np.float32)

        row_profile = gray.mean(axis=1)
        col_profile = gray.mean(axis=0)
        row_strength = float(np.std(row_profile) / 255 * 100)
        col_strength = float(np.std(col_profile) / 255 * 100)

        gx = np.abs(np.diff(gray, axis=1))
        gy = np.abs(np.diff(gray, axis=0))
        edge_density = float((((gx > 18).mean() + (gy > 18).mean()) / 2) * 100)
        texture_strength = float(((gx.mean() + gy.mean()) / 2) / 255 * 100)
        contrast = float(np.std(gray) / 255 * 100)
        brightness = float(np.mean(gray) / 255 * 100)
        highlight_ratio = float((gray > 220).mean() * 100)

        rgb_norm = rgb / 255.0
        maxc = rgb_norm.max(axis=2)
        minc = rgb_norm.min(axis=2)
        saturation = np.where(maxc == 0, 0, (maxc - minc) / maxc)
        mean_saturation = float(np.mean(saturation) * 100)

        rgb_flat = rgb_norm.reshape(-1, 3)
        sheen = []
        for r, g, b in rgb_flat[::64]:
            _, s, v = colorsys.rgb_to_hsv(float(r), float(g), float(b))
            sheen.append(v * (1 - s / 2))
        sheen_score = float(np.mean(sheen) * 100)

        return {
            "brightness": brightness,
            "contrast": contrast,
            "texture_strength": texture_strength,
            "edge_density": edge_density,
            "row_strength": row_strength,
            "col_strength": col_strength,
            "highlight_ratio": highlight_ratio,
            "mean_saturation": mean_saturation,
            "sheen_score": sheen_score,
        }

    def _infer_pattern(self, metrics: Dict[str, float], palette: list[dict]) -> Dict[str, str]:
        row_strength = metrics["row_strength"]
        col_strength = metrics["col_strength"]
        contrast = metrics["contrast"]
        color_count = len(palette)

        if max(row_strength, col_strength) < 5 and contrast < 12:
            pattern_type = "Solid"
            sub_type = "Minimal tonal variation"
            scale = "small"
            repeat = "none"
        elif col_strength > row_strength * 1.35 and col_strength > 6:
            pattern_type = "Striped"
            sub_type = "Vertical stripe"
            scale = "medium"
            repeat = "regular"
        elif row_strength > col_strength * 1.35 and row_strength > 6:
            pattern_type = "Striped"
            sub_type = "Horizontal stripe"
            scale = "medium"
            repeat = "regular"
        elif min(row_strength, col_strength) > 6 and abs(row_strength - col_strength) < 4:
            pattern_type = "Plaid" if color_count <= 4 else "Geometric"
            sub_type = "Grid repeat" if pattern_type == "Plaid" else "Angular repeat"
            scale = "medium"
            repeat = "regular"
        else:
            pattern_type = "Geometric" if color_count >= 4 else "Textured solid"
            sub_type = "Irregular visual texture"
            scale = "small"
            repeat = "irregular"

        return {
            "type": pattern_type,
            "sub_type": sub_type,
            "pattern_scale": scale,
            "pattern_repeat": repeat,
            "description": f"Locally inferred {pattern_type.lower()} surface with {len(palette)} dominant color groups.",
        }

    def _infer_texture(self, metrics: Dict[str, float]) -> Dict[str, str]:
        texture_strength = metrics["texture_strength"]
        sheen_score = metrics["sheen_score"]

        if texture_strength < 4:
            primary = "Smooth"
            hand_feel = "Soft and even"
        elif texture_strength < 7:
            primary = "Woven"
            hand_feel = "Balanced with light structure"
        elif texture_strength < 11:
            primary = "Textured"
            hand_feel = "Noticeably tactile"
        else:
            primary = "Rough"
            hand_feel = "Dry and visibly textured"

        if texture_strength < 4.5:
            weight = "Lightweight"
        elif texture_strength < 9.5:
            weight = "Medium-weight"
        else:
            weight = "Heavyweight"

        if weight == "Lightweight" or sheen_score > 63:
            drape = "Fluid"
        elif weight == "Heavyweight":
            drape = "Stiff"
        else:
            drape = "Semi-structured"

        if sheen_score > 72:
            sheen = "Glossy"
        elif sheen_score > 58:
            sheen = "Semi-sheen"
        else:
            sheen = "Matte"

        return {
            "primary": primary,
            "hand_feel": hand_feel,
            "weight": weight,
            "drape": drape,
            "sheen": sheen,
        }

    def _infer_fabric(
        self,
        metrics: Dict[str, float],
        pattern: Dict[str, str],
        texture: Dict[str, str],
        dominant: Dict[str, Any],
    ) -> Dict[str, str]:
        dominant_name = dominant.get("name", "Unknown")
        mean_saturation = metrics["mean_saturation"]
        sheen = texture["sheen"]
        weight = texture["weight"]

        if dominant_name in {"Navy", "Blue"} and weight != "Lightweight":
            primary = "Denim"
            sub_type = "Classic indigo twill"
            blend = "Likely cotton-rich denim"
            confidence = "medium"
        elif pattern["type"] == "Plaid" and weight == "Heavyweight":
            primary = "Wool Blend"
            sub_type = "Coating or suiting plaid"
            blend = "Likely wool-blend construction"
            confidence = "medium"
        elif sheen in {"Glossy", "Semi-sheen"} and texture["primary"] == "Smooth":
            primary = "Silk Blend"
            sub_type = "Satin-like dress fabric"
            blend = "Likely silk or synthetic satin blend"
            confidence = "low"
        elif texture["primary"] in {"Rough", "Textured"} and mean_saturation < 28:
            primary = "Linen Blend"
            sub_type = "Slubbed woven linen look"
            blend = "Likely linen-rich or linen-look blend"
            confidence = "low"
        elif mean_saturation > 42 or pattern["type"] == "Geometric":
            primary = "Polyester Blend"
            sub_type = "Printed synthetic fashion fabric"
            blend = "Likely polyester-forward blend"
            confidence = "medium"
        else:
            primary = "Cotton Blend"
            sub_type = "Plain woven casual fabric"
            blend = "Likely cotton-rich blend"
            confidence = "medium"

        return {
            "primary": primary,
            "sub_type": sub_type,
            "blend_composition": blend,
            "confidence": confidence,
        }

    def _infer_quality(self, metrics: Dict[str, float], fabric: Dict[str, str]) -> Dict[str, Any]:
        exposure_balance = max(0.0, 1.0 - abs(metrics["brightness"] - 58) / 58)
        base_score = 5.4
        base_score += min(metrics["contrast"] / 18, 1.3)
        base_score += min(metrics["edge_density"] / 30, 1.0)
        base_score += exposure_balance * 1.2
        if fabric["primary"] in QUALITY_SCORE_BONUS_FABRICS:
            base_score += 0.4
        if metrics["highlight_ratio"] > 18:
            base_score -= 0.4

        score = round(max(4.8, min(base_score, 9.1)), 1)
        if score >= 8.2:
            grade = "A"
        elif score >= 6.8:
            grade = "B"
        elif score >= 5.6:
            grade = "C"
        else:
            grade = "D"

        factors = []
        if metrics["contrast"] > 14:
            factors.append("Clear surface definition visible in the textile image")
        else:
            factors.append("Soft visual contrast suggests a gentler surface finish")
        if metrics["edge_density"] > 16:
            factors.append("Surface structure appears reasonably well defined")
        else:
            factors.append("Image shows limited micro-detail, so fine weave quality is harder to confirm")
        if metrics["highlight_ratio"] > 18:
            factors.append("Bright highlights may hide some fabric detail")
        else:
            factors.append("Exposure looks balanced enough for a stable local read")

        durability = "High" if fabric["primary"] in STRUCTURED_FABRICS else "Medium"
        if fabric["primary"] in DELICATE_FABRICS:
            durability = "Low"

        pilling = "High" if fabric["primary"] in HIGH_PILLING_FABRICS else "Low"
        if fabric["primary"] in MEDIUM_PILLING_FABRICS:
            pilling = "Medium"

        return {
            "score": score,
            "out_of": 10,
            "grade": grade,
            "factors": factors,
            "durability_estimate": durability,
            "pilling_tendency": pilling,
        }

    def _care_instructions_for(self, fabric_name: str) -> Dict[str, Any]:
        if fabric_name == "Denim":
            return {
                "washing": "Wash cold inside out to preserve dye depth.",
                "drying": "Line dry or tumble dry low.",
                "ironing": "Warm iron if needed.",
                "special_care": "Expect some dye transfer on the first few washes.",
                "dry_clean_recommended": False,
                "bleach_safe": False,
            }
        if fabric_name in DELICATE_FABRICS:
            return {
                "washing": "Hand wash or delicate wash in cold water.",
                "drying": "Air dry away from direct sun.",
                "ironing": "Low iron on the reverse side.",
                "special_care": "Use a pressing cloth and avoid harsh agitation.",
                "dry_clean_recommended": True,
                "bleach_safe": False,
            }
        if fabric_name in {"Wool Blend", "Wool", "Fleece"}:
            return {
                "washing": "Cool hand wash or wool-safe cycle.",
                "drying": "Dry flat to maintain shape.",
                "ironing": "Low steam with a pressing cloth.",
                "special_care": "Avoid high agitation to reduce felting risk.",
                "dry_clean_recommended": True,
                "bleach_safe": False,
            }
        return {
            "washing": "Machine wash cold on a gentle cycle.",
            "drying": "Line dry or tumble dry low.",
            "ironing": "Low to medium heat depending on finish.",
            "special_care": "Test heat on a hidden edge first if the blend is uncertain.",
            "dry_clean_recommended": False,
            "bleach_safe": False,
        }

    def _season_recommendation(self, texture: Dict[str, str], fabric: Dict[str, str]) -> Dict[str, Any]:
        if texture["weight"] == "Lightweight":
            best = ["Spring", "Summer"]
            avoid = ["Winter"]
            climate = "Best for warm to mildly humid weather"
            breathability = "High"
        elif texture["weight"] == "Heavyweight":
            best = ["Autumn", "Winter"]
            avoid = ["Summer"]
            climate = "Better suited to cool or dry conditions"
            breathability = "Low" if fabric["primary"] in {"Wool Blend", "Polyester Blend", "Wool", "Polyester", "Leather"} else "Medium"
        else:
            best = ["Spring", "Autumn"]
            avoid = []
            climate = "Flexible for transitional weather"
            breathability = "Medium"

        return {
            "best_seasons": best,
            "avoid_seasons": avoid,
            "climate_suitability": climate,
            "breathability": breathability,
        }

    def _price_range_for(self, fabric_name: str, quality_score: float) -> Dict[str, str]:
        if fabric_name in {"Silk Blend", "Silk", "Satin"}:
            category = "Premium" if quality_score < 8 else "Luxury"
            usd = "$28-65"
            inr = "2300-5400"
        elif fabric_name in {"Wool Blend", "Wool", "Denim", "Leather", "Suede"}:
            category = "Premium" if quality_score >= 7.5 else "Mid-range"
            usd = "$18-42"
            inr = "1500-3500"
        elif fabric_name in {"Polyester Blend", "Polyester", "Nylon", "Acrylic"}:
            category = "Budget" if quality_score < 7 else "Mid-range"
            usd = "$8-22"
            inr = "650-1800"
        else:
            category = "Mid-range"
            usd = "$12-28"
            inr = "1000-2300"

        value = "Excellent" if quality_score >= 8 else "Good" if quality_score >= 6.8 else "Fair"
        return {
            "category": category,
            "estimated_per_meter_usd": usd,
            "estimated_per_meter_inr": inr,
            "value_for_money": value,
        }

    def _sustainability_for(self, fabric_name: str) -> Dict[str, Any]:
        if fabric_name in NATURAL_FIBER_FABRICS:
            return {
                "eco_score": 7,
                "out_of": 10,
                "biodegradable": True,
                "recyclable": True,
                "environmental_impact": "Medium",
                "notes": "Likely contains a meaningful natural-fiber component, though image-only analysis cannot verify the exact blend.",
            }
        if fabric_name in {"Silk Blend", "Silk"}:
            return {
                "eco_score": 6,
                "out_of": 10,
                "biodegradable": True,
                "recyclable": False,
                "environmental_impact": "Medium",
                "notes": "Silk-family fabrics can age well, but blends and finishing treatments change the sustainability profile.",
            }
        if fabric_name == "Viscose":
            return {
                "eco_score": 5,
                "out_of": 10,
                "biodegradable": True,
                "recyclable": False,
                "environmental_impact": "Medium",
                "notes": "Viscose is cellulose-based but manufacturing methods strongly affect its environmental profile.",
            }
        return {
            "eco_score": 4,
            "out_of": 10,
            "biodegradable": False,
            "recyclable": True,
            "environmental_impact": "High",
            "notes": "Synthetic-looking fabrics are usually easier to maintain but less favorable environmentally.",
        }

    def _occasion_suitability(self, fabric_name: str, pattern_type: str, weight: str) -> list[dict]:
        if fabric_name in SHEEN_HEAVY_FABRICS:
            return [
                {"occasion": "Formal", "suitability_score": 9, "note": "Smooth surface and sheen fit occasion dressing."},
                {"occasion": "Party", "suitability_score": 8, "note": "Reflective finish works well under evening lighting."},
            ]
        if fabric_name == "Denim":
            return [
                {"occasion": "Casual", "suitability_score": 9, "note": "Structured durability suits everyday wear."},
                {"occasion": "Streetwear", "suitability_score": 8, "note": "Works well in utilitarian silhouettes."},
            ]
        if weight == "Heavyweight":
            return [
                {"occasion": "Outerwear", "suitability_score": 8, "note": "Visual body supports jackets or overshirts."},
                {"occasion": "Interior Accent", "suitability_score": 7, "note": "Heavier fabrics adapt well to cushions or panels."},
            ]
        return [
            {"occasion": "Casual", "suitability_score": 8, "note": f"{pattern_type} styling reads versatile in daily wear."},
            {"occasion": "Smart Casual", "suitability_score": 7, "note": "Balanced structure supports polished but relaxed outfits."},
        ]

    def _styling_suggestions(self, fabric_name: str, pattern_type: str, dominant_color: str) -> list[dict]:
        if fabric_name in SHEEN_HEAVY_FABRICS:
            return [
                {"garment": "Blouse", "style": "Soft drape with clean tailoring", "target_audience": "Occasion and evening wear"},
                {"garment": "Slip dress", "style": "Minimal silhouette with sheen-led styling", "target_audience": "Fashion-forward dressing"},
            ]
        if fabric_name == "Denim":
            return [
                {"garment": "Jacket", "style": "Utility-inspired layering piece", "target_audience": "Casual unisex wardrobes"},
                {"garment": "Jeans or skirt", "style": "Structured everyday staple", "target_audience": "Street and daily wear"},
            ]
        return [
            {"garment": "Shirt", "style": f"Clean {pattern_type.lower()} finish with {dominant_color.lower()} emphasis", "target_audience": "Everyday wear"},
            {"garment": "Dress or kurta", "style": "Easy silhouette built around the fabric surface", "target_audience": "General lifestyle wear"},
        ]

    def _interior_use(self, fabric_name: str, weight: str) -> Dict[str, Any]:
        suitable = weight != "Lightweight" or fabric_name in INTERIOR_FRIENDLY_LIGHTWEIGHTS
        suggestions = []
        if suitable:
            suggestions = ["Cushion covers", "Curtain panels"]
            if weight == "Heavyweight":
                suggestions.append("Light upholstery accents")
        return {
            "suitable": suitable,
            "suggestions": suggestions,
            "notes": "Local mode estimates interior suitability from surface weight and structure only.",
        }

    def _fun_fact_for(self, fabric_name: str) -> str:
        facts = {
            "Cotton Blend": "Cotton remains one of the most widely used natural fibers in global apparel.",
            "Cotton": "Cotton remains one of the most widely used natural fibers in global apparel.",
            "Linen Blend": "Linen is derived from flax and is known for its cool hand feel in warm climates.",
            "Linen": "Linen is derived from flax and is known for its cool hand feel in warm climates.",
            "Silk Blend": "Silk filaments can create an impressive sheen even when blended in small amounts.",
            "Silk": "Silk filaments can create an impressive sheen even when blended in small amounts.",
            "Wool Blend": "Wool fibers can hold moisture without immediately feeling wet.",
            "Wool": "Wool fibers can hold moisture without immediately feeling wet.",
            "Denim": "Denim is traditionally woven as a durable twill with indigo-dyed warp yarns.",
            "Polyester Blend": "Polyester can mimic many fabric looks, from crisp shirting to fluid dress fabrics.",
            "Polyester": "Polyester can mimic many fabric looks, from crisp shirting to fluid dress fabrics.",
        }
        return facts.get(fabric_name, "Fabric finishes can significantly change how a textile looks and behaves.")

    def _overall_summary(
        self,
        fabric: Dict[str, str],
        pattern: Dict[str, str],
        texture: Dict[str, str],
        dominant: Dict[str, Any],
        quality: Dict[str, Any],
        harmony: str,
        source: str = "heuristic",
        model_confidence: float | None = None,
    ) -> str:
        base = (
            f"The image points to a {fabric['primary'].lower()} with a {pattern['type'].lower()} presentation, "
            f"{texture['primary'].lower()} surface character, and a dominant {dominant.get('name', 'neutral').lower()} tone. "
            f"The fabric reads as {texture['weight'].lower()} with a {quality['score']}/10 visual quality score and a {harmony.lower()} color story."
        )
        if source == "trained" and model_confidence is not None:
            return f"Locally trained model prediction suggests {fabric['primary'].lower()} at about {round(model_confidence * 100, 1)}% confidence. {base}"
        return f"Local heuristic analysis suggests {fabric['primary'].lower()}. {base}"
