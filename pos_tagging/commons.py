


# Define a function to extract features for each word in a sentence
def word_features(sentence, i):
    word = sentence[i][0]
    features = {
        'word': word,
        'is_first': i == 0, #if the word is a first word
        'is_last': i == len(sentence) - 1,  #if the word is a last word

         #prefix of the word
        'prefix-1': word[0],   
        'prefix-2': word[:2],
        'prefix-3': word[:3],

         #suffix of the word
        'suffix-1': word[-1],
        'suffix-2': word[-2:],
        'suffix-3': word[-3:],

         #extracting previous word
        'prev_word': '' if i == 0 else sentence[i-1][0],
        
         #extracting next word
        'next_word': '' if i == len(sentence)-1 else sentence[i+1][0],
    }
    return features