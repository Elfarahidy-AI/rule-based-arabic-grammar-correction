from word_level_grammar import WordLevelGrammer

class ContextGrammar:
    def __init__(self):
        self.wlg = WordLevelGrammer()

    """
    handle sentence after هنا و هناك untill you find a something that is not a pronoun
    """
    def handle_after_hona_w_honak(self, words):
        for word in self.wlg.hona_w_honak:
            if word in words:
                i = words.index(word) + 1
                if words[i].endswith('ان') or words[i+1].endswith('ان') or words[i-1].endswith('ان') or words[i-1].endswith('ين'):
                    while i < len(words) and (words[i].endswith('ان') or words[i].endswith('ون') or words[i].endswith('ين')):
                        words[i] = words[i][:-2] + "ان"
                        i += 1
                elif words[i].endswith('ون') or words[i].endswith('ين'):
                    while i < len(words) and (words[i].endswith('ان') or words[i].endswith('ون') or words[i].endswith('ين')):
                        words[i] = words[i][:-2] + "ون"
                        i += 1
        return words
    

    def handle_asmaa_eleshara(self, words):
        pass
    





                
    """
    handle kana sentences and use the utility function to handle the kana words
    """
    def kana_utility(self, current_word, next_word):
        if current_word.startswith('ال'):
            if (current_word.endswith('ين') or current_word.endswith('ون'))and next_word.endswith('ان'): # we can detect that it is dual
                return current_word[:-2] + "ان"
            else:    # it is plural and mansoba
                return current_word[:-2] + "ون"
        elif not current_word.startswith('ال') and next_word.startswith('ال'):
            if (current_word.endswith('ون') or current_word.endswith('ين')) and (not current_word.endswith('عاون') and not current_word.endswith('هاون')):
                return current_word[:-2] + "و" # case of hazf el non lel edafa
            elif current_word.endswith('ان'):
                return current_word[:-2] + "ا"
        return current_word


    def handle_kana(self, words):
        verbs_indeces = self.wlg.get_verbs_indeces(words)
        for i in range(len(words) - 2):
            if words[i] in self.wlg.kana_and_sisters_regular or words[i][1:] in self.wlg.kana_and_sisters_regular:
                if i+1 not in verbs_indeces: # only work on no verbs words
                    words[i+1] = self.kana_utility(words[i+1], words[i+2])
  
        return words
    


    """"####################################################### main function #######################################################"""
    def handle_context_level_errors(self,words):
        after_hona_honak = self.handle_after_hona_w_honak(words)
        kana_handeled = self.handle_kana(after_hona_honak)
        return kana_handeled