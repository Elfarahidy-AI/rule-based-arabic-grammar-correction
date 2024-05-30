import re
import joblib

import sys
sys.path.append('..')  # Assuming the parent directory of 'pos_tagging' is the current working directory
from pos_tagging.commons import word_features
"""
this class is responsible for handling the grammer of the arabic words
using a rule based approach. but it assumes that all the sentences are 
separated using punctuation marks.
we are also assuming that there is no errors in the verbs spelling entered by the user
"""
class WordLevelGrammer():
    
    def __init__(self):

        # load the crf model to check if the word is a verb or not
        self.crf_model = joblib.load('../pos_tagging/models/crf_model.joblib')
        
        self.alef_wasl = ['ابن', 'ابنة', 'ابنان', 'ابنتان', 'اثنان', 'اثنتان', 'اسم', 'اسمان', 'امرؤ', 'امرأة', 'امرآن', 'امرأتان', 'ايم الله', 'ايمن الله']
       
        # these the are the kana and its sisters cases that most of time there is no deletion for esm kana
        self.kana_and_sisters_regular = ['كان', 'كانت', 'يكون', 'تكون', 'أكون', 'نكون', 'تكن',
                                         'وكان', 'وكانت', 'ويكون', 'وتكون', 'وأكون', 'ونكون', 'وتكن'] 

        # these are the kana and its sisters cases that most of time there is a deletion for esm kana
        self.kana_and_sisters_remove_esm_kana = ['كنت', 'كنا', 'كنتم', 'كنتما', 'كنتن', 'تكونون', 'تكونان', 
                                                 'وكنت', 'وكنتم', 'وكنتما', 'وكنتن', 'وتكونون', 'وتكونان']
        
        self.enna_and_sisters = ["إن", "أن", "كأن", "لكن", "ليت", "لعل"]
        
        self.enna_and_sisters_remove_esm_enna = ["إنهم", "إنكم", "إنه", "إنها", "إننا", "إنكن", "إنك", "إني", "إنا",
                                                 "أنهم", "أنكم", "أنه", "أنها", "أننا", "أنكن", "أنك", "أني", "أنا", 
                                                 "كأنهم", "كأنكم", "كأنه", "كأنها", "كأننا", "كأنكن", "كأنك", "كأني", "كأنا",
                                                 "لكنهم", "لكنكم", "لكنه", "لكنها", "لكننا", "لكنكن", "لكنك", "لكني", "لكنا",
                                                 "ليتهم", "ليتكم", "ليته", "ليتها", "ليتنا", "ليتكن", "ليتك", "ليتي", "ليتا", 
                                                 "لعلهم", "لعلكم", "لعله", "لعلها", "لعلنا", "لعلكن", "لعلك", "لعلي", "لعلن"]
        

        self.pronouns = {'هذا': ['mufrad', 'masc'], 'هذه': ['mufrad', 'fem'], 
                         'هذان': ['muthanna', 'masc'], 'هذين':['muthanna', 'masc'], 
                         'هاتان': ['muthanna', 'fem'], 'هاتين':['muthanna', 'fem'],
                         'هؤلاء': ['jam3', 'both'],
                         'ذلك': ['mufrad', 'masc'], 'تلك': ['mufrad', 'fem'], 'أولئك': ['jam3', 'both']}

        self.prepositions = ['في', 'على', 'من', 'إلى', 'عن']

        # list of most of al afaal al lazema (only fa3el, no maf3ool)
        self.essential_verbs = [
        'أذن', 'أمن', 'أدرك', 'أبل', 'أبحر', 'أتى', 'أجهض', 'أحصن',
        'أشرك', 'افتتح', 'آمن', 'أمسك', 'أوسع', 'استأمن', 'اعتقد',
        'اكتسى', 'إرتبع', 'استامن', 'استربع', 'استظهر', 'استعان', 'استعبر',
        'استعرض', 'استفتح', 'اشترك', 'اعترض', 'اكتتب', 'امتعض', 'انطلق',
        'انفتح', 'بحث', 'بدا', 'بقي', 'بل', 'تشعر', 'تبدل', 'تحدث', 'تحول',
        'تدبر', 'تغير', 'تفاتح', 'تفتح', 'تكلم', 'تواضع', 'جاء', 'حاسب',
        'حذر', 'حرك', 'حظر', 'خاف', 'خرج', 'دام', 'دابر', 'دخل', 'درس', 'ذبل',
        'ذهب', 'راح', 'راق', 'رجع', 'رجل', 'رحل', 'رد', 'سقط', 'سلك', 'سمح',
        'شر', 'شعب', 'شعر', 'صاح', 'طرأ', 'طرب', 'طلع', 'طلق', 'ظل', 'ظهر',
        'عاد', 'عبر', 'عبق', 'فاز', 'فرح', 'فشل', 'فكر', 'فهم',
        'قام', 'وقف', 'وثب', 'نجا', 'نجح', 'فشل', 'نزل', 'نشأ', 'نظر',
        ]

        self.five_names = ['أب','أخ', 'حم', 'فو', 'ذو']

        self.time_words = ["مساء", "سحرا", "غدوة", "بكرة", "صباحا", "اليوم", "أمس", "غدا", "الليلة", "حينا", "وقتا", "أمدا", "أبدا", "أصبح", "يوم"]
        
        self.place_words = ["هنا", "فوق", "تحت", "أمام", "قدام", "وراء", "خلف", "إزاء", "تلقاء", "عند", "حذاء", "ثم"]
        
        # most of the verbs patterns   
        #self.verbs_shapes = ['فعل', 'فععل', 'افعل', 'أفعل', 'تفاعل', 'إنفعل', 'انفعل', 'استفعل', 'إستفعل', 'استعل', 'إستعل', 'يفعل', 'افل', 'أفعل']

        # the tools that are used to make the verb mansoob
        self.verb_nasb_tools = ['أن', 'لن', 'كي', 'حتى', 'ل'] 

        # the tools that are used to make the verb majzoom
        self.verb_jazm_tools = ['لم', 'لما']
        self.la_alnahya = ['لا']    # sperated to handle the case of la alnahya alone

        self.hamza_known_words = ["إلينا", "إليكم", "إاليهم", "إليك", "إليه", "إليها", "إليهن", "إلي", "إليهما", "إليهما", "إليكما"]




    
    """
    stemm the words from any additons
    use it to check on the verbs
    """
    def stemm_word(self, word):
        initial = word
        count = 0   # added the count to check if the word was not changed
        if (word.endswith('ون') or 
            word.endswith('ان') or 
            word.endswith('ين') or 
            word.endswith('ات') or
            word.endswith('تا') or
            word.endswith('وا')):
            return word[:-2]
        elif word.endswith('ت') or word.endswith('ا'):
            return word[:-1]

        if word == initial:
            count +=1
        return word
    
        
    """
    function to return the indeces of the verbs in the list of words
    """
    def get_verbs_indeces(self, words):
        verbs_indeces = []
        sentence = list(zip(words, ['' for _ in range(len(words))]))
        X_new = [word_features(sentence, i) for i in range(len(sentence))]
        y_pred = self.crf_model.predict([X_new])[0]
        for word, tag in zip(words, y_pred):
            if 'VERB' in tag or 'AUX' in tag:
                verbs_indeces.append(words.index(word))
        return verbs_indeces




    """
    check if the sentence is verbal or not
    if the sentence starts with a word within the defined verbs or
    the word length is equal to 3 then it is probably verbal sentence
    """
    def is_verbal_sentence(self, words):
        verbs_indeces = self.get_verbs_indeces(words)
        x = 0
        if x in verbs_indeces:
            return True
        return False
    



    """####################################################   complex grammar handling   ################################################################"""

    """
    handle the hamzat in the words
    the rule is:
        1- if the word starts with 'الا' then replace it with 'الأ'
        2- if the word starts with 'ال' or 'أل' then replace it with 'ال'
        3- quadratic verbs should start with 'أ' (most cases in arabic)
        4- quadratic nouns should start with 'أ' (most cases in arabic)
        5- triple verbs or nouns should start with 'أ' (most cases in arabic)
        6- larger than 4 letters should start with 'ا' (most cases in arabic)
        7- if the word is one character difference from a defined word then change it to the defined word
           using the utility function is_similar
    """
    # utility function to check if the word is already defined in the class
    def is_similar(self, word):
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        if word == item and (word[0] == 'أ' or word[0] == 'إ' or word[0] == 'آ' or word[0] == 'ا'):
                            return word, 1
                        elif((item[0] == 'أ' or item[0] == 'إ' or item[0] == 'آ' or item[0] == 'ا') and 
                             (word[0] == 'ا' or word[0] == 'أ' or word[0] == 'إ' or word[0] == 'آ')):
                            if word[1:] == item[1:]:
                                return item, 1
        return word, 0
        
    def handle_hamzat(self, words):
        verb_indeces = self.get_verbs_indeces(words)
        for i in range(len(words)): 
            returned_word, flag = self.is_similar(words[i])
            if flag:
                words[i] = returned_word
                if len(words[i]) == 2: # most of time for defined words of size 2, the first letter should be 'أ' not 'إ
                    words[i] = 'أ' + words[i][1:]
                continue

            # second case is handling the verbs
            elif (i in verb_indeces or
                 words[i] in self.kana_and_sisters_regular or 
                 words[i] in self.kana_and_sisters_remove_esm_kana):
                stemmed_word = self.stemm_word(words[i])
                if stemmed_word[0] == 'أ' or stemmed_word[0] == 'إ' or stemmed_word[0] == 'آ' or stemmed_word[0] == 'ا':
                    if len(stemmed_word) > 4:
                        words[i] = 'ا' + words[i][1:]
                    elif len(stemmed_word) == 4:
                        words[i] = 'أ' + words[i][1:]
                    elif len(stemmed_word) == 3:
                        words[i] = 'أ' + words[i][1:]

            else:
                if words[i].startswith('الا'):
                    words[i] = 'الأ' + words[i][3:]
                elif words[i].startswith('ال') or words[i].startswith('أل'):
                    words[i] = 'ال' + words[i][2:]
                elif words[i][0] == 'ا' or words[i][0] == 'أ' or words[i][0] == 'إ' or words[i][0] == 'آ':
                    if len(words[i]) > 4:
                        words[i] = 'ا' + words[i][1:]
                    elif len(words[i]) == 4:
                        words[i] = 'أ' + words[i][1:]
                    elif len(words[i]) == 3:
                        words[i] = 'أ' + words[i][1:]

        return words
                                    

        
    
    """
    handle the after proposition words
    """
    def handle_after_propositions_words(self, words):
        for i in range(len(words)):
            if words[i] in self.prepositions:
                j = i + 1
                while words[j].endswith('ون') or words[j].endswith('ان'):
                    words[j] = words[j][:-2] + "ين"
                    j += 1
        return words


    """
    function to handle if the verb is mansoub 
    """
    def handle_verb_shape_mansoob(self, words):
        verb_indeces = self.get_verbs_indeces(words)
        for i in range(1, len(words)):
            if i in verb_indeces:
                prev_word = words[i-1]
                if prev_word in self.verb_nasb_tools:
                    if (words[i].endswith('ون') or words[i].endswith('ين')) and (words[i][0] == 'ي' or words[i][0] == 'ت'):
                        words[i] = words[i][:-2] + "وا"
                    elif (words[i].endswith('ان') or words[i].endswith('ين')) and (words[i][0] == 'ي' or words[i][0] == 'ت'):
                        words[i] = words[i][:-1]
        return words
    

    """
    function to handle if the verb is majzoom
    """
    def handle_verb_shape_majzoom(self, words):
        verbs_indeces = self.get_verbs_indeces(words)
        for i in range(1, len(words)):
            if i in verbs_indeces:
                prev_word = words[i-1]
                if prev_word in self.verb_jazm_tools:
                    if (words[i].endswith('ون') or words[i].endswith('ين')) and (words[i][0] == 'ي' or words[i][0] == 'ت'):
                        words[i] = words[i][:-2] + "وا"
                    elif (words[i].endswith('ان') or words[i].endswith('ين')) and (words[i][0] == 'ي' or words[i][0] == 'ت'):
                        words[i] = words[i][:-1]
                    elif words[i].endswith('و') or words[i].endswith('ي') or words[i].endswith('ى'):  # remove 3ela character (don't )
                        words[i] = words[i][:-1]
                elif prev_word in self.la_alnahya:
                    if words[i].startswith('ت'):
                        if words[i].endswith('ون') or words[i].endswith('ين'):
                            words[i] = words[i][:-2] + "وا"
                    elif words[i].endswith('ان') or words[i].endswith('ن'):
                        words[i] = words[i][:-1]
        return words
    


    """
    handle the pronouns and what is after them
    """
    def handle_pronouns(self, words):
        if words[0] in self.pronouns.keys():
            if self.pronouns[words[0]] == ['muthanna', 'masc']:
                words[0] = 'هذان'
            elif self.pronouns[words[0]] == ['muthanna', 'fem']:
                words[0] = 'هاتان'
        return words
        
            
        
    """###############################    the main functions      ############################"""

    def handle_word_level_errors(self, words):
        hamza_handled_words = self.handle_hamzat(words)
        handeled_words_propsositions = self.handle_after_propositions_words(hamza_handled_words)
        verb_mansoob_shapes_handeled = self.handle_verb_shape_mansoob(handeled_words_propsositions)
        verb_majzoom_shapes_handeled = self.handle_verb_shape_majzoom(verb_mansoob_shapes_handeled)
        pronouns_handled = self.handle_pronouns(verb_majzoom_shapes_handeled)
        return pronouns_handled
    



