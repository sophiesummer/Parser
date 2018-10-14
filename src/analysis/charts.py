from src.analysis.analysis import DataAnalysis
import matplotlib.pyplot as plt

data_analysis = DataAnalysis()

# hub_actor
plt.figure(0)
hub_actor_info = data_analysis.hub_actor_connections(20)
plt.barh(list(hub_actor_info.keys()), list(hub_actor_info.values()), color='g')
plt.title("Hub Actors -- Top 20")
plt.show()

# age_gross relation
plt.figure(1)
age_gross_info = data_analysis.age_gross_relation()
plt.bar(list(age_gross_info.keys()), age_gross_info.values(), color='g')
plt.xlabel("age range")
plt.ylabel("gross value")
plt.title("Age-Gross Relation")
plt.show()

# year_gross_relation
plt.figure(2)
year_gross_info = data_analysis.year_gross_relation()
plt.bar(list(year_gross_info.keys()), year_gross_info.values(), color='g')
plt.xlabel("Year range")
plt.ylabel("Gross value")
plt.title("Total Gross of Movies / Year ")
plt.show()