from .word_level_grammar import WordLevelGrammar

class ContextGrammar:
    def __init__(self):
        self.wlg = WordLevelGrammar()

    
        

# """
# function to keep the words consistent along the sentence
# all the words should be in the same form (singular, dual, plural)
# """
# def keep_consistent(self, words):
#     pass



# """
# function to keep the shape (e3rab) of the words consistent along the sentence
# all the words should be in the same shape (marfoo3, mansoob, majroor)
# """
# def keep_shape_consistent(self, words):
#     pass


    
# """
# handle the after pronouns words(asma2 el eshara)
# """
# def handle_after_pronouns(self, words):
#     return words
    


# """
# handle kana and its sisters
# and handled the muthanna case
# """
# def handle_kana(self, words):
#     return words
    


# """
# handle kana and its sisters
# and handled the muthanna case
# """
# def handle_kana(self, words):
#     muthanna = False # flag to check if the coming words has a muthanna word or not
#     for word in words:
#         if self.is_dual(word):
#             muthanna = True
#             break
#     for word in words:
#         if word in self.kana_and_sisters_regular:
#             kana_index = words.index(word)
#             # the case that the coming is esm kana
#             if words[kana_index + 1].startswith('ال') or words[kana_index + 1].startswith('أل'):
#                 if words[kana_index + 1].endswith('ين') and not muthanna:
#                     words[kana_index +1 ] = words[kana_index + 1][:-2] + "ون"
#                 elif words[kana_index + 1].endswith('ين') and muthanna:
#                     words[kana_index +1 ] = words[kana_index + 1][:-2] + "ان"
#                 i = kana_index + 2
#                 while words[i].endswith('ين') or words[i].endswith('ون') or words[i].endswith('ان'):
#                     if (words[i].startswith('ال') or words[i].startswith('أل')):
#                         if not self.is_verb(words[i]) and not self.is_dual(words[i]):
#                             words[i] = words[i][:-2] + "ون"
#                         elif self.is_dual(words[i]) and not self.is_verb(words[i]):
#                             words[i] = words[i][:-2] + "ان"
#                     elif not words[i].startswith('أل') and not words[i].startswith('أل'):
#                         if not self.is_verb(words[i]):
#                             words[i] = words[i][:-2] + "ين"
#                     i += 1

#             # the case that the comming is khabr kana
#             elif not words[kana_index + 1].startswith('أل') and not words[kana_index + 1].startswith('ال') and not self.is_verb(words[kana_index + 1]):
#                 if words[kana_index + 1].endswith('ون') or words[kana_index + 1].endswith('ان'):
#                     words[kana_index +1 ] = words[kana_index + 1][:-2] + "ين"
#                 i = kana_index + 2
#                 while words[i].endswith('ون'):
#                     words[i] = words[i][:-2] + "ين"
#                     i += 1
#     return words