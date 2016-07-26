#!/usr/bin/env python

__author__ = 'IH'
__project__ = 'analyzeLacuna'

import csv
import datetime
import random
from collections import defaultdict
from NoteInstance import NoteInstance
from topicModelLDA import LDAtopicModel as ldat

# User Inputs
NUM_LDA_TOPICS = 15  # number of topics in topic model

# LOGFILE NAMES
FILENAME_LOGFILE="combined_final_codes.csv"
FILENAME_OUTFILE="combined_final_codes_sim.csv"

# TEXT-RELATED VARIABLES
CONST_DELIMITER = ","
COL_HEADERS = []  # the headers of the file
COL_PASSAGE = "passage"
COL_NOTE = "annotation"
COL_SIM = "similarity"
COL_TOPIC = "LDAtopic"

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

                # Calculate similarity between note and passage

                #note_instance.set_similarity()
                list_all_lines.append(note_instance)
            count_lines +=1

    # topic modeling
    lda = ldat(NUM_LDA_TOPICS, list_note_sentences)
    for note_instance in list_all_lines:

        # assign LDA topic
        topic_name = lda.predict_topic(ldat.clean_string(note_instance.get_note()))
        note_instance.set_topic(topic_name)

        # write this instance to file
        outfile_out.write(note_instance.to_string(delimiter=CONST_DELIMITER)+'\n')

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

def is_help_topic(sentence):
    """
    Determine if the given string (message post) contains a question or help request.
    #TODO: This is a really over simplistic way of caclulating such a thing
    :param sentence: a string sentence / message post
    :return: True if the string is about help seeking
    """
    # TODO: this is a super naive way to determine this
    if "help" in sentence or "question" in sentence or "?" in sentence or "dunno" in sentence or "n't know" in sentence:
        return True
    if "confus" in sentence or "struggl" in sentence or "lost" in sentence or "stuck" in sentence or "know how" in sentence:
        return True
    return False

'''
So that logfileLacuna can act as either a reusable module, or as a standalone program.
'''
if __name__ == '__main__':
    print("Running logfileLacuna")
    run()