#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_json("results.json")

plt.plot('time:', 'state', data=df)
plt.show()
