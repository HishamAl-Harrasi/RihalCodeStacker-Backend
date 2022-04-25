from pdfminer.high_level import extract_text
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

def parseResume(fileName=None, keywords=None):
    keywords = [word.lower() for word in keywords]

    stopwordsToStrip = stopwords.words('english')

    extractedText = extract_text('HishamCV.pdf')
    
    sentences = sent_tokenize(extractedText)
    words = []

    sentencesNoStopWords = []
    for line in sentences:
        # words.append(word_tokenize(line))

        strippedSentence = [word for word in line.split() if word.lower() not in stopwordsToStrip] # Reference: https://bit.ly/3rPXPCO
        for i, word in enumerate(strippedSentence):
            word.replace(",", "")
            strippedSentence[i] = word.lower()
        
        print(Counter(strippedSentence), "\n\n\n")

        regex = createRegex(keywords)

        print(regex)

        regexMatches  = []

        for word in strippedSentence:
            match = re.match(regex, word)
            if match != None:
                regexMatches.append(match)

        test = re.match(regex, extractedText)
        print(test)
        # print(regexMatches)




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




parseResume("temp", ["Computer Science", "CyberSecurity", "React", "Warwick"])

        




