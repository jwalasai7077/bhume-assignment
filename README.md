# BhuMe Assignment – Cadastral Boundary Alignment

## Problem Statement

The objective is to improve the alignment of official cadastral plot boundaries with the actual field boundaries visible on satellite imagery.

The provided cadastral maps contain georeferencing errors that cause plots to be shifted relative to their true locations. The task is to identify and correct this drift while producing confidence estimates for each correction.

---

## Dataset

The village bundle contains:

* `input.geojson` – Official cadastral plot geometries
* `imagery.tif` – Satellite imagery
* `boundaries.tif` – Boundary hint raster
* `example_truths.geojson` – Small set of hand-corrected examples

Village used:

* Vadnerbhairav (Nashik)

---

## Approach

### 1. Drift Analysis

I first compared the example truth polygons with the official cadastral polygons.

By analyzing centroid differences and visualizing the geometries, I observed that most corrections could be explained by a consistent village-wide translation rather than major shape distortions.

### 2. Village-Wide Drift Estimation

For each example truth polygon:

* Compute official centroid
* Compute corrected centroid
* Measure centroid displacement

The median displacement across all example truths was used as a robust estimate of village-wide drift.

### 3. Plot Correction

Each cadastral plot was translated using the estimated median drift.

This produced a corrected geometry for every plot in the village.

### 4. Confidence Framework

A confidence field was included in the prediction schema.

The framework supports future calibration and flagging of uncertain corrections.

### 5. Future Refinement

The provided `boundaries.tif` raster was investigated as a potential signal for local per-plot refinement.

Future work would use boundary overlap scoring to improve alignment beyond a global translation model.

---

## Results

Example truth evaluation:

* Official Median IoU: 0.612
* Corrected Median IoU: 0.713
* Improvement: +0.113

Additional metrics:

* Accurate (IoU ≥ 0.5): 100%
* Median centroid error: 8.815 m

### Official vs Corrected Example

The figure below compares the official cadastral boundary (red) against the example truth boundary (green).

<img width="1600" height="1600" alt="plot_1145_compare" src="https://github.com/user-attachments/assets/d737f46a-9a82-4bb3-bd8a-60354f074095" />

This visualization shows that the dominant error is a translation (shift) rather than a major shape distortion, which motivated the median drift correction approach.

Video Walkthrough

Google Drive:
https://drive.google.com/file/d/1O7owXX4VX-Ok_u9Xk0WgV2LODn58C3Qi/view?usp=sharing
---

## Repository Structure

```text
code/
    predictor_v5.py

outputs/
    predictions_vadnerbhairav.geojson

images/
    plot_1145_compare.png

transcripts/
    README.md
```

---

## Installation

```bash
pip install -r requirements.txt
```

or

```bash
uv sync
```

---

## Running

```bash
uv run predictor_v5.py
```

This generates:

```text
predictions_vadnerbhairav.geojson
```

---

## Future Work

* Boundary-guided local refinement
* Confidence calibration
* Plot-level uncertainty estimation
* Multi-scale imagery analysis
