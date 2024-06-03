from modules.word_grammar import WordLevelGrammer

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
    

    """
    handle what is after asmaa eleshara
    """
    def handle_asmaa_eleshara(self, words):
        verbs_indeces = self.wlg.get_verbs_indeces(words)
        j = 0
        pronoun = None
        for i in range(len(words)):
            if words[i] in self.wlg.pronouns:
                j = i 
                pronoun = words[i]
                break
            elif words[i][1:] in self.wlg.pronouns:
                j = i
                pronoun = words[i][1:]
                break
        if pronoun:
            if ((self.wlg.pronouns[pronoun] == ["muthanna", "masc"] or 
                self.wlg.pronouns[pronoun] == ["muthanna", "fem"])
                and j not in verbs_indeces):
                for j in range(j, len(words)):
                    if words[j].endswith('ين') or words[j].endswith('ون'):
                        words[j] = words[j][:-2] + "ان"

            elif self.wlg.pronouns[pronoun] == ["jam3", "both"] and j not in verbs_indeces:
                for j in range(j, len(words)):
                    if words[j].endswith('ين') or words[j].endswith('ان'):
                        words[j] = words[j][:-2] + "ون"
        return words
        


    """
    handle jumla ismiya 
    """
    def handle_nominal_sentence(self, words):
        pass

    """
    handle na3t el mufrad
    """
    def handle_adjectives(self, words):
        verbs_indeces = self.wlg.get_verbs_indeces(words)
        for i in range(len(words) - 1):
            if ((words[i].startswith('ال') and words[i+1].startswith('ال')) or 
                (not words[i].startswith('ال') and not words[i+1].startswith('ال') and i not in verbs_indeces and i+1 not in verbs_indeces)):
                if (words[i].endswith('ون') or words[i].endswith('ين') or 
                    words[i].endswith('ان') or words[i].endswith('وا')):
                    words[i+1] = words[i+1][:-2] + words[i][-2:]

        return words
    

    """
    handle 7rof el 3atf
    """
    def handle_Conjunctions(self, words):
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
        elif not current_word.startswith('ال') and next_word.startswith('ال') and current_word not in self.wlg.pronouns: # added the check that it is not in asmaa eleshara
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
    

    """
    handle remove characters for joining (جذف بعض الحروف للإضافة)
    should be called at the end of the context level errors as the last step
    we can check if the word[i+1] is not a person name or country name
    using the csv files in the dataset folder
    """
    def handle_removal(self, words):
        verbs_indeces = self.wlg.get_verbs_indeces(words)
        for i in range(len(words) - 1):
            if not words[i].startswith('ال') and words[i+1].startswith('ال') and i not in verbs_indeces:
                if words[i].endswith('ون'):
                    words[i] = words[i][:-2] + "و"
                elif words[i].endswith('ين'):
                    words[i] = words[i][:-2] + "ي"
                elif words[i].endswith('ان'):
                    words[i] = words[i][:-2] + "ا"
        return words


    """"####################################################### main function #######################################################"""
    def handle_context_level_errors(self,words):
        after_hona_honak = self.handle_after_hona_w_honak(words)
        after_asmaa_eleshara = self.handle_asmaa_eleshara(after_hona_honak)
        kana_handeled = self.handle_kana(after_asmaa_eleshara)
        adjectives_handeled = self.handle_adjectives(kana_handeled)
        return adjectives_handeled