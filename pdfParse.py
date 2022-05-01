from pdfminer.high_level import extract_text
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import helperFunctions


def parseResume(filePath, keywords):
    keywords = [word.lower() for word in keywords]
    regex = createRegex(keywords)

    # stopwordsToStrip = stopwords.words('english')

    extractedText = extract_text(filePath)
    extractedText = extractedText.replace(",", "").lower()

    # sentences = sent_tokenize(extractedText)

    keywordsFound = []

    splitText = splitTextByLinebreak(extractedText)
    for line in splitText:
        match = re.search(regex, line)
        if match:
            keywordsFound.append({"keyword": match.group(), "sentence": line})

    return keywordsFound


def splitTextByLinebreak(inputText):
    # Split the text into lines - The split point would be a linebreak '\n'
    splitText = inputText.splitlines()
    # splitText = inputText.split(". ")

    splitText = filter(None, splitText)

    return splitText


def createRegex(keywords):
    regex = r''
    firstKeyword = True
    for keyword in keywords:
        if firstKeyword:
            firstKeyword = False
            regex += keyword
        else:
            regex += f"|{keyword}"

    return regex


if __name__ == "__main__":

    parseResume("temp", ["Cyber", "authentication", "React", "SQL", "Docker"])
