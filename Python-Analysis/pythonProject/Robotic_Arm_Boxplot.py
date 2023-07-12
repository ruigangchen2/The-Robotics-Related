import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ptitprince as pt

df = pd.read_excel("./20230712/final.xlsx")

dy="group"
dx="Final Angle (º)"

f, ax=plt.subplots(figsize=(10, 8))
ax=pt.half_violinplot(x=dx, y=dy, data=df, palette="Set2", bw=.2, cut=0.,
                      scale="area", width=.2, inner=None, orient="h")
ax=sns.stripplot(x=dx, y=dy, data=df, palette="Set2", edgecolor="white",
                 size=7, jitter=1, zorder=0, orient="h")
ax=sns.boxplot(x=dx, y=dy, data=df, color="black", width=.15, zorder=10,
              showcaps=True, boxprops={'facecolor':'none',"zorder":10},
              showfliers=True, whiskerprops={'linewidth':2,"zorder":10},
              showmeans=True, meanline=True, meanprops={'marker': 'D', 'markerfacecolor': 'white'},
              saturation=1, orient="h",)
plt.grid()
plt.title("Raincloud")
plt.show()

