
import json
import string

from datetime import date, datetime, timedelta
from calendar import month_abbr, monthrange
from dateutil.parser import parse

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from helper import parseTimeBlock, getTimeDelta, getTimeStr

# Load Roam graph
with open('../data/database.json') as f:
    allPages = json.load(f)

# Setup

# Map month to number of days
months = {month: index for index, month in enumerate(month_abbr) if month}

# Start - End months
winterTerm = ("Jan", "Apr")
springTerm = ("May", "Aug")
fallTerm = ("Sep", "Dec")

year = {"2020": 2020, "2021": 2021}
trimesters = {"winter": winterTerm, "spring": springTerm, "fall": fallTerm}

# Get input
chosenYear = input("Enter year (2020, 2021): ")
while chosenYear not in year:
    print("Invalid year chosen")
    chosenYear = input("Enter year (2020, 2021): ")

chosenTrimester = input("Enter trimester (winter, spring, fall): ")
while chosenTrimester not in trimesters:
    print("Invalid trimester chosen")
    chosenTrimester = input("Enter trimester (winter, spring, fall): ")
chosenTrimesterName = chosenTrimester.capitalize()
chosenTrimester = trimesters.get(chosenTrimester)

startTermDate = date(
    int(chosenYear),
    months.get(chosenTrimester[0]),
    1)

endTermDate = date(
    int(chosenYear),
    months.get(chosenTrimester[1]),
    monthrange(int(chosenYear), months.get(chosenTrimester[1]))[1])

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