import sys
from package.components.nested_dropdown_group import NestedDropdownGroup

sys.path.insert(0, "./coc-dashboard")

indicator_group = pd.read_csv("./coc-dashboard/data/groups.csv")

indicator_dropdown_group = NestedDropdownGroup(
    indicator_group, title="Select an indicator"
)

print(indicator_dropdown_group.dropdown_ids)
