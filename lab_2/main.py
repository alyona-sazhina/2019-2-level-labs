"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows, num_cols):
    if type(num_rows) is int and type(num_cols) is int:
        edit_matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
        return edit_matrix
    else:
        return []


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    i, j = 0, 0
    edit_matrix = list(edit_matrix)
    if type(add_weight) is int and type(remove_weight) is int and edit_matrix and edit_matrix[0]:
        for _ in edit_matrix:
            edit_matrix[0][0] = 0
            edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight
            i += 1
        for _ in edit_matrix[0]:
            edit_matrix[0][0] = 0
            edit_matrix[0][j] = edit_matrix[0][j - 1] + add_weight
            j += 1
        print(edit_matrix)
        return edit_matrix
    else:
        return edit_matrix


def minimum_value(numbers: tuple) -> int:
    min1 = 32000
    for i in numbers:
        if i < min1:
            min1 = i
    return min1


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    a, b, c = 0, 0, 0
    if type(add_weight) is int and type(remove_weight) is int and type(substitute_weight) is int and original_word:
        for i in range(1, len(edit_matrix)):
            for j in range(1, len(edit_matrix[i])):
                a = edit_matrix[i - 1][j] + remove_weight
                b = edit_matrix[i][j - 1] + add_weight
                if original_word[i - 1] != target_word[j - 1]:
                    c = edit_matrix[i - 1][j - 1] + substitute_weight
                else:
                    c = edit_matrix[i - 1][j - 1]
                edit_matrix[i][j] = minimum_value((a, b, c))
        return list(edit_matrix)
    else:
        return list(edit_matrix)


def save_to_csv(edit_matrix, path_to_file):
    file = open(path_to_file, 'w')
    for i in edit_matrix:
        for j in i:
            a = str(j) + ','
            file.write(a)
        file.write('\n')
    file.close()


def load_from_csv(path_to_file):
    file = open(path_to_file)
    edit_matrix = []
    for line in file:
        row = line.split(',')
        row1 = []
        for i in row:
            row1.append(int(i))
        edit_matrix.append(row1)
    file.close()
    print(edit_matrix)
    return edit_matrix


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if type(original_word) is str and type(target_word) is str and \
            type(add_weight) is int and type(remove_weight) is int and type(substitute_weight) is int:
        num_rows = len(original_word) + 1
        num_cols = len(target_word) + 1
        edit_matrix = generate_edit_matrix(num_rows, num_cols)
        initialize_edit_matrix(tuple(edit_matrix), add_weight, remove_weight)
        fill_edit_matrix(edit_matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
        save_to_csv(edit_matrix, 'save.csv')
        print(edit_matrix[num_rows - 1][num_cols - 1])
        return edit_matrix[num_rows - 1][num_cols - 1]
    else:
        return -1
