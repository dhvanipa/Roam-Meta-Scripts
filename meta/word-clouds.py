import json
import string

from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 

with open('data/database.json') as f:
    allPages = json.load(f)

summerTerm = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

timeRange = summerTerm

year = "2020"

pageCount = 0

showerThoughtsText = ""
heartReviewText = ""
mindReviewText = ""
soulReviewText = ""
bodyReviewText = ""

stopwords = set(STOPWORDS) 

for page in allPages:
    pageTitle = page.get("title")

    # Filter out daily pages
    if pageTitle.startswith(timeRange) and pageTitle.endswith(year):
        # print(page.get("title"))
        notes = page.get("children")                       

        # If page isn't empty
        if notes is not None:
            for note in notes:     
                # Filter out Daily Review bullet                     
                parentTitle = note.get("string")            
                if parentTitle == "[[Daily Review]]":                                        
                    reviewalNotes = note.get("children")
                    if reviewalNotes is not None:                        
                        for reviewNote in reviewalNotes:
                            # Filter out Shower Thoughts bullet    
                            reviewNoteTitle = reviewNote.get("string")                            
                            if reviewNoteTitle == "[[Shower thoughts]]":
                                showerNotes = reviewNote.get("children")
                                if showerNotes is not None:
                                    # print("Shower thoughts")
                                    for showerNote in showerNotes:
                                        showerThoughtsText += " " + showerNote.get("string")
                            elif reviewNoteTitle == "Heart:":
                                heartNotes = reviewNote.get("children")
                                if heartNotes is not None:
                                    # print("Heart review")
                                    for heartNote in heartNotes:
                                        heartReviewText += " " + heartNote.get("string")
                            elif reviewNoteTitle == "Mind:":
                                mindNotes = reviewNote.get("children")
                                if mindNotes is not None:
                                    # print("Mind review")
                                    for mindNote in mindNotes:
                                        mindReviewText += " " + mindNote.get("string")
                            elif reviewNoteTitle == "Soul:":
                                soulNotes = reviewNote.get("children")
                                if soulNotes is not None:
                                    # print("Soul review")
                                    for soulNote in soulNotes:
                                        soulReviewText += " " + soulNote.get("string")
                            elif reviewNoteTitle == "Body:":
                                bodyNotes = reviewNote.get("children")
                                if bodyNotes is not None:
                                    # print("Body review")
                                    for bodyNote in bodyNotes:
                                        bodyReviewText += " " + bodyNote.get("string")

            pageCount += 1        

print("-----------")
print("Analyzed: " + str(pageCount) + " pages")

# SWAP OUT THE TEXT HERE
wordCloudText = showerThoughtsText

wordCloudText = wordCloudText.translate(str.maketrans('', '', string.punctuation))
print(wordCloudText)
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white',
                collocations=False,
                stopwords = stopwords,
                relative_scaling=0.5
                ).generate(wordCloudText) 
  
# plot the WordCloud image                    
plt.figure(figsize = (8, 7), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()
