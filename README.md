# Integrative Analysis of Multiomics Data Workshop

This repository contains tutorial material for **TOAST** (Topography-Aware Optimal Alignment of Spatially Resolved Tissues), an optimal transport framework for aligning spatial omics data, and **DOT**, a multi-objective optimization framework for transferring features across single-cell and spatial omics data.

TOAST extends the classical Fused Gromov-Wasserstein (FGW) objective with two spatially informed terms — *spatial coherence* and *neighbourhood consistency* — that preserve local tissue organisation and molecular heterogeneity during alignment. It supports slice-to-slice alignment, multimodal integration (e.g. transcriptomics + proteomics), and spatial reconstruction from dissociated single-cell data.

> Ceccarelli et al., *Topography-aware optimal transport for alignment of spatial omics data*, Cell Reports Methods (2026). https://doi.org/10.1016/j.crmeth.2026.101373

DOT uses optimal transport to transfer cell type labels, gene expression, and other features from single-cell reference data to spatial omics measurements. It jointly optimizes multiple objectives to preserve transcriptomic similarity, spatial structure, and feature consistency, enabling annotation transfer, deconvolution, and spatial gene expression imputation across modalities.

> Rahimi et al., *DOT: a flexible multi-objective optimization framework for transferring features across single-cell and spatial omics*, Nature Communications (2024). https://doi.org/10.1038/s41467-024-48868-z

---

## Contents

| Notebook | Description |
|---|---|
| [`TOAST/visium.ipynb`](visium.ipynb) | Evaluation of TOAST on the human dorsolateral prefrontal cortex (DLPFC) 10× Visium dataset. Reproduces Figure 3 of the paper: consecutive, non-consecutive, and cross-sample slice alignment benchmarks. |
| `TOAST/xenium_tutorial.ipynb` | Multimodal alignment of Xenium transcript and protein data. |
| `DOT/Cortical_layer_annotation_transfer.ipynb` | LIBD/DLPFC Visium-to-Visium cortical-layer annotation transfer. Known layer labels from source sections are transferred to target sections, while target labels are withheld during fitting and used afterward as ground truth for accuracy evaluation. |
| `DOT/Gene_expression_imputation.ipynb` | Breast-cancer Xenium gene-expression imputation. DOT learns reference-community weights for Xenium cells from genes shared with a transcriptome-wide single-cell reference, then reconstructs measured Xenium genes and imputes genes absent from the Xenium panel for comparison with aligned Visium data. |


---

## Installation

Environment management uses [Pixi](https://pixi.sh), which resolves all dependencies (including `spatialdata` and its geospatial binary packages) from conda-forge in a single step.

See [installation.txt](installation.txt) for full instructions. In brief:

```bash
# 1. Install Pixi (one-time)
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Launch Jupyter for the TOAST notebooks
pixi run -e toast jupyter notebook

# 3. Launch JupyterLab for the DOT notebooks
pixi run -e dotpy jupyter lab
```

The environments are stored in `.pixi/envs/` and do not affect any existing conda environments.
