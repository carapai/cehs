import geopandas as gpd
import pandas as pd
from store import Database

shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")

pop = Database().get_population_data()

pop_tgt = Database().get_population_target()

static = {"population data": pop, "target population type": pop_tgt}
