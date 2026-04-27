# FabriSense

FabriSense is a Streamlit application for fabric image analysis. It converts an uploaded textile image into a structured material brief using local image processing and local trained checkpoints.

The app is designed for practical analysis workflows: single-image review, side-by-side comparison, batch processing, history tracking, and exportable reports.

## Core Features

- Fabric analysis from image uploads or sample images
- Two local analysis modes: `Local Heuristics` and `Local Trained Model`
- Side-by-side fabric comparison
- Batch analysis with CSV export
- Local history of previous analyses
- Model benchmark and checkpoint review pages
- PDF report generation

## Implementation Details

### Application Architecture

- `app.py` bootstraps Streamlit and page routing.
- `ui/` contains page composition, reusable UI blocks, and styling.
- `src/` contains the analysis engine, preprocessing, color extraction, reporting, and persistence utilities.
- `training/` contains dataset handling, model definitions, training, evaluation, and run comparison tooling.

### Analysis Pipeline

1. Input image is validated and normalized by preprocessing utilities.
2. Visual features are extracted, including dominant palette and texture/pattern cues.
3. Analysis mode logic runs:
	- `Local Heuristics`: rule-based interpretation from extracted visual signals.
	- `Local Trained Model`: checkpoint-based fabric-family prediction plus local feature analysis.
4. Structured result is assembled for display, comparison, history storage, and export.

### Model and Benchmarking

- Trained checkpoints and run artifacts are stored under `artifacts/`.
- Benchmark utilities support checkpoint comparison and manifest-based evaluation.
- Review history and benchmark outputs are persisted locally for repeatable analysis.

## Analysis Modes

### Local Heuristics

Uses local preprocessing and rule-based computer-vision signals (palette, texture, pattern cues) to build a structured fabric brief.

### Local Trained Model

Uses local checkpoints from project artifacts/models for fabric-family prediction, then combines that with local feature analysis to produce the final brief.

## Application Pages

- Analyze
- Batch Analysis
- Compare Fabrics
- History
- Fabric Guide
- Care Guide
- Models
- About

## Tech Stack

- Python 3.11+
- Streamlit
- Pillow
- NumPy
- PyTorch (for trained-model workflow)
- fpdf2

## Project Layout

```text
FabriSense/
|-- app.py
|-- src/
|-- ui/
|-- training/
|-- tests/
|-- assets/
|-- data/
|-- artifacts/
|-- requirements.txt
`-- requirements-ml.txt
```

## Setup

### 1. Create and activate virtual environment

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Install ML extras (recommended)

```powershell
pip install -r requirements-ml.txt
```

## Run

```powershell
streamlit run app.py
```

## Testing

```powershell
python -m unittest discover -s tests -v
```

