# lacuna-log-processing
This project represents a Python script for processing a single CSV logfile from an annotation tool.

## requires
Python 3+ with gensim and stop_words installed. Likely the Anaconda distribution.

## running
The main scripts are **logfileLacuna.py** .

## code
**logfileLacuna.py** reads in the file from CSV, maneuvers other classes to get the topic modeling and similarities, and then writes out to CSV

**topicModelLDA.py** an internal class for creating an LDA topic model and predicting the topic of future documents. Also contains a convenient method for cleaning unwanted characters from a string and turning it into a bag of words to be fed to the model. Will eventually have functionality for calculating similarity between two strings.

**NoteInstance.py** an internal class representing one usage of the annotation system: the users involved, the passage highlighted, annotation made, context, title of article, manual codes, etc.

## logfiles
Note: The logfiles contained in this github repository are simulated and not the real data gathered from the study
- **combine_final_codes.csv:** 
> ex: annotation_id,uid,passage,annotation,title,setting,comp/crit,strategy,notes,combined strategy calculation,combined strategy
7645,3401,"The Lord of the Rings is an epic high-fantasy novel written by English author J. R. R. Tolkien. The story began as a sequel to Tolkien's 1937 fantasy novel The Hobbit, but eventually developed into a much larger work. Written in stages between 1937 and 1949, The Lord of the Rings is one of the best-selling novels ever written, with over 150 million copies sold.",A chocolate chip cookie is a drop cookie that originated in the United States and features chocolate chips as its distinguishing ingredient. The traditional recipe combines a dough composed of butter and both brown and white sugar with semi-sweet chocolate chips. Variations include recipes with other types of chocolate as well as additional ingredients such as nuts or oatmeal.,fellowship,shire,critique,evaluation,,evaluation,evaluation