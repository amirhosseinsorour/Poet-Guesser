# -*- coding: utf-8 -*-
import collections


def get_sentences(filePath, isTest):
    punctuations = ".،:؛!؟*\"\'«»"
    with open(filePath, 'r', encoding="utf-8") as f:
        temp_list = dict() if isTest else list()
        for line in f.readlines():
            line = line.translate(line.maketrans('', '', punctuations))
            if isTest:
                line = line.split("\t")
                line[1] = "</s> " + line[1].rstrip("\n") + " <s>"
                temp_list.update({line[1]: int(line[0])})
            else:
                line = "</s> " + line.rstrip("\n") + " <s>"
                temp_list.append(line)
        f.close()
    return temp_list


def get_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = sentence.split()
        for word in sentence:
            temp_list.append(word)
    return temp_list


def get_pair_of_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        words = sentence.split()
        for i in range(words.__len__() - 1):
            pair = words[i] + " " + words[i + 1]
            temp_list.append(pair)
    return temp_list


def build_dictionary(sentences, n):
    frequencies_dict = dict()
    if n == 1:
        words = get_words(sentences)
        for word in words:
            if word in frequencies_dict.keys():
                newFrequency = frequencies_dict[word] + 1
                frequencies_dict.update({word: newFrequency})
            else:
                frequencies_dict.update({word: 1})
        temp_dict = frequencies_dict.copy()
        for word in temp_dict:
            if temp_dict.get(word) < 2:
                frequencies_dict.pop(word)
        return frequencies_dict
    if n == 2:
        pair_of_words = get_pair_of_words(sentences)
        for pair in pair_of_words:
            if pair in frequencies_dict.keys():
                newFrequency = frequencies_dict[pair] + 1
                frequencies_dict.update({pair: newFrequency})
            else:
                frequencies_dict.update({pair: 1})
        temp_dict = frequencies_dict.copy()
        for pair in temp_dict:
            if temp_dict.get(pair) < 2:
                frequencies_dict.pop(pair)
        return frequencies_dict


def build_unigram(unigram_dict):
    unigram_model = dict()
    M = sum(unigram_dict.values())
    for word, count in unigram_dict.items():
        unigram_model.update({word: count / M})
    sorted_y = sorted(unigram_model.items(), key=lambda kv: kv[1])
    sorted_unigram_model = collections.OrderedDict(sorted_y)
    return sorted_unigram_model


def build_bigram(bigram_dict, unigram_dict):
    bigram_model = dict()
    for pair, count in bigram_dict.items():
        bigram_model.update({pair: (count / unigram_dict[pair.split()[0]])})
    sorted_y = sorted(bigram_model.items(), key=lambda kv: kv[1])
    sorted_bigram_model = collections.OrderedDict(sorted_y)
    return sorted_bigram_model


def build_all_models(poet):
    filePath = "train_set\\" + poet + "_train.txt"
    all_sentences = get_sentences(filePath, False)
    unigram_dict = build_dictionary(all_sentences, 1)
    bigram_dict = build_dictionary(all_sentences, 2)
    unigram_model = build_unigram(unigram_dict)
    bigram_model = build_bigram(bigram_dict, unigram_dict)

    backoff_model = dict()
    for pair, count in bigram_dict.items():
        unigram_probability = unigram_model[pair.split()[0]]
        bigram_probability = bigram_model[pair]
        backoff_probability = (landa3 * bigram_probability) + (landa2 * unigram_probability) + (landa1 * e)
        if backoff_probability > 1:
            print(pair + "\n" + str(backoff_probability) + "\n")
        backoff_model.update({pair: backoff_probability})
    return backoff_model, bigram_model, unigram_model


def accuracy():
    test_sentences = get_sentences("test_set\\test_file.txt", True)
    count = 0
    with open("test_set\\answer_file.txt", 'w' , encoding="utf-8") as f:
        for sentence in test_sentences.keys():
            f.write(sentence + "\n")
            print(sentence)
            poet = get_poet(test_sentences[sentence])
            f.write("Real poet: " + poet + "\n\n")
            ferdowsi_prob = probability(sentence, "ferdowsi")
            hafez_prob = probability(sentence, "hafez")
            molavi_prob = probability(sentence, "molavi")
            f.write("Ferdowsi probability: " + str(ferdowsi_prob) + "\n")
            f.write("Hafez probability: " + str(hafez_prob) + "\n")
            f.write("Molavi probability: " + str(molavi_prob) + "\n")
            guessed_poet = get_poet(get_max(ferdowsi_prob, hafez_prob, molavi_prob))
            if guessed_poet == poet:
                count += 1
            f.write("\nGuessed poet: " + guessed_poet + "\n")
            f.write("=============================================================\n")
    f.close()
    return count / test_sentences.keys().__len__() * 100


def probability(sentence, poet):
    backoff_model, bigram_model, unigram_model = get_all_models(poet)
    pair_of_words = get_pair_of_words([sentence])
    for pair in pair_of_words:
        if pair in backoff_model.keys():
            return backoff_model[pair]
        else:
            u = pair.split()[0]
            if u in unigram_model.keys():
                return (landa2 * unigram_model[u]) + (landa1 * e)
            else:
                return landa1 * e


def get_all_models(poet):
    if poet == "ferdowsi":
        return ferdowsi_backoff_model, ferdowsi_bigram_model, ferdowsi_unigram_model
    if poet == "hafez":
        return hafez_backoff_model, hafez_bigram_model, hafez_unigram_model
    if poet == "molavi":
        return molavi_backoff_model, molavi_bigram_model, molavi_unigram_model


def get_poet(flag):
    if flag == 1:
        return "ferdowsi"
    if flag == 2:
        return "hafez"
    if flag == 3:
        return "molavi"


def get_max(ferdowsi_prob, hafez_prob, molavi_prob):
    if ferdowsi_prob >= hafez_prob:
        if ferdowsi_prob >= molavi_prob:
            return 1
        else:
            return 3
    else:
        if hafez_prob >= molavi_prob:
            return 2
        else:
            return 3


landa1 = 0.003
landa2 = 0.007
landa3 = 0.99
e = 0.002

ferdowsi_unigram_model = dict()
ferdowsi_bigram_model = dict()
ferdowsi_backoff_model = dict()

hafez_unigram_model = dict()
hafez_bigram_model = dict()
hafez_backoff_model = dict()

molavi_unigram_model = dict()
molavi_bigram_model = dict()
molavi_backoff_model = dict()

if __name__ == '__main__':
    ferdowsi_backoff_model, ferdowsi_bigram_model, ferdowsi_unigram_model = build_all_models("ferdowsi")
    hafez_backoff_model, hafez_bigram_model, hafez_unigram_model = build_all_models("hafez")
    molavi_backoff_model, molavi_bigram_model, molavi_unigram_model = build_all_models("molavi")

    print(accuracy())
