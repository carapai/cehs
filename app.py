# from COC_dashboard import data_story
# from demo_v1 import data_story


import sys

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

sys.path.insert(0, "./coc-dashboard")

from callbacks import define_callbacks  # NOQA: E402
from view import ds  # NOQA: E402

server = ds.app.server

ds._define_callbacks()
define_callbacks(ds)
ds._set_layout()

if __name__ == "__main__":
    ds.app.run_server(debug=True)
