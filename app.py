# from COC_dashboard import data_story
# from demo_v1 import data_story
import sys

sys.path.insert(0, "./coc-dashboard")

from view import ds

server = ds.app.server

if __name__ == "__main__":
    ds.run(dev=True)
else:
    ds.set_layout_and_callbacks()