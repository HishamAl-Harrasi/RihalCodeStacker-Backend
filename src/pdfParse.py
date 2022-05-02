from pdfminer.high_level import extract_text
import re

# This file contains the functions used in the API application (main.py)
# This is based on parsing the pdf resume file and spliting it line by line,
# and then employs a regular expression based keyword search to find any text
# containing the keywords submitted by the user


def parseResume(filePath, keywords):
    # Create a regex to be used for searching through keywords
    keywords = [word.lower() for word in keywords]
    regex = createRegex(keywords)

    # Extract text from PDF and perform some data cleaning
    extractedText = extract_text(filePath)
    extractedText = extractedText.replace(",", "").lower()

    keywordsFound = []

    splitText = splitTextByLinebreak(extractedText)

    for line in splitText:
        # Search for keyword using the regex in each line
        match = re.search(regex, line)
        if match:
            keywordsFound.append({"keyword": match.group(), "sentence": line})

    return keywordsFound


def splitTextByLinebreak(inputText):
    # Split the text into lines - The split point would be a linebreak '\n'
    splitText = inputText.splitlines()
    splitText = filter(None, splitText)

    return splitText


def createRegex(keywords):
    # Script to create the regex for detecting keywords
    regex = r''
    firstKeyword = True

    for keyword in keywords:
        if firstKeyword:
            firstKeyword = False
            regex += keyword
        else:
            regex += f"|{keyword}"

    return regex
