"""
This file is for modifying the raw data and it's tags to only contain 
the tags that were previously trained in the ged model 
"""
ged_tags = [
    # "DELETE",
    "MERGE-B",
    "MERGE-I",
    "REPLACE_M",
    "REPLACE_MI",
    "REPLACE_MI+REPLACE_OH",
    "REPLACE_MT",
    "REPLACE_O",
    "REPLACE_OA",
    "REPLACE_OA+REPLACE_OH",
    "REPLACE_OA+REPLACE_OR",
    "REPLACE_OC",
    "REPLACE_OD",
    "REPLACE_OD+REPLACE_OG",
    "REPLACE_OD+REPLACE_OH",
    "REPLACE_OD+REPLACE_OM",
    "REPLACE_OD+REPLACE_OR",
    "REPLACE_OH",
    "REPLACE_OH+REPLACE_OM",
    "REPLACE_OH+REPLACE_OT",
    "REPLACE_OH+REPLACE_XC",
    "REPLACE_OM",
    "REPLACE_OM+REPLACE_OR",
    "REPLACE_OR",
    "REPLACE_OR+REPLACE_OT",
    "REPLACE_OT",
    "REPLACE_OW",
    "REPLACE_P",
    "REPLACE_S",
    "REPLACE_SF",
    "REPLACE_SW",
    "REPLACE_X",
    "REPLACE_XC",
    "REPLACE_XC+REPLACE_XG",
    "REPLACE_XC+REPLACE_XN",
    "REPLACE_XF",
    "REPLACE_XG",
    "REPLACE_XM",
    "REPLACE_XN",
    "REPLACE_XT",
    "SPLIT",
    "UC",
    "UNK"
]

def prepare_data_for_cleaning(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as file:
        source_tokens = []
        target_tokens = []
        tag_tokens = []
        for line in file:
            line = line.split('\t')
            if len(line) == 3:
                source, target, tag = line
                source = source.strip()
                target = target.strip()
                tag = tag.strip()
                if tag == 'MERGE':
                    sources, targets, tags = handle_merge(source, target, tag)
                    source_tokens.extend(sources)
                    target_tokens.extend(targets)
                    tag_tokens.extend(tags)
                    continue

                elif 'INSERT' in tag:
                    continue

                elif "DELETE" in tag:
                    tag = 'DELETE'

                elif tag not in ged_tags and "DELETE" not in tag:
                    tag = 'UNK'
                source_tokens.append(source)
                target_tokens.append(target)
                tag_tokens.append(tag)
    return source_tokens, target_tokens, tag_tokens



def handle_merge(source, target, tag):    
    target_list = [target] * len(source.split())
    return source.split(), target_list, ['MERGE-B'] + ['MERGE-I'] * (len(source.split()) - 1)
 

def write_data(source_tokens, target_token, tag_tokens, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        for src, tgt, tags in zip(source_tokens, target_token, tag_tokens):
            line = src + '\t' + tgt + '\t' + tags + '\n'
            file.write(line)
           


def generate_datasets(input_filepath, output_filepath):
    source_tokens, target_tokens, tag_tokens = prepare_data_for_cleaning(input_filepath)
    write_data(source_tokens, target_tokens, tag_tokens, output_filepath)

generate_datasets('../../datasets/ngram_datasets/raw_qalb_14/raw_qalb14_train.txt', '../../datasets/ngram_datasets/processed_qalb14/qalb14_train.txt')
generate_datasets('../../datasets/ngram_datasets/raw_qalb_15/raw_qalb15_train.txt', '../../datasets/ngram_datasets/processed_qalb15/qalb15_train.txt')
generate_datasets('../../datasets/ngram_datasets/raw_zaebuc/raw_zaebuc_train.txt', '../../datasets/ngram_datasets/processed_zaebuc/zaebuc.train.txt')





