import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Input your text for summarizing below:

def summary(text):


    # Next, you need to tokenize the text:

    stopWords = set(stopwords.words("arabic"))
    words = word_tokenize(text)

    # Now, you will need to create a frequency table to keep a score of each word:

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Next, create a dictionary to keep the score of each sentence:

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Now, we define the average value from the original text as such:

    average = int(sumValues / len(sentenceValue))

    # And lastly, we need to store the sentences into our summary:

    summary = ''

    for sentence in sentences:

        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    # print(summary)
    return(summary)

