import geopandas as gpd
import pandas as pd

shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")

pop = pd.read_csv("./coc-dashboard/data/pop.csv")

pop_tgt = pd.read_csv(
    "./coc-dashboard/data/target_pop.csv",
    dtype={"indicator": str, "cat": str},
)

static = {"population data": pop, "target population type": pop_tgt}
