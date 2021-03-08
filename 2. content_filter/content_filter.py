# Librerias
from mysql.connector import connection
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

# Lectura de archivos
# ds = pd.read_csv("C:\\Users\\luisc\\Documents\\UNSA PROYECTO\\pdt_Implementaciones\\1. db_reader\\sample_test_ENG_copia.csv", sep='@', encoding='utf-8', error_bad_lines=False)
# ds = pd.read_csv("..\\1. db_reader\\sample_test_ENG.csv", sep=';', encoding='utf-8', error_bad_lines=False)
# ds = pd.read_csv("..\\1. db_reader\\NEW_pipes_data_test.csv", sep='|', encoding='utf-8', error_bad_lines=False)
ds = pd.read_csv("..\\1. db_reader\\NEW_pipes_data_test_es.csv", sep='|', encoding='utf-8', error_bad_lines=False)

# TF + IDF
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0)
tfidf_matrix = tf.fit_transform(ds['utility']) #name

# matriz
print(tf.get_feature_names())
print(tfidf_matrix.shape)
m = np.array(tf)
print(m)
# Similitud de Coseno
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}
idx_results = []
idx_index = []
idx_names = []

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
    results[row['id']] = similar_items[1:]
    
print('\n')

def itemuti(id):
    return ds.loc[ds['id'] == id]['utility'].tolist()[0].split(' | ')[0]

def itemname(id):
    return ds.loc[ds['id'] == id]['name'].tolist()[0].split(' | ')[0]

def itemid(id):
    return ds.loc[ds['id'] == id]['id'].to_string().split(' ')[-1]

# Just reads the results out of the dictionary.
def recommend(item_id, num):
    print("\nRecommending " + str(num).upper() + " similar TEAs to"+"[" + itemid(item_id) + "]:" + itemname(item_id).upper())
    print("----------------")
    print("UTILIDAD -> ")
    print(str(itemuti(item_id)).upper())
    print("----------------")
    recs = results[item_id][:num]
    for rec in recs:
        print("\nRecommendations: " + 
        "[" + itemid(rec[1]) + "] " + str(itemname(rec[1])).upper() +": " + itemuti(rec[1]) + "\n (score:" + str(rec[0]) + ")")
        print("----------------")
        # print(str(itemname(rec[1])).upper())
        print("----------------")
        idx_results.append(str(rec[0])) # score
        idx_index.append(itemid(rec[1]))
        idx_names.append(itemname(rec[1]))

def score_word(dat):
    return


recommend(item_id=30, num=5)
print(idx_results)
print(idx_index)
print(idx_names)

######################################################################################################################
################################################## INSERT TO BD ######################################################
######################################################################################################################
import mysql.connector

schema = 'tecnicas_ratings' # SPANISH
# schema = 'techniques_eng' # ENGLISH

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="tecnicasdb"
)

def describe_db(database, schema):
    '''
    Describe la base de datos y sus componentes
    '''
    mycursor = database.cursor()
    mycursor.execute("DESCRIBE " + schema)
    cadena = []
    for x in mycursor:
        cadena.append(x)
        # print(x)
    # print(cadena)
    return cadena

def save_db(database, scheme, scores, indexes, names, item_id):

    mycursor = database.cursor()
    for s, i, n in scores, indexes, names:

        query = "(INSERT INTO" + schema +".scores (id, name, score) VALUES (%s, %s, %s)"
        values = (s,i,n)
        mycursor.execute(query, values)
        connection.commit()

    
save_db(db, schema, idx_results, idx_names, idx_index, item_id=30)

