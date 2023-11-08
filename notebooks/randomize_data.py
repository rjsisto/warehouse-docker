#script used to partially randomize the data

import pandas as pd
import random
from sys import path
path.append("..")
from config import *

sae = pd.read_csv(DATA_FOLDER + '/sae.csv')
cases = pd.read_csv(DATA_FOLDER + "/Cases.csv")
hours = pd.read_csv(DATA_FOLDER + "/hours.csv")

#making sure that the number is not negative
def not_neg(x):
    if(x <= 0):
        return 1
    else:
        return x


#using the standard deviation for the min/max range of each new column 
eaches_std = int(cases["EACHES_SELECTED"].std())

eaches = cases["EACHES_SELECTED"]
eaches = list(eaches)


new_eaches = []
for x in eaches: 
    new_eaches.append(random.randrange(not_neg(x - eaches_std), x+eaches_std))

new_cases = cases
new_cases["EACHES_SELECTED"] = new_eaches


#doing the same for hours
cases_std = int(hours["CASES_SELECTED"].std())
hours_std = int(hours["MEASURED_DIRECT_HRS"].std())

cases_sel = list(hours["CASES_SELECTED"])
hours_sel = list(hours["MEASURED_DIRECT_HRS"])

new_cases_sel = []
new_hours_sel = []
for x,y in zip(cases_sel, hours_sel):
    x = int(x)
    y = int(y)
    new_cases_sel.append(random.randrange(not_neg(x-cases_std), x+cases_std))
    new_hours_sel.append(random.randrange(not_neg(y-hours_std), y+hours_std))

new_hours = hours
new_hours["CASES_SELECTED"] = new_cases_sel
new_hours["MEASURED_DIRECT_HRS"] = new_hours_sel

#writing the new datasets to files
new_hours.to_csv(DATA_FOLDER + "/random_hours.csv")
new_cases.to_csv(DATA_FOLDER + "/random_cases.csv")
