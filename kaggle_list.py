#!/usr/bin/env python
import os

os.environ["KAGGLE_USERNAME"] = "backupsonbackupsrobby-cyber"
os.environ["KAGGLE_KEY"] = "KGAT_bb4030a949969eca4009e86b404ea4cb"

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

# Get active competitions
comps = api.competitions_list()
print(f"Total competitions: {len(comps)}\n")
print("ACTIVE COMPETITIONS:")
print("=" * 80)
for i, c in enumerate(comps[:15], 1):
    print(f"{i}. {c.ref}")
    print(f"   Title: {c.title}")
    print(f"   Deadline: {c.deadline}")
    print(f"   Teams: {c.number_of_teams}")
    print()
