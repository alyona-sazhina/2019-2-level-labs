"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text):
    t1 = []
    freq_dict = {}
    if type(text) is str and text != '':
        text1 = text.lower()
        for i in text1:
            if i not in 'abcdefghijklmnopqrstuvwxyz ':
                text1 = text1.replace(i, '')
        t = text1.split(' ')
        for word in t:
            if word != '':
                t1.append(word)
        for word in t1:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
        return freq_dict
    else:
        return freq_dict


text = ""
frequencies = {}
stop_words = ()


def filter_stop_words(freq_dict, stop_words):
    if stop_words == None or freq_dict == None:
        if stop_words != None:
            return {}
        else: return freq_dict
    elif stop_words == None and freq_dict == None:
        return {}
    else:
        if stop_words != () and freq_dict != {}:
            for word in freq_dict.keys():
                if word not in stop_words and type(word) == str:
                    frequencies[word] = freq_dict[word]
            return frequencies
        elif stop_words == () and freq_dict != {}:
            return freq_dict
        else: return {}

top_n = 5

def get_top_n(frequencies, top_n):
    list_frequencies = list(frequencies.items())
    list_frequencies.sort(key=lambda i: i[1], reverse=True)
    toplist = []
    if top_n > 0:
        for i in list_frequencies:
            toplist += i
            top_n -= 1
            if top_n == 0:
                break
        for i in toplist:
            if type(i) is int:
                toplist.remove(i)
        toplist = tuple(toplist)
        return toplist
    else:
        return ()


calculate_frequences(text)
filter_stop_words(frequencies, stop_words)
get_top_n(frequencies, top_n)


