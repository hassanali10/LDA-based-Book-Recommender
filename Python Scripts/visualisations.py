# Load the Pandas libraries with alias 'pd'
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
plt.close("all")

os.chdir("../../../task")
print(os.listdir(os.getcwd()))
items = pd.read_csv("items.csv", sep="|")
sessions = pd.read_csv("transactions.csv", sep="|")
eval = pd.read_csv("evaluation.csv", sep="|")

# Sessions
print("Einträge sessions: ", len(sessions))
items_looked_at = sessions.groupby("sessionID").size()
print("verschiedene SessionIDs: ", len(items_looked_at))
print("---------------items looked at in one session-----------------")
print("max: ", items_looked_at.max(), "\nmin: ", items_looked_at.min(),
      "\navg: ", items_looked_at.mean())
items_looked_at_size = pd.DataFrame(items_looked_at)
items_looked_at_size.groupby(0).size().plot(logy=True)
plt.title('Verteilung angeschaute Titel pro Session')
# print(items_looked_at_size.groupby(0).size())
plt.show()


# evaluation
eval_info_left = pd.merge(eval, sessions, how="left", on="itemID")
eval_info_left = pd.merge(eval_info_left, items, how="left", on="itemID")
eval_info_inner = pd.merge(eval, sessions, how="inner", on="itemID")
eval_info_inner = pd.merge(eval_info_inner, items, how="left", on="itemID")
print("---------------evaluation left join items-----------------")
print(eval_info_left.describe())
items_without_session = eval_info_left["itemID"].count() - eval_info_inner["itemID"].count()
print("items without session: ", items_without_session)
print("items with session: ", 1000 - items_without_session)

eval_session_count = eval_info_left.groupby("itemID").count().sort_values("click", ascending=False)
eval_session_count.head(10).plot.bar(y='sessionID', logy=False)
eval_session_sum = eval_info_left.groupby("itemID").sum()
print(eval_session_count.describe())
print(eval_session_sum.describe())
plt.title('Anzahl Sessions pro Titel (nur für Titel in eval)')
plt.show()

test = eval_session_sum.sort_values('click', ascending=False)
print(test.head(10))

