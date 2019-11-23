# -*- coding: utf-8 -*-
"""TF-IDF_moive_recomment_sample.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PN6Xij84xKiyNMaUDimoOq2xkaHnx5j7
"""

#https://wikidocs.net/24603

from google.colab import drive
import os
drive.mount('/content/gdrive')

file_name = 'movies_metadata.csv'
review_file = open(os.path.join('/content/gdrive/My Drive/AI/HS', file_name))

import pandas as pd
data = pd.read_csv(review_file, low_memory=False)
# 예를 들어 윈도우 바탕화면에 해당 파일을 위치시킨 저자의 경우
# pd.read_csv(r'C:\Users\USER\Desktop\movies_metadata.csv', low_memory=False)
data.head(2)

data=data.head(20000)
print(data['overview'].isnull().sum())

data['overview'] = data['overview'].fillna('')
# overview에서 Null 값을 가진 경우에는 값 제거
print(data['overview'].isnull().sum())

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['overview'])
# overview에 대해서 tf-idf 수행
print(tfidf_matrix.shape)

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['title']).drop_duplicates()
print(indices.head())

idx = indices['Father of the Bride Part II']
print(idx)

def get_recommendations(title, cosine_sim=cosine_sim):
    # 선택한 영화의 타이틀로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 영화를 가지고 연산할 수 있습니다.
    idx = indices[title]

    # 모든 영화에 대해서 해당 영화와의 유사도를 구합니다.
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 영화들을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 영화를 받아옵니다.
    sim_scores = sim_scores[1:11]

    # 가장 유사한 10개의 영화의 인덱스를 받아옵니다.
    movie_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 영화의 제목을 리턴합니다.
    return data['title'].iloc[movie_indices]

get_recommendations('The Dark Knight Rises')

