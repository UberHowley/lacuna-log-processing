#!/usr/bin/env python

__author__ = 'IH'
__project__ = 'analyzeLacuna'

import csv
from collections import defaultdict
from NoteInstance import NoteInstance
from topicModelLDA import LDAtopicModel as ldat
import re, math
from collections import Counter

# User Inputs
NUM_LDA_TOPICS = 15  # default number of topics in topic model
MIN_NUM_LDA_TOPICS = 5 # starting number of topics, if greater than MAX, uses default
MAX_NUM_LDA_TOPICS = 40  # set to less than MIN if only want default number

# LOGFILE NAMES
FILENAME_LOGFILE="combined_final_codes.csv"
FILENAME_OUTFILE="combined_final_codes_sim.csv"

# TEXT-RELATED VARIABLES
CONST_DELIMITER = ","
COL_HEADERS = []  # the headers of the file
COL_COUNT = "line_count"
COL_TINDEX = "LDAtopic_index"
COL_TOPIC = "LDAtopic"
COL_SIM = "similarity"

list_headers = [] # a list of the original input headers
list_all_lines = [] # a list of NoteInstance of every line
list_passage_sentences = []  # a list of a list of all words in passages
list_note_sentences = []  # a list of a list of all words in annotations

def run():
    """
    Read in our file.
    :return: None
    """
    # Writing out to file
    outfile_out = open(FILENAME_OUTFILE, 'w', encoding="utf8")

    print("Processing "+FILENAME_LOGFILE)

    count_lines = 0
    with open(FILENAME_LOGFILE,'r', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=CONST_DELIMITER)

        for line in csvreader:
            #line = line.replace(CONST_DELIMITER, ' ')  # Replace all occurrences of delimiter with empty space
            #array_line = line.split(CONST_DELIMITER)

            # first line is headers, only store following lines
            if (count_lines > 0):
                # TODO: Make it so clean_string() isn't needed, look into CSV writing.
                # TODO: Currently stripping all punctuation out!
                txt_noteid = line[0]
                txt_uid = line[1]
                txt_passage = ldat.clean_string(line[2])
                txt_note = ldat.clean_string(line[3])
                txt_title = line[4]
                txt_setting = line[5]
                txt_compcrit = line[6]
                txt_strategy = line[7]
                txt_notes = ldat.clean_string(line[8])
                txt_calculated=line[9]
                txt_combined = line[10]

                # create new Note Instance
                note_instance = NoteInstance(txt_noteid, txt_uid,txt_passage, txt_note, txt_title, txt_setting, txt_compcrit, txt_strategy,txt_notes, txt_calculated,txt_combined, count_lines)

                # adding text to our topic model dictionary
                list_passage_sentences.append(ldat.to_bow(ldat.clean_string(txt_passage)))
                list_note_sentences.append(ldat.to_bow(ldat.clean_string(txt_note)))

                # Convert strings to vectors
                #vector1 = text_to_vector(txt_passage)
                #vector2 = text_to_vector(txt_note)
                vector1 = Counter(ldat.to_bow(txt_passage))
                vector2 = Counter(ldat.to_bow(txt_note))
                # Calculate similarity between note and passage
                cosine = get_cosine(vector1, vector2)

                note_instance.set_similarity(cosine)
                list_all_lines.append(note_instance)
            else:
                list_headers = line
                list_headers.append(COL_COUNT)
                list_headers.append(COL_SIM)
                for num_topic in range(MIN_NUM_LDA_TOPICS, MAX_NUM_LDA_TOPICS):
                    list_headers.append(COL_TINDEX+str(num_topic))
                    list_headers.append(COL_TOPIC+str(num_topic))
            count_lines +=1

    outfile_out.write(str(list_headers) + '\n')

    # topic modeling
    """
    if MAX_NUM_LDA_TOPICS <= MIN_NUM_LDA_TOPICS:
        MIN_NUM_LDA_TOPICS = NUM_LDA_TOPICS
        MAX_NUM_LDA_TOPICS = NUM_LDA_TOPICS+1
    """

    for num_topics in range(MIN_NUM_LDA_TOPICS, MAX_NUM_LDA_TOPICS):
        lda = None
        lda = ldat(num_topics, list_note_sentences)
        for note_instance in list_all_lines: # assigns many topics depending on MAX LDA TOPICS
            # assign LDA topic
            topic_name = lda.predict_topic(ldat.clean_string(note_instance.get_note())) # returns a tuple if you don't manually name it yourself!
            name_cleaned = topic_name.replace("(","")
            name_cleaned = name_cleaned.replace(")", "")
            note_instance.add_topic(name_cleaned)

    for note_instance in list_all_lines: # print each instance now
        # write this instance to file
        outfile_out.write(note_instance.to_string(delimiter=CONST_DELIMITER) + '\n')

    outfile_out.close()
    print("Done writing " + FILENAME_OUTFILE)

def get_topic_match(sentence):
    """
    Find what the topic match percentage was given the topic match sentence
    :param sentence: the relevant sentence containing topic match info
    :return: topic match percentage
    """
    tm = sentence[len(sentence)-7:len(sentence)-1]
    tm = float(tm.strip("abcdefghijklmnopqrstuvwxyz% "))
    if tm < 1:  # Turning decimals into percentage numbers
        tm = tm*100
    return str(tm)

def get_cosine(vec1, vec2):
    """"
    Calculates cosine similarity between two vectors of words.
    Does not remove stop words or handle stemming or any advanced stuff.

    Code from http://stackoverflow.com/questions/15173225/how-to-calculate-cosine-similarity-given-2-sentence-strings-python
    More on cosine similarity: https://en.wikipedia.org/wiki/Cosine_similarity
    :param vec1: first vector to compare
    :param vec2: second vector to compare against vec1
    :return: cosine similarity
    """
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

'''
So that logfileLacuna can act as either a reusable module, or as a standalone program.
'''
if __name__ == '__main__':
    print("Running logfileLacuna")
    run()