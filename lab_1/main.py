"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text):
    freq_dict = {}
    if type(text) is str and text != '':
        text1 = text.lower()
        for i in text1:
            if i not in 'abcdefghijklmnopqrstuvwxyz ':
                text1 = text1.replace(i, '')
        t = text1.split(' ')
        for word in t:
            if word == '':
                continue
            elif word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
        return freq_dict
    else:
        return freq_dict


def filter_stop_words(freq_dict, stop_words):
    if freq_dict == {} or stop_words == () or stop_words is None:
        return freq_dict
    elif freq_dict is None and stop_words is None or freq_dict is None:
        return {}
    else:
        if stop_words != () and freq_dict != {}:
            for word in freq_dict.keys():
                if word not in stop_words and type(word) == str:
                    frequencies[word] = freq_dict[word]
            return frequencies


def get_top_n(frequencies, top_n):
    list_frequencies = list(frequencies.items())
    list_frequencies.sort(key=lambda i: i[1], reverse=True)
    top_list = []
    if top_n > 0:
        for i in list_frequencies:
            top_list += i
            top_n -= 1
            if top_n == 0:
                break
        for i in top_list:
            if type(i) is int:
                top_list.remove(i)
        top_list = tuple(top_list)
        return top_list
    else:
        top_list = tuple(top_list)
        return top_list


def read_from_file(path_to_file: str, lines_limit: int):
    file = open(path_to_file)
    k = 0
    text = ''
    for line in file:
        text += line
        k += 1
        if k == lines_limit:
            break
    file.close()
    return text


def write_to_file(path_to_file: str, content: tuple):
    file = open(path_to_file, 'w')
    for i in content:
        file.write(i)
        file.write('\n')
    file.close()


frequencies = {}
stop_words = ()
top_n = 5
lines_limit = top_n

text = read_from_file('data.txt', lines_limit)
freq_dict = calculate_frequences(text)
frequencies = filter_stop_words(frequencies, stop_words)
content = get_top_n(frequencies, top_n)
write_to_file('report.txt', content)