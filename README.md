# Roam Scripts

## Format

### Format iBook Highlights for Roam

Export your highlights by sharing them to your email, then copy the email message here to format it.

Use it: https://pateldhvani.com/format/ibooks

Running locally:

`python -m http.server`

## Meta

### Time Tracking

Make sure each parent bullet has a start and end timestamp, eg. `"08:30 - 09:28: Reading."`.

This script will then generate a line graph where the x-axis is time, and the y-axis the amount of minutes spent on a chosen activity.

This script will also generate a word cloud for the text that follows the category, eg. `": learning - speech"`.

### Word Clouds

Make sure each day has the following section:
```
- [[Daily Review]]
    - [[Shower thoughts]]
    - Heart:
    - Mind:
    - Soul:
    - Body:
```

This script will then generate a word cloud from each of these sections across a chosen time frame.

> Dhvani
