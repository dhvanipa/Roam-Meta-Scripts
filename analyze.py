import json

with open('data/database.json') as f:
  allPages = json.load(f)

summer_term = ("May", "June", "July", "August")

time_range = summer_term
year = "2020"
    
page_count = 0
for page in allPages:    
    pageTitle = page.get("title")    
    if pageTitle.startswith(time_range) and pageTitle.endswith(year):
        print(page.get("title"))      
        page_count += 1      

print("-----------")
print("Analyzed: " + str(page_count) + " pages")