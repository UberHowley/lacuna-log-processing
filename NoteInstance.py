__author__ = 'IH'
__project__ = 'analyzeLacuna'

class NoteInstance(object):
    """
    A line in the logfile represents one annotation and the important information around that.
    ex: annotation_id	uid, passage, annotation, title, setting, comp/crit, strategy, notes, combined strategy calculation, combined strategy
    """
    note_id=""
    uid=""
    passage=""
    note=""
    title=""
    setting=""
    code_top=""
    code_strategy=""
    notes=""
    code_top_calculate =""
    code_combined=""

    # calculated
    count = -1
    topic_index = -1
    topic=""
    similarity=-1


    def __init__(self, ni,u,p,n,t,s,ct,cs,no,ctc,cc, l):
        """
        Initialize a new NoteInstance with the necessary information
        :param ni: annotation id
        :param u: user id
        :param p: passage
        :param n: note
        :param t: title
        :param s: setting
        :param ct: top level code
        :param cs: strategy code
        :param no: notes
        :param ctc: calculated top code based on strategy
        :param cc: combined strategy code
        :param l: line number
        :param to: topic name
        :param si: similarity between note and passage
        :return: None
        """
        self.note_id = ni
        self.uid = u
        self.passage = p
        self.note = n
        self.title = t
        self.setting = s
        self.code_top = ct
        self.code_strategy = cs
        self.notes = no
        self.code_top_calculate = ctc
        self.code_combined = cc
        self.count = l

    def get_passage(self):
        return self.passage

    def get_note(self):
        return self.note

    def set_count(self,l):
        self.count = l

    def set_topic(self, t):
        self.topic=t

    def set_topic_index(self, ti):
        self.topic_index=ti

    def set_similarity(self,si):
        self.similarity = si

    def to_string(self, delimiter):
        """
        Create a string for printing this note instance
        :param delimiter: character to split each column
        :return: a string for printing this NoteInstance
        """
        line = str(self.note_id) + delimiter + str(self.uid) + delimiter
        line += "\"" + self.passage  + "\"" + delimiter
        line += "\"" + self.note + "\"" + delimiter
        line += "\"" + self.title + "\"" + delimiter
        line += self.setting + delimiter + self.code_top + delimiter
        line += self.code_strategy + delimiter
        line += "\"" + self.notes + "\"" + delimiter
        line += self.code_top_calculate + delimiter + self.code_combined
        line += delimiter + str(self.count) + delimiter
        #line += str(self.topic_index) + delimiter
        line += self.topic + delimiter + str(self.similarity)

        return line

