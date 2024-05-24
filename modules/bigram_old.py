class BiGram():
    def __init__(self):
        self.bi_dict = {}

    # read the data set and store it in separate lists
    def read_data(self):
        file1 = 'datasets/processed_qalb14/qalb14_train.txt'
        file2 = 'datasets/processed_qalb15/qalb15_train.txt'
        file3 = 'datasets/processed_zaebuc/zaebuc.train.txt'
        
        source_list = []
        target_list = []
        tag_list = []
        with open(file1, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split('\t')
                source, target, tag = line
                source = source.strip()
                target = target.strip()
                tag = tag.strip()
                source_list.append(source)
                target_list.append(target)
                tag_list.append(tag)

        with open(file2, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split('\t')
                source, target, tag = line
                source = source.strip()
                target = target.strip()
                tag = tag.strip()
                source_list.append(source)
                target_list.append(target)
                tag_list.append(tag)

        with open(file3, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split('\t')
                source, target, tag = line
                source = source.strip()
                target = target.strip()
                tag = tag.strip()
                source_list.append(source)
                target_list.append(target)
                tag_list.append(tag)
    
        return source_list, target_list, tag_list


    # handle the merge tags to solve it manually befor constructing the bigram
    def handle_merge(self, source_list, target_list, tag_list):
        new_source_list = []
        new_target_list = []
        new_tag_list = []
        for source, target, tag in zip(source_list, target_list, tag_list):
            if tag == 'MERGE-B':
                new_source_list.append(source)
                new_target_list.append(target)
                new_tag_list.append("UC")
            
            elif tag == 'MERGE-I':
                new_source_list[-1] += source

            else:
                new_source_list.append(source)
                new_target_list.append(target)
                new_tag_list.append(tag)

        return new_source_list, new_target_list, new_tag_list

            
    """
        we may ignore storing the tags, and sources only if the tag is UC
        because we won't use this tag or the souce with it to change anything
    """
    # construct the bigram from the final lists after handling the merge tags
    def construct_bigram_dict(self, source_list, target_list, tag_list):
        source_list.insert(0, 'START')
        target_list.insert(0, 'START')
        tag_list.insert(0, 'UC')
        source_list.append('END')
        target_list.append('END')
        tag_list.append('UC')
        for i in range(len(source_list) - 1):
            key = (target_list[i], source_list[i+1], tag_list[i+1])
            if key not in self.bi_dict:
                self.bi_dict[key] = {}
            if target_list[i+1] not in self.bi_dict[key]:
                self.bi_dict[key][target_list[i+1]] = 0
            self.bi_dict[key][target_list[i+1]] += 1

    # train the model
    def train(self):
        source_list, target_list, tag_list = self.read_data()
        source_list, target_list, tag_list = self.handle_merge(source_list, target_list, tag_list)
        self.construct_bigram_dict(source_list, target_list, tag_list)
        
    # handle the merge tags for the predict function to solve it manually
    def handle_merge_for_predict(self, source_list, tags_list):
        new_source_list = []
        new_tags_list = []
        for source, tag in zip(source_list, tags_list):
            if tag == 'MERGE-B':
                new_source_list.append(source)
                new_tags_list.append("UC")
            elif tag == 'MERGE-I':
                new_source_list[-1] += source
            else:
                new_source_list.append(source)
                new_tags_list.append(tag)

        return new_source_list, new_tags_list

    # predict the target list, if the tag is UC, then the target is the source
    def predict(self, source_list, tags_list):
        source_list, tags_list = self.handle_merge_for_predict(source_list, tags_list)
        target_list = ['START'] + source_list[:]
        source_list.insert(0, 'START')
        tags_list.insert(0, 'UC')
        tags_list.append('UC')
        self.handle_merge(source_list, target_list, tags_list)
        for i in range(1, len(source_list)):
            key = (target_list[i-1], source_list[i], tags_list[i])
            if key not in self.bi_dict or tags_list[i] == 'UC':
                target_list[i] = source_list[i]
            elif key in self.bi_dict and tags_list[i] != 'UC':
                target = max(self.bi_dict[key], key=self.bi_dict[key].get)
                target_list[i] = target
        return target_list[1:]

    


    # save the model in a pickle file
    def save_model(self):
        pass


    # a testing function to save the last list to check their correctness
    def save_lists(self, source_list, target_list, tag_list):
        with open('datasets/ngram_datasets/processed_qalb14/train22.txt', 'w', encoding='utf-8') as file:
            for source, target, tag in zip(source_list, target_list, tag_list):
                file.write(source + '\t' + target + '\t' + tag + '\n')

