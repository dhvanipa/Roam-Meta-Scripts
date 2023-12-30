
import json
import string

from datetime import timedelta
from dateutil.parser import parse

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from helper import parseTimeBlock, getTimeDelta, getTimeStr, getTimeRange

# Load Roam graph
print("Loading Roam graph...")
with open('../data/database.json') as f:
    allPages = json.load(f)
print("Loaded!")

# Setup
(chosenYear, chosenTrimester, chosenTrimesterName, startTermDate, endTermDate) = getTimeRange()

categories = {
    "shower thoughts": "",
    "heart": "",
    "mind": "",
    "soul": "",
    "body": "",
}

stopwords = set(STOPWORDS)

pageCount = 0

for page in allPages:
    pageTitle = page.get("title")

    try:
        # Filter out daily pages
        dailyPage = parse(pageTitle)
        dailyPage = dailyPage.date()

        # Filter time range selected
        if dailyPage >= startTermDate and dailyPage <= endTermDate:
            notes = page.get("children")
            if notes is not None:
                for note in notes:
                    # Filter out Daily Review bullet
                    parentTitle = note.get("string")
                    if parentTitle == "[[Daily Review]]":
                        reviewalNotes = note.get("children")
                        if reviewalNotes is not None:
                            # print(reviewalNotes)
                            for reviewNote in reviewalNotes:
                                # Filter out Shower Thoughts bullet
                                reviewNoteTitle = reviewNote.get("string")
                                if reviewNoteTitle == "[[Shower thoughts]]":
                                    showerNotes = reviewNote.get("children")
                                    if showerNotes is not None:
                                        # print("Shower thoughts")
                                        showerThoughtsText = categories.get("shower thoughts")
                                        for showerNote in showerNotes:
                                            showerThoughtsText += " " + showerNote.get("string")
                                        categories["shower thoughts"] = showerThoughtsText
                                elif reviewNoteTitle == "Heart:":
                                    heartNotes = reviewNote.get("children")
                                    if heartNotes is not None:
                                        # print("Heart review")
                                        heartReviewText = categories.get("heart")
                                        for heartNote in heartNotes:
                                            heartReviewText += " " + heartNote.get("string")
                                        categories["heart"] = heartReviewText
                                elif reviewNoteTitle == "Mind:":
                                    mindNotes = reviewNote.get("children")
                                    if mindNotes is not None:
                                        # print("Mind review")
                                        mindReviewText = categories.get("mind")
                                        for mindNote in mindNotes:
                                            mindReviewText += " " + mindNote.get("string")
                                        categories["mind"] = mindReviewText
                                elif reviewNoteTitle == "Soul:":
                                    soulNotes = reviewNote.get("children")
                                    if soulNotes is not None:
                                        # print("Soul review")
                                        soulReviewText = categories.get("soul")
                                        for soulNote in soulNotes:
                                            soulReviewText += " " + soulNote.get("string")
                                        categories["soul"] = soulReviewText
                                elif reviewNoteTitle == "Body:":
                                    bodyNotes = reviewNote.get("children")
                                    if bodyNotes is not None:
                                        # print("Body review")
                                        bodyReviewText = categories.get("body")
                                        for bodyNote in bodyNotes:
                                            bodyReviewText += " " + bodyNote.get("string")
                                        categories["body"] = bodyReviewText
            pageCount += 1
    except:
        continue

print("-"*10)
print("Analyzed: " + str(pageCount) + " pages")
print("-"*10)

while True:
    # Let user pick a category
    chosenCategory = input("Choose a category (shower thoughts, heart, mind, soul, body) or exit: ")
    while chosenCategory not in categories.keys() and chosenCategory != "exit":
        print("Invalid activity chosen")
        chosenCategory = input("Choose a category (shower thoughts, heart, mind, soul, body) or exit: ")

    if chosenCategory == "exit":
        break

    wordCloudText = categories.get(chosenCategory).translate(str.maketrans('', '', string.punctuation))
    # print(wordCloudText)
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
    plt.title("Word Cloud For: " + chosenCategory)
    plt.tight_layout(pad = 0)
    plt.draw()
    plt.pause(1)