from pathlib import Path

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# Load CLIP model once
MODEL_NAME = "openai/clip-vit-base-patch32"

processor = CLIPProcessor.from_pretrained(MODEL_NAME)
model = CLIPModel.from_pretrained(MODEL_NAME)


def analyze_image(image_path: Path):
    """
    Analyze a UI screenshot using CLIP.
    """

    image = Image.open(image_path).convert("RGB")

    labels = [
        "a modern website UI",
        "a clean and minimal UI",
        "a cluttered website UI",
        "a professional website UI",
        "a poorly designed website UI",
        "a mobile app UI",
        "a payment interface"
    ]

    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = outputs.logits_per_image.softmax(dim=1)[0]

    results = []

    for label, score in zip(labels, probabilities):
        results.append({
            "label": label,
            "confidence": round(float(score), 4)
        })

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results