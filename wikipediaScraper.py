import wikipedia
import os
import sys
import argparse
import inspect

def slugify(value):
    import unicodedata
    import re
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def findAnotherSubject(subjects):
    isAlreadyInList = True
    while isAlreadyInList:
        subject = wikipedia.random()
        try:
            next(x for x in subjects if x == subject)
        except StopIteration:
            isAlreadyInList = False
    return subject

parser = argparse.ArgumentParser(description='Scrape a certain number of random articles in different languages from Wikipedia.')

parser.add_argument("-l", "--languages", nargs= '*', default=['en', 'es', 'fr', 'it', 'de'], help="List of languages to scrape. \n All the supported languages : {}".format(wikipedia.languages()))
parser.add_argument("-n", "--numberOfArticles", type = int, default = 502, help="the number of articles per languages to scrape.")

args = parser.parse_args()

languages = args.languages

numberOfArticles = args.numberOfArticles

print("languages = {}".format(languages), "number of articles = {}".format(numberOfArticles))

DATA_PATH = "{0}\\data".format(sys.path[0])
for language in languages:
    wikipedia.set_lang(language)
    langPath = "{0}\\{1}".format(DATA_PATH,language)
    if not os.path.exists(langPath):
        os.makedirs(langPath)
    numberOfSubjects = numberOfArticles-len(os.listdir(langPath))
    if numberOfSubjects:
        subjects = wikipedia.random(numberOfSubjects)
        i = len(os.listdir(langPath))
        sys.stdout.write(language + "\n")
        sys.stdout.flush()
        for subject in subjects:
            isInvalidPageId = True
            while isInvalidPageId:
                try:
                    title = u''.join(subject).encode('ascii', errors='ignore').strip()
                    if not title:
                        raise ValueError('Title should not be empty')
                    article = wikipedia.page(title=title)
                    isInvalidPageId = False
                except wikipedia.exceptions.DisambiguationError as e:
                    if e.options:
                        if e.options[0] and e.options[0] != subject:
                            subject = e.options[0]
                        else:
                            subject = findAnotherSubject(subjects)
                except Exception as e:
                    subject = findAnotherSubject(subjects)

            filename = u"{0}\\{1}.txt".format(langPath, slugify(subject))
            with open(filename, 'w+', encoding= 'utf-8') as file:
                file.write(article.content)
            if os.stat(filename).st_size != 0:
                sys.stdout.write("\r{0}/{1}".format(i,numberOfArticles))
                i = i + 1
                sys.stdout.flush()
            else:
                os.remove(filename)