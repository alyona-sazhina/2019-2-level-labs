import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    if not texts or not isinstance(texts, list):
        return []
    clean_token_corpus = []
    for one_text in texts:
        if not isinstance(one_text, str):
            continue
        while '<br />' in one_text:
            one_text = one_text.replace("<br />", " ")
        new_text = ''
        for symbol in one_text:
            if symbol.isalpha() or symbol == ' ':
                new_text += symbol
        new_text = new_text.lower()
        corpus1 = new_text.split(' ')
        corpus = []
        for word in corpus1:
            if word != '':
                corpus.append(word)
        clean_token_corpus.append(corpus)
    return clean_token_corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']

    def calculate_tf(self):
        if self.corpus:
            for one_text in self.corpus:
                if not one_text:
                    continue
                tf_values = {}
                if one_text:
                    len_text = len(one_text)
                    for word in one_text:
                        if not isinstance(word, str):
                            len_text -= 1
                for word in one_text:
                    if isinstance(word, str) and word not in tf_values:
                        count_word = one_text.count(word)
                        tf_values[word] = count_word / len_text
                self.tf_values.append(tf_values)
        return self.tf_values

    def calculate_idf(self):
        if self.corpus:
            for one_text in self.corpus:
                if not one_text:
                    continue
                new_corpus = []
                for word in one_text:
                    if word not in new_corpus and isinstance(word, str):
                        new_corpus += [word]
                count_words = {}
                for word in new_corpus:
                    count_word = 0
                    for text_ in self.corpus:
                        if not text_ or word in text_:
                            count_word += 1
                    count_words[word] = count_word
                    if word in count_words.keys():
                        self.idf_values[word] = math.log(len(self.corpus) / count_words[word])
            return self.idf_values

    def calculate(self):
        if self.idf_values and self.tf_values:
            for one_text in self.tf_values:
                tf_idf_values = {}
                for word, tf_value in one_text.items():
                    tf_idf_values[word] = tf_value * self.idf_values[word]
                self.tf_idf_values.append(tf_idf_values)
        return self.tf_idf_values

    def report_on(self, word, document_index):
        if not self.tf_idf_values or document_index >= len(self.tf_idf_values):
            return ()
        tf_idf_dict = self.tf_idf_values[document_index]
        if word not in tf_idf_dict:
            return ()
        list_tf_idf = sorted(tf_idf_dict, key=tf_idf_dict.__getitem__, reverse=True)  # создаем список значений словаря
        # print(tf_idf_dict)                                                            # и сортируем его по убыванию
        # print(list_tf_idf)
        return tf_idf_dict[word.lower()], list_tf_idf.index(word.lower())

    def dump_report_csv(self):
        with open("report.csv", "w", encoding="utf-8") as report:
            tf_str = ""
            tf_idf_str = ""
            for i in self.file_names:
                tf_str += "tf_" + i + ","
                tf_idf_str += "tf_idf_" + i + ","
            first_line = "word," + tf_str + "idf," + tf_str[:-1]
            table = [first_line]
            dict_report = {}
            for index, text_dict in enumerate(self.tf_values):
                if text_dict:
                    for word, tf_value in text_dict.items():
                        idf_value = self.idf_values[word]
                        tf_idf_again = tf_value * idf_value
                        dict_report[word+str(index)] = str(tf_value) + ','
                        dict_report[word+str(index)] += str(idf_value) + ","
                        dict_report[word+str(index)] += str(tf_idf_again)
            reports = []
            sorted_report = sorted(dict_report.items())
            list_words = []
            for word_and_value in sorted_report:
                word_with_index = word_and_value[0]
                values = word_and_value[1].split(',')
                word = word_with_index[:-1]
                if word not in list_words:
                    report_text = ["0" for _ in range(len(self.corpus) * 2 + 2)]
                index = int(word_with_index[-1])
                report_text[0] = word
                report_text[index+1] = values[0]   # TF
                report_text[len(self.corpus) + 1] = values[1]   # IDF
                report_text[len(self.corpus) + index + 2] = values[2]   # TF-IDF
                if word in list_words:
                    reports[-1] = report_text
                else:
                    reports.append(report_text)
                list_words.append(word)
            for i in reports:
                new_line = ",".join(i)
                table.append(new_line)
            result = "\n".join(table)
            report.write(result)

    def cosine_distance(self, index_text_1, index_text_2):
        if index_text_1 >= len(self.corpus) or index_text_2 >= len(self.corpus):
            return 1000
        new_words = []
        text_1 = self.corpus[index_text_1]   # список слов текста 1
        text_2 = self.corpus[index_text_2]   # список слов текста 2
        for word in text_1:
            if word not in new_words:
                new_words.append(word)
        for word in text_2:
            if word not in new_words:
                new_words.append(word)

        vector_1 = [0 for _ in range(len(new_words))]
        vector_2 = [0 for _ in range(len(new_words))]

        tf_idf_values = {}
        for text_dict in self.tf_idf_values:
            tf_idf_values.update(text_dict)

        for index, word in enumerate(new_words):
            if word in text_1:
                vector_1[index] = tf_idf_values[word]
            elif word not in text_1:
                vector_1[index] = 0
            if word in text_2:
                vector_2[index] = tf_idf_values[word]
            elif word not in text_2:
                vector_2[index] = 0

        numerators = [vector_1[i] * vector_2[i] for i in range(len(new_words))]
        numerator = sum(numerators)
        denominators_1 = sum([i**2 for i in vector_1])
        denominators_2 = sum([i**2 for i in vector_2])
        denominator = math.sqrt(denominators_1) * math.sqrt(denominators_2)

        cos_vectors = numerator / denominator
        return cos_vectors


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
