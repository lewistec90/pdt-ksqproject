import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# ds = pd.read_csv("C:\\Users\\luisc\\Documents\\UNSA PROYECTO\\pdt_Implementaciones\\1. db_reader\\sample_test_ENG_copia.csv", sep='@', encoding='utf-8', error_bad_lines=False)
# ds = pd.read_csv("..\\1. db_reader\\sample_test_ENG.csv", sep=';', encoding='utf-8', error_bad_lines=False)
ds = pd.read_csv("..\\1. db_reader\\NEW_pipes_data_test.csv", sep='|', encoding='utf-8', error_bad_lines=False)

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0)
tfidf_matrix = tf.fit_transform(ds['utility']) #name
print(tf.get_feature_names())
print(tfidf_matrix.shape)


cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    results[row['id']] = similar_items[1:]
    
print('\n')

def item(id):
    return ds.loc[ds['id'] == id]['utility'].tolist()[0].split(' - ')[0]

def itemname(id):
    return ds.loc[ds['id'] == id]['name'].tolist()[0].split(' - ')[0]

# Just reads the results out of the dictionary.
def recommend(item_id, num):
    print("\nRecommending " + str(num) + " products similar to " + item(item_id) + "...")
    print(str(itemname(item_id)).upper())
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("\nRecommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")
        print(str(itemname(rec[1])).upper())

recommend(item_id=10, num=5)