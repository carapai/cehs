# from COC_dashboard import data_story
# from demo_v1 import data_story


import sys
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

sys.path.insert(0, "./coc-dashboard")

from callbacks import define_callbacks  # NOQA: E402
from view import ds  # NOQA: E402

server = ds.app.server


define_callbacks(ds)

if __name__ == "__main__":
    ds.run(dev=False)
else:
    ds.set_layout_and_callbacks()
