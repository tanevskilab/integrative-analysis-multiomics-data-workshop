"""Create the reconstructed Figure 7 common-region barcode lists.

This script uses only coordinates distributed with the original 10x Xenium and
Visium datasets. 

The bounds reconstruct the rectangular intersection illustrated in
Supplementary Figure 7 and reproduce the published input dimensions:
139,806 Xenium cells and 3,958 Visium spots.  The authors did not publish their
original ROI barcodes or cross-assay transform, so these bounds remain a
documented reconstruction rather than an official registration.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


# Reconstructed common capture-area bounds in the original coordinate systems.
XENIUM_BOUNDS_MICRONS = {
    "x_min": 141.00517302,
    "x_max": 7037.04812383,
    "y_min": 338.76538367,
    "y_max": 5470.49140630,
}
VISIUM_MIN_FULLRES_X = 6097.5

EXPECTED_XENIUM_CELLS = 139_806
EXPECTED_VISIUM_SPOTS = 3_958


def prepare_common_region(
    data_dir: Path,
    output_dir: Path | None = None,
    overwrite: bool = False,
) -> tuple[Path, Path]:
    """Write Xenium and Visium barcode lists for the reconstructed overlap."""

    data_dir = Path(data_dir)
    output_dir = Path(output_dir or data_dir / "paper_common_region")
    output_dir.mkdir(parents=True, exist_ok=True)

    xenium_output = output_dir / "xenium_barcodes.csv.gz"
    visium_output = output_dir / "visium_barcodes.csv.gz"
    if not overwrite and xenium_output.exists() and visium_output.exists():
        return xenium_output, visium_output

    cells_file = data_dir / "cells.csv.gz"
    positions_file = (
        data_dir
        / "visium"
        / "GSM7782699"
        / "spatial"
        / "tissue_positions.csv"
    )
    if not cells_file.exists():
        raise FileNotFoundError(f"Missing Xenium cell metadata: {cells_file}")
    if not positions_file.exists():
        raise FileNotFoundError(f"Missing Visium positions: {positions_file}")

    cells = pd.read_csv(cells_file, index_col=0)
    cells.index = cells.index.astype(str)
    b = XENIUM_BOUNDS_MICRONS
    xenium_mask = (
        cells["x_centroid"].between(b["x_min"], b["x_max"], inclusive="both")
        & cells["y_centroid"].between(
            b["y_min"], b["y_max"], inclusive="both"
        )
    )
    xenium_barcodes = pd.Series(
        cells.index[xenium_mask], name="barcode", dtype="string"
    )

    positions = pd.read_csv(positions_file)
    visium_mask = positions["pxl_col_in_fullres"] >= VISIUM_MIN_FULLRES_X
    visium_barcodes = positions.loc[visium_mask, "barcode"].astype("string")
    visium_barcodes.name = "barcode"

    if len(xenium_barcodes) != EXPECTED_XENIUM_CELLS:
        raise RuntimeError(
            f"Expected {EXPECTED_XENIUM_CELLS:,} Xenium cells, "
            f"found {len(xenium_barcodes):,}. Check the dataset release."
        )
    if len(visium_barcodes) != EXPECTED_VISIUM_SPOTS:
        raise RuntimeError(
            f"Expected {EXPECTED_VISIUM_SPOTS:,} Visium spots, "
            f"found {len(visium_barcodes):,}. Check the dataset release."
        )

    xenium_barcodes.to_frame().to_csv(
        xenium_output, index=False, compression="gzip"
    )
    visium_barcodes.to_frame().to_csv(
        visium_output, index=False, compression="gzip"
    )
    return xenium_output, visium_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("/mnt/data/data_tanevski/xenium_breast"),
        help="Directory containing the original Xenium and Visium files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: DATA_DIR/paper_common_region).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing barcode files.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    outputs = prepare_common_region(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
    )
    print(f"Wrote {outputs[0]}")
    print(f"Wrote {outputs[1]}")
