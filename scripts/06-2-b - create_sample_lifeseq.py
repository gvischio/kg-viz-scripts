import pandas as pd

cxts = pd.read_csv("06 - Parsed datasets/02 - Parsed locations/context_event.csv")
cxts = cxts[cxts['what'] == "Lesson"]
cxts = cxts.sample(40)
cxts['lsID'] = "LS1"
cxts['name'] = "KDI lectures"
cxts['descr'] = "All the lectures from KDI"
cxts = cxts[['lsID', 'name', 'descr', 'contextID']]
cxts.to_csv("06 - Parsed datasets/02 - Parsed locations/life_sequences.csv", index=False)