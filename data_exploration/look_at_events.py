import pandas as pd
import os

path = os.path.join('data','movebank','gps_events_s1470245419_i1509785865_ss653.csv')

data = pd.read_csv(path)

data