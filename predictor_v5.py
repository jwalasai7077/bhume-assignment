from bhume import load, write_predictions, score

import numpy as np

from shapely.affinity import translate

import geopandas as gpd


def main():

    village = load("../vadnerbhairav")

    dxs = []
    dys = []

    print("Computing village drift...")

    for pn in village.example_truths.index:

        official = village.plot(pn)

        truth = village.example_truths.loc[pn, "geometry"]

        dx = truth.centroid.x - official.centroid.x
        dy = truth.centroid.y - official.centroid.y

        dxs.append(dx)
        dys.append(dy)

    median_dx = np.median(dxs)
    median_dy = np.median(dys)

    print("Median DX:", median_dx)
    print("Median DY:", median_dy)

    preds = village.plots.copy()

    preds["geometry"] = preds.geometry.apply(
        lambda g: translate(
            g,
            xoff=median_dx,
            yoff=median_dy
        )
    )

    preds["status"] = "corrected"

    preds["confidence"] = 0.65

    preds["method_note"] = (
        f"median shift "
        f"dx={median_dx:.8f} "
        f"dy={median_dy:.8f}"
    )

    output = write_predictions(
        "../vadnerbhairav/predictions_v5.geojson",
        preds
    )

    print("\nSaved:", output)

    print()
    print(score(preds, village))


if __name__ == "__main__":
    main()