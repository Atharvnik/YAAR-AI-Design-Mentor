# YAAR AI Design Mentor

**YAAR AI Design Mentor** is a multimodal AI-powered UI/UX review assistant that analyzes website and application screenshots and provides automated design feedback.

The system combines computer vision, OCR, visual analysis, accessibility checks, and an LLM-based review layer to help identify potential UI/UX issues from a static screenshot.

---

## Features

* **YOLO-based UI element detection**
* **EasyOCR text extraction**
* **CLIP-based visual style analysis**
* **Accessibility and contrast analysis**
* **Gemini-powered UI/UX review**
* **PostgreSQL review history**
* **FastAPI backend**
* **Browser-based frontend**
* **PNG/JPEG upload validation**

---

## How It Works

The user uploads a screenshot of a website or application through the browser. YAAR processes the screenshot through multiple analysis stages, combines the results, and generates a structured UI/UX review.

```text
Uploaded Screenshot
        |
        v
YOLO UI Detection
        |
        v
EasyOCR Text Extraction
        |
        v
CLIP Visual Analysis
        |
        v
Accessibility Analysis
        |
        v
Result Merger
        |
        v
Gemini UI/UX Review
        |
        v
PostgreSQL Review History
```

### 1. YOLO UI Detection

The trained YOLO model identifies UI components present in the screenshot, such as buttons, fields, headings, images, links, labels, and text.

For each detected element, the model provides its class, confidence, and bounding-box coordinates.

### 2. EasyOCR Text Extraction

EasyOCR extracts visible text from the screenshot. The extracted information includes the recognized text, confidence value, and text location.

### 3. CLIP Visual Analysis

CLIP analyzes the visual appearance of the screenshot by comparing it with predefined visual descriptions. This provides relative visual-category information about the interface.

### 4. Accessibility Analysis

The accessibility module performs basic image and UI-based checks, including contrast-related analysis, OCR confidence, and detected element dimensions.

The accessibility result is a project-specific heuristic and is not intended to represent formal WCAG compliance.

### 5. Result Merger

The results from YOLO, EasyOCR, CLIP, and accessibility analysis are combined into a single structured result.

This allows the different analysis modules to work together as one pipeline.

### 6. Gemini UI/UX Review

The merged analysis results are passed to Gemini to generate a human-readable UI/UX review containing design observations, issues, accessibility notes, and recommendations.

Gemini receives the structured analysis results rather than the original screenshot.

### 7. PostgreSQL Review History

The generated review and analysis information are stored in PostgreSQL so that previous reviews can be accessed through the review history.

---

## Project Architecture

```text
YAAR(AI-Design-Mentor)/
│
├── backend/
│   │
│   ├── ai/
│   │   ├── accessibility.py
│   │   ├── clip_analyzer.py
│   │   ├── gemini_reviewer.py
│   │   ├── pipeline.py
│   │   ├── result_merger.py
│   │   ├── train_model.py
│   │   └── yolo_detector.py
│   │
│   ├── models/
│   │   └── website_ui_detector/
│   │
│   ├── routes/
│   │   ├── detect.py
│   │   ├── review.py
│   │   └── reviews.py
│   │
│   ├── uploads/
│   └── main.py
│
├── database/
│   ├── connection.py
│   └── repository.py
│
├── dataset/
│   ├── train/
│   ├── valid/
│   └── test/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── tests/
├── requirements.txt
└── README.md




