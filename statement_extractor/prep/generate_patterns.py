# -*- coding: utf-8 -*-
from os.path import dirname, realpath
from os import listdir
from sys import exit
import re, pickle
directory_of_this_file = dirname(realpath(__file__))
directory_of_keywords = directory_of_this_file + "/keywords"
directory_of_patterns = directory_of_this_file + "/patterns"

# load keywords from files into dictionary
language_keyword_pattern = {}
for filename in listdir(directory_of_keywords):
    language = filename.split(".")[0]
    print "language is", language

    path_to_keywords_file = directory_of_keywords + "/" + filename

    with open(path_to_keywords_file) as f:
        keywords = f.read().decode("utf-8").splitlines()

        # sort keywords by length, because we want to match the longest ones first
        # wouldn't want to accidentaly match say instead of saying
        keywords = sorted(keywords, key=lambda x: -1*len(x))

    pattern = u"(?P<keyword>" + u"|".join(keywords) + u")"
    language_keyword_pattern[language] = pattern


language_statement_pattern = {}
#######################################################
##########################       English
################################################
keyword = language_keyword_pattern['English']
print "keyword is", keyword
speaker = "(?P<speaker>[A-Za-z]+)"
#quote = """(?:"|')(?P<quote>[^\"']*),?(?:"|')"""
#quote = """("|')(?P<quote>[^\"']*),?\1"""
#quote = """(?P<qchar>"|')(?P<quote>[^(?P=qchar)]*)(?<!,),?(?P=qchar)"""
#quote = """(?P<qchar>"|')(?P<quote>[^(?P=qchar)]*),?(?P=qchar)"""

# I added a question mark after {3,100} to make the previous pattern not greedy
# which means that the quote ends as soon as we hit another qchar
# \u201c is left quote
#quote = """(?P<qchar>"|'|\u201c)(?P<quote>[^\n\r\t]{3,1000}?),?(?P=qchar)"""
quote = u"""(?P<qchar>"|'|(?P<ldquo>\u201c))(?P<quote>[^\n\r\t]{3,1000}?),?(?(ldquo)(?:\u201d)|(?P=qchar))"""
skq = speaker.replace("speaker","speaker_skq") + " " + keyword.replace("keyword","keyword_skq") + " " + quote.replace("quote","quote_skq").replace("qchar","qchar_skq").replace("ldquo","ldquo_skq")
qsk = quote.replace("quote","quote_qsk").replace("qchar","qchar_qsk").replace("ldquo","ldquo_qsk") + ",? " + speaker.replace("speaker","speaker_qsk") + " " + keyword.replace("keyword","keyword_qsk")
statement = "(?:" + skq + "|" + qsk + ")"
#statement = "(?P<statement>" + skq + "|" + qsk + ")"
language_statement_pattern['English'] = statement
print "statement = '''" + statement + "'''"

###########################################
###########            ARABIC
##########################################
#keyword = language_keyword_pattern['Arabic']
#print "keyword is", keyword
#pattern = u"(?:" + keyword + u"(?: (?:(?:\u0648?\u0627\u0644[^ .,\u060c\n\r<\";]*)|\u0641\u064a|(?:\u0628[^ .,\u060c\n\r<\"\u200e;]*)))+)(?<!\u0641\u064a)"
#language_statement_pattern['Arabic'] = pattern


# write all patterns to their respective files
for language, pattern in language_statement_pattern.iteritems():
    with open(directory_of_patterns + "/" + language + ".txt", "wb") as f:
        f.write(pattern.encode("utf-8"))
