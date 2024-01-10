from math import log

import os

import re

import string





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
fonction tokenisation de la question
def tokenisation_question(question):
    question_clean = changer_le_format(question)  # permet d'enlever toutes les ponctuations et de lower la question
    liste_de_mot_question = question_clean.split(" ")
    return liste_de_mot_question


# fonction calcul de la similarité

def recherche_mot(liste_mot_question, matrice_tf_idf):
    list_mot_trouves = []# Création d'une liste
    for mot in liste_mot_question: #Parcours de la liste
        if mot in matrice_tf_idf: #Si le mot se trouve dans la matrice tf_idf amors ça l'ajoute à liste qu'on vient créer
            list_mot_trouves.append(mot)

    return list_mot_trouves


def tf_question(liste_mot_question, matrice_tf_idf):
    dico_tf_question = {}  # création d'un dico
    for mot in matrice_tf_idf.keys():  # Parcours de la matrice tf-idf
        if mot in liste_mot_question:  # Si le mot de la question se trouve dans le corpus on calcule le TF
            dico_tf_question[mot] = liste_mot_question.count(mot) / len(liste_mot_question)
        else:  # Sinon on met 0 en valeur
            dico_tf_question[mot] = 0
    return dico_tf_question


def calcul_vecteur_tf_idf_question(chemin, liste_mot_question, matrice_tf_idf, avec_cle=False):
    idf_qst = idf(chemin)  # Appel de la fonction IDF
    tf_qst = tf_question(liste_mot_question, matrice_tf_idf)  # Appel de la fonction TF de la question
    # print(tf_qst)
    tf_idf_qst = 0
    if avec_cle:  # Si cette variable est vrai alors liste vecteur est dico
        liste_vecteur = {}
    else:  # Sinon liste vecteur est une liste
        liste_vecteur = []
    for mot in idf_qst.keys():
        if avec_cle:
            tf_idf_qst += idf_qst[mot] * tf_qst[mot]
            liste_vecteur[mot] = idf_qst[mot] * tf_qst[mot]
        else:
            tf_idf_qst += idf_qst[mot] * tf_qst[mot]
            liste_vecteur.append(idf_qst[mot] * tf_qst[mot])


    return liste_vecteur


def produit_scalaire(vectA, vectB):
    sommeAB = 0  # Initialisation d'une variable somme
    m = len(vectB)
    for i in range(0, m):
        """print(i)
        print("Vecteur A : ", vectA[i])
        print("Vecteur B : ", vectB[i])"""
        sommeAB = sommeAB + (float(vectA[i]) * float(
            vectB[i]))  # Somme du produit de  chaque élément du produits des vecteurs A et B
    # print("Somme AB :",sommeAB)
    return sommeAB


def norme_vecteur(vect):
    somme = 0
    m = len(vect)
    for i in range(0, m):
        somme = somme + (vect[i] * vect[i])  # Somme des carrées de chaquue élément du vecteur A

    somme = sqrt(somme)  # Racine carée de la somme du des carrées de chaque élément du vecteur A
    """print("Norme :",somme)"""
    return somme


def calcul_similarité(vectA, vectB):
    """print("Vecteur A : " ,vectA)
    print("Vecteur B :",vectB)"""
    resultat = produit_scalaire(vectA, vectB) / (norme_vecteur(vectA) * norme_vecteur(vectB))  # Calcul de la similarité

    return resultat


def calcul_document_pertinent(matrice_tf_idf, vecteur_tf_idf_question, liste_noms_fichiers):
    matval = len(matrice_tf_idf)  # calcul la longueur de la matrice
    similariteMax = 0  # initialisation de la vraible similariteMax
    idDoc = None  # initialisation de la variable idDoc
    for i in range(0, matval):
        similariteCourante = calcul_similarité(vecteur_tf_idf_question,
                                               matrice_tf_idf[i])  # appel de la fonction de la calcul similarite
        if (
                similariteCourante > similariteMax):  # attribue à similarité max la plus grande valeur du calcul de similarité
            similariteMax = similariteCourante
            idDoc = i

    return liste_noms_fichiers[idDoc]  # renvoie le fichier correspondant à ce calcul


def meilleur_tf_idf(chemin, liste_mot_question, matrice_tf_idf):
    vecteur_question = calcul_vecteur_tf_idf_question(chemin, liste_mot_question, matrice_tf_idf,
                                                      True)  # Appel de la fonction calcul vecteur tf idf question
    tf_idf_max = 0
    mot_max = None
    for mot, valeur in vecteur_question.items(): #Parcours du dico vecteur question
        if (valeur > tf_idf_max): #Renvoie le mot du meilleur score tf idf du dico vecteur question
            tf_idf_max = valeur
            mot_max = mot
        # print("Avant: ", valeur, mot)

    return mot_max


def reponse_pertinente(fichier, mot):
    fichier_ouvert = open(fichier, "r", encoding='UTF-8')
    lignes = fichier_ouvert.readlines() #Transforme les lignes de fichier en liste
    phrase_pertinente = ""
    for ligne in lignes: #Parcours des lignes
        if ligne.find(mot) > -1: #Quand le mot pertinent est trouvé pour la première fois il renvoie la ligne entière où il apparait
            phrase_pertinente = ligne
            break
    if phrase_pertinente:  # Vérifie si la chaîne n'est pas vide
        premier_caractere = phrase_pertinente[0].lower()  # Premier caractère en minuscule
        reste_de_la_phrase = phrase_pertinente[1:]  # Le reste de la chaîne
        return premier_caractere + reste_de_la_phrase
    else:
        return phrase_pertinente


def generation_reponse(phrase_pertinente, question):
    questions_genere = { #Création d'un dico afin de générer des réponses plus vivantes
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr! ",
        "comment": "Après analyse, ",
        "pourquoi": "Car, ",
        "peux-tu": "Oui, bien sûr! "
    }

    for mot, reponse in questions_genere.items(): #Parcours du dico
        "reponse_genere = None"
        if mot in question: #Condition de si la clé du dico est dans la question posé par l'utilsateur alors ça met renvoie la valeur de clé plus la phrase pertinente
            reponse_genere = questions_genere[mot] + phrase_pertinente
            return reponse_genere
        else :
            reponse_genere = phrase_pertinente
            if reponse_genere:  #Met une majuscule à la première lettre de la phrase si elle a trouve l'une des clés du dico dans la question
                premier_caractere = reponse_genere[0].upper()
                reste_de_la_phrase = reponse_genere[1:]
                return premier_caractere + reste_de_la_phrase
            else:
                return reponse_genere