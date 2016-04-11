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
proper_noun = "(?:[A-Z][a-z]{2,15})(?: [A-Z][a-z]{2,15})*"
speaker = "(?P<speaker>" + proper_noun + "|[A-Za-z]+)"
word = "(?:[A-Z]?[a-z]{1,15})"
words = "(?: " + word + ")*"
#quote = """(?:"|')(?P<quote>[^\"']*),?(?:"|')"""
#quote = """("|')(?P<quote>[^\"']*),?\1"""
#quote = """(?P<qchar>"|')(?P<quote>[^(?P=qchar)]*)(?<!,),?(?P=qchar)"""
#quote = """(?P<qchar>"|')(?P<quote>[^(?P=qchar)]*),?(?P=qchar)"""

# I added a question mark after {3,100} to make the previous pattern not greedy
# which means that the quote ends as soon as we hit another qchar
# \u201c is left quote
#quote = """(?P<qchar>"|'|\u201c)(?P<quote>[^\n\r\t]{3,1000}?),?(?P=qchar)"""
#quote = u"""(?P<qchar>"|'|(?P<ldquo>\u201c))(?P<quote>[^\n\r\t]{3,1000}?),?(?(ldquo)(?:\u201d)|(?P=qchar))"""
#quote = u"""(?P<qchar>"|'|(?P<ldquo>\u201c|&ldquo;))(?P<quote>[^\n\r\t]{3,1000}?),?(?(ldquo)(?:\u201d|&rdquo;)|(?P=qchar))"""
# we put the " as an unacceptable character inside the quote; don't think I've ever seen this inside a quote
# so probably okay and it helps make sure that we don't capture parts of surrounding tags
# we added that weird (?=[^>]) because weird case where getting part of tag and starting with >
quote = u"""(?P<qchar>\u0022|"|'|&quot;|(?P<lchar>\u201c|&ldquo;))(?=[^>])(?P<quote>[^\n\r\t\"]{3,1000}?),?(?(lchar)(?:\u201d|&rdquo;)|(?P=qchar))"""
#skq = speaker.replace("speaker","speaker_skq") + " " + keyword.replace("keyword","keyword_skq") + "(?: [A-Za-z]{3,10})? " + quote.replace("quote","quote_skq").replace("qchar","qchar_skq").replace("ldquo","ldquo_skq")
# make sure in doesn't proceed speaker; this often happens when s is actually a place
# make sure speaker isn't actually part of a word
#skq = "(?<!in )(?<![A-Za-z])" + speaker.replace("speaker","speaker_skq") + "(?:, [^,]+,)? " + keyword.replace("keyword","keyword_skq") + "(?: [A-Za-z]{3,10})?,? " + quote.replace("quote","quote_skq").replace("qchar","qchar_skq").replace("lchar","lchar_skq")
skq = "(?<!in )(?<![A-Za-z])" + speaker.replace("speaker","speaker_skq") + "(?:, [^,]+,)? " + keyword.replace("keyword","keyword_skq") + words + ",? " + quote.replace("quote","quote_skq").replace("qchar","qchar_skq").replace("lchar","lchar_skq")
qsk = quote.replace("quote","quote_qsk").replace("qchar","qchar_qsk").replace("lchar","lchar_qsk") + ",? " + speaker.replace("speaker","speaker_qsk") + " " + keyword.replace("keyword","keyword_qsk")
statement = "(?:" + skq + "|" + qsk + ")"
#statement = "(?P<statement>" + skq + "|" + qsk + ")"
language_statement_pattern['English'] = statement
print "statement = '''" + statement + "'''"

###########################################
###########            ARABIC
##########################################
arabic_keyword = language_keyword_pattern['Arabic'].replace("keyword","keyword_arabic")
print "keyword is", [arabic_keyword]
wa = u"\u0648"
al = u"\u0627\u0644"
letter = u"[^)( .,\u060c\n\r<\";\u200e]"
word = letter + u"{3,15}"
words = "(?: " + word + ")*"
speaker = "(?P<speaker_arabic>" + word + ")"
arabic_statement = "(?:" + wa+"?" + arabic_keyword + " " + speaker + words + " " + quote.replace("quote","quote_arabic").replace("qchar","qchar_arabic").replace("lchar","lchar_arabic") + ")"
print "arabic regex statement is"
print [arabic_statement]
language_statement_pattern['Arabic'] = arabic_statement


# write all patterns to their respective files
for language, pattern in language_statement_pattern.iteritems():
    with open(directory_of_patterns + "/" + language + ".txt", "wb") as f:
        f.write(pattern.encode("utf-8"))
