from math import log

import os

import re

import string

import math



def list_of_files(directory, extension):

    files_names = []

    for filename in os.listdir(directory):

        if filename.endswith(extension):

            files_names.append(filename)

    return files_names





def extract_president_names(file_name):


    name_pattern = re.compile(r'\b(?:Chirac|Giscard dEstaing|Hollande|Macron|Mitterand|Sarkozy)\s+(.*?)\b', re.IGNORECASE)

    match = name_pattern.search(file_name)

    if match:

        return match.group(1)

    return None





def associate_first_name(president_names):



    name_mapping = {

        "Chirac": "Jacques Chirac",

        "Giscard dEstaing": "Valéry Giscard dEstaing",

        "Mitterrand": "François Mitterrand",

        "Macron": "Emmanuel Macron",

        "Sarkozy": "Nicolas Sarkozy",

        "Hollande": "François Hollande"

    }



    first_names = []



    for full_name in president_names:

        first_name = name_mapping.get(full_name, "Unknown")

        first_names.append(first_name)

    return first_names





def pres_name(files_names):



    tab_all_name = []

    dic = {"Chirac": "Jacques Chirac",

           "Giscard dEstaing": "Valéry Giscard dEstaing",

           "Mitterrand": "François Mitterrand",

           "Macron": "Emmanuel Macron",

           "Sarkozy": "Nicolas Sarkozy",

           "Hollande": "François Hollande"

           }

    for name in files_names:

        if name[-5] == "1" or name[-5] == "2":

            tab_all_name.append(dic[name[11:-5]])

        else:

            tab_all_name.append(dic[name[11:-4]])

    tab_all_name = list(set(tab_all_name))

    return tab_all_name





def display_president_names(president_names):



    unique_names_set = set(president_names)



    print("List of President Names:")

    for name in unique_names_set:

        print(name)





def clean_and_store_files(input_dir, output_dir):



    cleaned_dir = os.path.join(os.path.dirname(__file__), output_dir)

    os.makedirs(cleaned_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):

        if file_name.endswith(".txt"):

            input_path = os.path.join(input_dir, file_name)

            output_path = os.path.join(cleaned_dir, file_name)

            with open(input_path, 'r', encoding='utf-8') as infile:

                content = infile.read().lower()

                content = content.replace("’", " ")

                content = content.replace("'", " ")  # Handle apostrophe

                content = content.replace(",", "")

                content = content.replace("–", " ")  # Handle dash

                content = content.replace("!", "")

                content = content.translate(str.maketrans('', '', string.punctuation))

                content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())

            with open(output_path, 'w', encoding='utf-8') as outfile:

                outfile.write(content)





def calculate_tf(a_string):



    dic_tf = {}

    for words in a_string.split(" "):

        for word in words.split("\n"):

            if word.strip() not in dic_tf:

                dic_tf[word.strip()] = 1

            else:

                dic_tf[word.strip()] += 1

    return dic_tf





def calculate_idf(directory):


    idf = {}

    wordset = []

    modified_wordset = []

    list_doc = list_of_files(directory, 'txt')

    for doc in list_doc:

        with open(os.path.join(directory, doc), 'r', encoding='utf-8') as f:

            string_doc = f.read()

            wordset.append(set(string_doc.split()))



    for i in range(len(wordset) - 1):

        modified_wordset.append(list(wordset[i]))



    for i in range(len(modified_wordset) - 1):

        for word in modified_wordset[i]:

            if word in modified_wordset[i + 1]:

                if word not in idf:

                    idf[word] = 1

                else:

                    idf[word] += 1

    for value in idf.keys():

        idf[value] = log(len(list_doc) / idf[value])



    return idf





def td_idf_matrix(directory):


    matrix = []

    combined_dic = {}

    idf = calculate_idf(directory)

    for file_name in list_of_files(directory, 'txt'):

        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:  # the list with all the file name

            f = file.read()

            combined_dic.update(calculate_tf(f))



    for file_name in list_of_files(directory, 'txt'):

        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:

            f = file.read()

            tf = calculate_tf(f)



            tf_idf_vector = {word: tf_value * idf.get(word, 0) for word, tf_value in tf.items()}

            matrix.append(tf_idf_vector)



    return matrix
