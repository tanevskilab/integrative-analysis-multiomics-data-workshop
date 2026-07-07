# Integrative Analysis of Multiomics Data Workshop

This repository contains tutorial material for **TOAST** (Topography-Aware Optimal Alignment of Spatially Resolved Tissues), an optimal transport framework for aligning spatial omics data.

TOAST extends the classical Fused Gromov-Wasserstein (FGW) objective with two spatially informed terms — *spatial coherence* and *neighbourhood consistency* — that preserve local tissue organisation and molecular heterogeneity during alignment. It supports slice-to-slice alignment, multimodal integration (e.g. transcriptomics + proteomics), and spatial reconstruction from dissociated single-cell data.

> Ceccarelli et al., *Topography-aware optimal transport for alignment of spatial omics data*, Cell Reports Methods (2026). https://doi.org/10.1016/j.crmeth.2026.101373

---

## Contents

| Notebook | Description |
|---|---|
| [`visium.ipynb`](visium.ipynb) | Evaluation of TOAST on the human dorsolateral prefrontal cortex (DLPFC) 10× Visium dataset. Reproduces Figure 3 of the paper: consecutive, non-consecutive, and cross-sample slice alignment benchmarks. |
| `xenium_tutorial.ipynb` | *(coming soon)* Multimodal alignment of Xenium transcript and protein data. |

---

## Installation

Environment management uses [Pixi](https://pixi.sh), which resolves all dependencies (including `spatialdata` and its geospatial binary packages) from conda-forge in a single step.

See [installation.txt](installation.txt) for full instructions. In brief:

```bash
# 1. Install Pixi (one-time)
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Launch Jupyter
pixi run -e toast jupyter notebook
```

The environment is stored in `.pixi/envs/` and does not affect any existing conda environments.
