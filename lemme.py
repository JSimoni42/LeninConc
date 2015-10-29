import pymorphy2
import json
import datetime

class lemme:
    '''filename'''
    def __init__(self, filename):
        self.lemmes = list()
        self.lemmesHyphen = list()
        self.filename = filename
        self.morph = pymorphy2.MorphAnalyzer()

    '''returns list of lemmes'''
    def produce_lemmes(self):
        infile = open(self.filename, 'r', encoding = "utf-8")
        for word in infile:  #one word per line.
            word = word.rstrip()
            if '-' in word:
                self.addHyphenWord(word)
            else:
                self.addWord(word)
        infile.close()
        today = datetime.date.today().strftime("%b%d") #Month_day
        outfile = open("outNoHyphen" + today + ".json", 'w', encoding = "utf-8")
        outfileHyph = open("outHyphen" + today + ".json", 'w', encoding = "utf-8")
        json.dump(self.lemmes, outfile)
        json.dump(self.lemmesHyphen, outfileHyph)
        outfile.close()
        outfileHyph.close()

    '''Obtains the grammeme of a word'''
    def getGram(self, word):
        gram = list()
        for g in word.tag.grammemes:
            gram.append(g)
        return gram

    '''Adds hyphenated word to lemma table'''
    def addHyphenWord(self, word):
        output = [word]
        wordParts = word.split('-')
        valid_check = self.validHyphCheck(wordParts)
        valid_parts = valid_check[1]
        whole_valid = valid_check[0]

        if not whole_valid:
            output.append("XXX")
        else:
            output.append(self.lemmaHyphen(wordParts))
        gram_index = 2 #index before which to insert gram information
        for i in range(3):
            if i < len(wordParts):
                if valid_parts[i] == "": #word is valid, produce grammatical info
                    guess = self.morph.parse(wordParts[i])[0]
                    gram = self.getGram(guess)
                    normal = guess.normal_form.upper()
                else:
                    gram = valid_parts[i]
                    normal = wordParts[i]
            else: #word only has one hyphen, need to fill in extra columns to maintain alignment with 2 hyphen words
                gram = " "
                normal = " "
            output.insert(gram_index, gram)
            output.append(normal)
            gram_index += 1
        self.lemmesHyphen.append(output)

    '''Input: parts of hyphenated word, split on the '-'
    Output: A tuple. First half is whether or not all parts are valid words.
        Second half is an array marking which parts are valid using letters XXX, YYY, and ZZZ to
        mark the invalidity of first, second, and third words, respectively'''
    def validHyphCheck(self, wordParts):
        valid_parts = list()
        negChr = ord('X')
        wholeValid = True
        for part in wordParts:
            if not self.morph.word_is_known(part):
                wholeValid = False
                valid_parts.append(chr(negChr)*3)
            else:
                valid_parts.append("")
            negChr += 1
        return (wholeValid, valid_parts)

    '''Input: Parts of a hyphenated word, all of which are valid
    Output: lemmas of those parts, hyphenated together'''
    def lemmaHyphen(self, wordParts):
        guess_tail = self.morph.parse(wordParts[-1])[0]
        lemma_tail = guess_tail.normal_form.upper()
        new_parts = wordParts[:-1]
        new_parts.append(lemma_tail)
        lemmas = "-".join(new_parts)
        return lemmas


    '''Adds words to lemme list'''
    def addWord(self, word):
        if self.morph.word_is_known(word):
            guess = self.morph.parse(word)[0]
            self.lemmes.append([word, guess.normal_form, self.getGram(guess)])
        else:
            self.lemmes.append([word, word, "XXX"])

lemme1 = lemme("LVocabUCyrOnly.txt")
lemme1.produce_lemmes()
