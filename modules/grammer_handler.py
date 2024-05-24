import re

"""
this class is responsible for handling the grammer of the arabic words
using a rule based approach. but it assumes that all the sentences are 
separated using punctuation marks.
we are also assuming that there is no errors in the verbs spelling entered by the user
"""
class Grammer():
    
    def __init__(self):
        
        self.alef_wasl = ['ابن', 'ابنة', 'ابنان', 'ابنتان', 'اثنان', 'اثنتان', 'اسم', 'اسمان', 'امرؤ', 'امرأة', 'امرآن', 'امرأتان', 'ايم الله', 'ايمن الله']
       
        # these the are the kana and its sisters cases that most of time there is no deletion for esm kana
        self.kana_and_sisters_regular = ['كان', 'كانت', 'يكون', 'تكون', 'أكون', 'نكون', 'تكن',
                                         'وكان', 'وكانت', 'ويكون', 'وتكون', 'وأكون', 'ونكون', 'وتكن'] 

        # these are the kana and its sisters cases that most of time there is a deletion for esm kana
        self.kana_and_sisters_remove_esm_kana = ['كنت', 'كنا', 'كنتم', 'كنتما', 'كنتن', 'تكونون', 'تكونان', 
                                                 'وكنت', 'وكنتم', 'وكنتما', 'وكنتن', 'وتكونون', 'وتكونان']

        self.pronouns = {'هذا': ['mufrad', 'masc'], 'هذه': ['mufrad', 'fem'], 
                         'هذان': ['muthanna', 'masc'], 'هذين':['muthanna', 'masc'], 'هاتان': ['muthanna', 'fem'], 'هاتين':['muthanna', 'fem'],
                           'هؤلاء': ['jam3', 'both'], 'ذلك': ['mufrad', 'masc'], 'تلك': ['mufrad', 'fem'], 'أولئك': ['jam3', 'both']}

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
        self.verbs_shapes = ['فعل', 'فععل', 'افعل', 'أفعل', 'تفاعل', 'إنفعل', 'انفعل', 'استفعل', 'إستفعل', 'استعل', 'إستعل', 'يفعل', 'افل', 'أفعل']

        # the tools that are used to make the verb mansoob
        self.verb_nasb_tools = ['أن', 'لن', 'كي', 'حتى', 'ل'] 

        # the tools that are used to make the verb majzoom
        self.verb_jazm_tools = ['لم', 'لما']
        self.la_alnahya = ['لا']    # sperated to handle the case of la alnahya alone




    """
    check if the word is alef wasl or not
    """
    def is_alef_wasl(self, word):
        if word.startswith('ال') or word.startswith('أل'):
            word = word[2:]
        if word.startswith('أ'): # check if it has hamza at the beginning
            word = word[2:]
        return word in self.alef_wasl


    """
    check if the word is feminine or masculine
    """
    def check_gender(arabic_word):
        masculine_endings = ['ون', 'ان', 'ين', 'ي', 'ا', 'و']
        feminine_endings = ['ة', 'ات']

        if any(arabic_word.endswith(ending) for ending in masculine_endings):
            return 'Masculine'
        elif any(arabic_word.endswith(ending) for ending in feminine_endings):
            return 'Feminine'
        return 'Unknown'
  
    """
    check if the word is dual(muthanna) or not 
    """
    def is_dual(self, word):
        if word in self.essential_verbs or word in self.kana_and_sisters_regular:
            return False
        dual_endings = ['ان', 'تان']
        if any(word.endswith(ending) for ending in dual_endings):
            return True
        return False

    """
    check if the word is a plural or not
    """
    def check_plural(arabic_word):
        plural_endings = ['ون', 'ين', 'ات']

        if any(arabic_word.endswith(ending) for ending in plural_endings):
            return True
        return False
    
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
        # if word.startswith('و'):
        #     return word[1:]
        if word == initial:
            count +=1
        return word
        

    """
    check if the word is a verb or not
    uses the utility function stemm_word to check on the verb
    handle most of the verbs cases, but not all past tense verbs that has only three characters 
    """
    def is_verb(self, word, prev_word = None):
        # check if the prev word is a preposition or a time word or a place word
        # as this prevent the word after them to be a verb
        if (prev_word in self.prepositions or 
            prev_word in self.time_words or
            prev_word in self.place_words):
            return False
        if len(word) < 2:
            return False
        if (word in self.prepositions or
            word in self.pronouns or
            word in self.place_words or 
            word in self.time_words):
            return False
        if (word in self.essential_verbs or 
            word in self.verbs_shapes or 
            word in self.kana_and_sisters_regular or
            word in self.kana_and_sisters_remove_esm_kana):
            return True
        
        if word.startswith('ال') or word.startswith('أل') or word.startswith('م'):
            return False
        
        sub_word = self.stemm_word(word)
        if (sub_word in self.essential_verbs or 
            sub_word in self.verbs_shapes or 
            sub_word in self.kana_and_sisters_regular or
            sub_word in self.kana_and_sisters_remove_esm_kana):
            return True
        
        if (sub_word.startswith('ا') or 
            sub_word.startswith('ي') or 
            sub_word.startswith('ت') or
            sub_word.startswith('ن')):
            return True
        
        verb_patterns = [
            r'^س([أ-ي]{2,})$',  # Future tense pattern like "سيتعلم"
            r'^ي([أ-ي]{2,})$',  # Present tense pattern like "يتعلم"
            r'^ت([أ-ي]{2,})$',  # Present tense pattern like "تعمل"
            r'^ن([أ-ي]{2,})$',  # Present tense pattern like "نأكل"
        ]
        
        for pattern in verb_patterns:
            if re.match(pattern, word):
                return True
        return False


    """
    check if the sentence is verbal or not
    if the sentence starts with a word within the defined verbs or
    the word length is equal to 3 then it is probably verbal sentence
    """
    def is_verbal_sentence(self, words):
        sub_word = words[0]
        if (sub_word in self.kana_and_sisters_regular or 
            sub_word in self.essential_verbs or 
            sub_word in self.verbs_shapes or 
            sub_word in self.kana_and_sisters_remove_esm_kana):
            return True  
        if (len(sub_word) == 3 and 
            sub_word not in self.prepositions and 
            sub_word not in self.pronouns and 
            sub_word not in self.place_words and 
            sub_word not in self.time_words):
            return True
        
        if self.is_verb(sub_word):
            return True
        return False
    



    """####################################################   complex grammar handling   ################################################################"""

    """
    handle the hamzat in the words
    the rule is:
        1- if the word starts with 'الا' then replace it with 'الأ'
        2- if the word starts with 'ال' or 'أل' then replace it with 'ال'
        3- quadratic verbs should start with 'إ' (most cases in arabic)
        4- quadratic nouns should start with 'أ' (most cases in arabic)
        5- triple verbs or nouns should start with 'أ' (most cases in arabic)
        6- larger than 4 letters should start with 'ا' (most cases in arabic)
        7- if the word is one character difference from a defined word then change it to the defined word
           using the utility function is_similar
    """
    # utility function to check if two words are similar
    def is_similar(self, word, prop):
        if len(word) != len(prop):
            return False
        differences = sum(char1 != char2 for char1, char2 in zip(word, prop))
        return differences <= 1
    
    def handle_hamzat(self, word):
        # check if the word is a preposition, time word, or place word to handle the hamzat 
        for prop in self.prepositions + self.time_words + self.place_words:
            if ((prop[0] == 'ا' or prop[0] == 'أ' or prop[0] == 'إ' or prop[0] == 'آ') and 
                (word[0] == 'ا' or word[0] == 'أ' or word[0] == 'إ' or word[0] == 'آ')):
                if self.is_similar(word[1:], prop[1:]):
                    # Perform desired action when the word is similar to a prop
                    word = prop[0] + word[1:]
                    return word
        if word.startswith('الا'):
            return 'الأ' + word[3:]
        if word.startswith('ال') or word.startswith('أل'):
            return 'ال' + word[2:]
        
        if word.startswith('أ') or word.startswith('إ') or word.startswith('آ') or word.startswith('ا'): 
            if len(self.stemm_word(word)) > 4:
              return 'ا' + word[1:]
            elif len(self.stemm_word(word)) == 4 and self.is_verb(word): 
                return 'إ' +word[1:]
            elif len(self.stemm_word(word)) == 4 and not self.is_verb(word):
                return 'أ' + word[1:]
            elif len(self.stemm_word(word)) == 3:
                return 'أ' + word[1:]
        return word
    

    
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
        prev_word = words[0]
        for i in range(1, len(words)):
            prev_word = words[i-1]
            if self.is_verb(words[i], prev_word):
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
        prev_word = words[0]
        prev_word = words[0]
        for i in range(1, len(words)):
            prev_word = words[i-1]
            if self.is_verb(words[i], prev_word):
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
    

            
        
    """###############################    the main functions      ############################"""

    def handle_word_level_errors(self, words):
        new_words = []
        for word in words:
            handled_word = self.handle_hamzat(word)
            new_words.append(handled_word)
        handeled_words_propsositions = self.handle_after_propositions_words(new_words)
        verb_mansoob_shapes_handeled = self.handle_verb_shape_mansoob(handeled_words_propsositions)
        verb_majzoom_shapes_handeled = self.handle_verb_shape_majzoom(verb_mansoob_shapes_handeled)
        return verb_majzoom_shapes_handeled
    