def tokenize_question(question):
    clean_question = clean_and_store_files()  # Removes all punctuation and lowercases the question
    word_list_question = clean_question.split(" ")
    return word_list_question

def search_word(word_list_question, tf_idf_matrix):
    found_words_list = []
    for word in word_list_question:
        if word in tf_idf_matrix:
            found_words_list.append(word)
    return found_words_list

def tf_question(word_list_question, tf_idf_matrix):
    tf_question_dict = {}
    for word in tf_idf_matrix.keys():
        if word in word_list_question:
            tf_question_dict[word] = word_list_question.count(word) / len(word_list_question)
        else:
            tf_question_dict[word] = 0
    return tf_question_dict

def calculate_tf_idf_vector_question(path, word_list_question, tf_idf_matrix, with_key=False):
    idf_question = calculate_idf(path)
    tf_question_result = tf_question(word_list_question, tf_idf_matrix)
    tf_idf_question = 0
    if with_key:
        vector_list = {}
    else:
        vector_list = []
    for word in idf_question.keys():
        if with_key:
            tf_idf_question += idf_question[word] * tf_question_result[word]
            vector_list[word] = idf_question[word] * tf_question_result[word]
        else:
            tf_idf_question += idf_question[word] * tf_question_result[word]
            vector_list.append(idf_question[word] * tf_question_result[word])
    return vector_list

def dot_product(vectA, vectB):
    sumAB = 0
    m = len(vectB)
    for i in range(0, m):
        sumAB = sumAB + (float(vectA[i]) * float(vectB[i]))
    return sumAB

def vector_norm(vect):
    sum = 0
    m = len(vect)
    for i in range(0, m):
        sum = sum + (vect[i] * vect[i])
    sum = sqrt(sum)
    return sum

def calculate_similarity(vectA, vectB):
    result = dot_product(vectA, vectB) / (vector_norm(vectA) * vector_norm(vectB))
    return result

def calculate_relevant_document(tf_idf_matrix, tf_idf_vector_question, file_name_list):
    matrix_length = len(tf_idf_matrix)
    max_similarity = 0
    doc_id = None
    for i in range(0, matrix_length):
        current_similarity = calculate_similarity(tf_idf_vector_question, tf_idf_matrix[i])
        if current_similarity > max_similarity:
            max_similarity = current_similarity
            doc_id = i
    return file_name_list[doc_id]

def best_tf_idf(path, word_list_question, tf_idf_matrix):
    question_vector = calculate_tf_idf_vector_question(path, word_list_question, tf_idf_matrix, True)
    max_tf_idf = 0
    max_word = None
    for word, value in question_vector.items():
        if value > max_tf_idf:
            max_tf_idf = value
            max_word = word
    return max_word

def relevant_response(file, word):
    opened_file = open(file, "r", encoding='UTF-8')
    lines = opened_file.readlines()
    relevant_sentence = ""
    for line in lines:
        if line.find(word) > -1:
            relevant_sentence = line
            break
    if relevant_sentence:
        first_character = relevant_sentence[0].lower()
        rest_of_sentence = relevant_sentence[1:]
        return first_character + rest_of_sentence
    else:
        return relevant_sentence

def generate_response(relevant_sentence, question):
    generated_questions = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr! ",
        "comment": "Après analyse, ",
        "pourquoi": "Car, ",
        "peux-tu": "Oui, bien sûr! "
    }

    for word, response in generated_questions.items():
        if word in question:
            generated_response = generated_questions[word] + relevant_sentence
            return generated_response
        else:
            generated_response = relevant_sentence
            if generated_response:
                first_character = generated_response[0].upper()
                rest_of_sentence = generated_response[1:]
                return first_character + rest_of_sentence
            else:
                return generated_response




