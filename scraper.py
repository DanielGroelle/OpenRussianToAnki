import requests
import csv
from os.path import exists
from time import sleep

# URL = "https://en.openrussian.org/vocab/B1"
baseURL = "https://en.openrussian.org/ru/"
baseAPI = "https://api.openrussian.org/api/"

# == preferences ==
languagelevel = "A1"
#change this to desired language level to scrape from
#(A1, A2, B1, B2, C1, C2)
singletranslationlimit = 2 #refers to the amount of translations you will get for a particular meaning
#ex: счёт - bill, check (same meaning said in different ways)
uniquetranslationlimit = 3 #refers to the amount of different meanings you will get from a word
#ex: стол - table, cuisine, department (all different meanings)
prependto = False #prepends "to" to verbs that do not already have it in their translation, ex: run -> to run
#may cause strange translations for certain words

#create new output file
created = False
index = 1
while(not(created)):
  if(exists("./output" + str(index) + ".csv") == False):
    created = True
    break
  index += 1

outputfile = open("./output" + str(index) + ".csv", "w", encoding="utf-8", newline='')
writer = csv.writer(outputfile)
writer.writerow(["word", "translations", "part of speech", "russian sentence", "english sentence", "pronunciation", "url"])
#this will end up being a card in anki, remember to delete it

outputting = True
startvalue = 0
lastscraped = [] #check against this to prevent duplicates
while outputting:
  page = requests.get(baseAPI + "wordlists/all?level=" + languagelevel + "&lang=en&start=" + str(startvalue))
  page = page.json()
  response = page["result"]["entries"]

  print(startvalue)
  #increment startvalue for next api call (api only returns in groups of 50 words)
  startvalue += 50

  #if empty response, meaning we reached the end of the list
  if (len(response) == 0):
    outputting = False #stops the while loop and finishes the script

  for wordobj in response:
    word = wordobj["bare"]

    #convert the word to its utf8 form for fetching
    linkutf8 = word.encode("utf-8") #start form: b'\xd0\xba\xd1\x83\xd0\xb4'
    linkutf8 = str(linkutf8)
    linkutf8 = linkutf8.split(r"\x")
    linkutf8.pop(0)
    linkutf8[len(linkutf8)-1] = linkutf8[len(linkutf8)-1][0:2]
    linkutf8 = "%".join(linkutf8)
    linkutf8 = "%" + linkutf8
    #end form: %d0%ba%d1%83%d0%b4

    # audio scraping not implemented
    # audio = requests.get("https://api.openrussian.org/read/ru/" + linkutf8)

    #fetch individual word from api
    sleep(.3) #lets be nice to their api
    wordsdata = requests.get(baseAPI + "words?lang=en&bare=" + linkutf8)
    wordsdata = wordsdata.json()
    wordsdata = wordsdata["result"]["words"]

    #this word will be a duplicate so continue on
    if (lastscraped == wordsdata):
      continue

    lastscraped = wordsdata

    #in case there are two words of same spelling but different stress accents
    #such as выходи́ть and вы́ходить
    for worddata in wordsdata:
      #this word is not a part of the level category so continue on
      if (not(worddata["level"] == languagelevel)):
        continue

      pronunciation = worddata["accented"]
      #if the word has an accent mark, apply the unicode accent combining character
      if (pronunciation.find("'") != -1):
        pronunciation = pronunciation.split("'")
        pronunciation = u'\u0301'.join(pronunciation)
      
      partofspeech = worddata["type"]
      if (partofspeech == "verb"):
        partofspeech += " - " + worddata["verb"]["aspect"]
      if (partofspeech == "other"):
        partofspeech = ""

      #print the current word to console
      print(pronunciation + ", " + partofspeech)

      russiansentence = ""
      englishsentence = ""
      #if sentence data exists
      if (len(worddata["sentences"]) != 0):
        sentencedata = worddata["sentences"][0]
        russiansentence = sentencedata["ru"]
        englishsentence = sentencedata["tl"]
        #convert accent marks to unicode accent combining character
        if (russiansentence.find("'") != -1):
          russiansentence = russiansentence.split("'")
          russiansentence = u'\u0301'.join(russiansentence)

      translations = []
      for tlsindex, tls in enumerate(worddata["translations"]):
        if (tlsindex == uniquetranslationlimit):
            break #we hit the unique meanings translation limit
        for tlindex, tl in enumerate(tls["tls"]):
          if (tlindex == singletranslationlimit):
            break #we hit the single meaning translation limit
          translation = tl
          #prepend "to" to words that are verbs and do not already have it, ex: run -> to run
          if (prependto and partofspeech.find("verb") != -1 and partofspeech.find("adverb") == -1 and tl[:2] != "to"):
              translation = "to " + tl
          translations.append(translation)
      translations = ', '.join(str(translation) for translation in translations)

      #append to csv file all the data we processed
      writer.writerow([word, translations, partofspeech, russiansentence, englishsentence, pronunciation, baseURL+word])

outputfile.close()
print("finished")