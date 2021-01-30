def get_sentences(poet):
    filePath = "train_set\\" + poet + "_train.txt"
    temp_list = list()
    punctuations = ".،:؛!؟*\"\'«»"
    with open(filePath, 'r') as f:
        for line in f.readlines():
            line = line.translate(line.maketrans('', '', punctuations))
            line = "</s> " + line.rstrip("\n") + " <s>"
            temp_list.append(line)
    return temp_list


def get_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = sentence.split()
        for word in sentence:
            temp_list.append(word)
    return temp_list


def build_dictionary(words):
    frequencies_dict = dict()
    for word in words:
        if word in frequencies_dict:
            newFrequency = frequencies_dict[word] + 1
            frequencies_dict.update({word: newFrequency})
        else:
            frequencies_dict.update({word: 1})
    temp_dict = frequencies_dict.copy()
    for word in temp_dict:
        if temp_dict.get(word) <= 5:
            frequencies_dict.pop(word)
    return frequencies_dict


if __name__ == '__main__':
    ferdowsi_all_sentences = get_sentences("ferdowsi")
    hafez_all_sentences = get_sentences("hafez")
    molavi_all_sentences = get_sentences("molavi")

    ferdowsi_all_words = get_words(ferdowsi_all_sentences)
    hafez_all_words = get_words(hafez_all_sentences)
    molavi_all_words = get_words(molavi_all_sentences)

    ferdowsi_dict = build_dictionary(ferdowsi_all_words)
    hafez_dict = build_dictionary(hafez_all_words)
    molavi_dict = build_dictionary(molavi_all_words)
