import geopandas as gpd
import pandas as pd

shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")

pop = pd.read_csv(
    "./coc-dashboard/data/pop.csv",
    header=None,
    names=["district", "year", "male", "female", "total", "age"],
    dtype={
        "district": str,
        "year": int,
        "male": int,
        "female": int,
        "total": int,
        "age": str,
    },
)

pop_tgt = pd.read_csv(
    "./coc-dashboard/data/target_pop.csv",
    dtype={"indicator": str, "ages": str, "sex": str},
)

static = {"population data": pop, "target population type": pop_tgt}
