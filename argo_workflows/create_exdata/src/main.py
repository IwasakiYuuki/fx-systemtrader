import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from sklearn.neighbors import NearestNeighbors


def main():
    """Annotate input text data and save it into local file.

    Annotate sentiment intensity of input text based degree of similarity to
    existing annotated dataset.
    For measure similarity, convert document to vector using doc2vec
    (jawiki dbow model) and measure distance of both vectors.
    * Currently, we use this method to measure sentiment intensity similarity,
    unclear if just language model can measure sentiment similarity.

    """

    model_df = pd.read_csv('/tmp/input_model.csv')
    data_df = pd.read_csv('/tmp/input_data.csv')

    model = Doc2Vec.load('/tmp/model_files/jawiki.doc2vec.dbow300d.model')

    def f_doc2vec(text):
        return model.infer_vector(text.split(' '))

    model_df['doc_vector'] = model_df['text'].apply(f_doc2vec)
    data_df['doc_vector'] = data_df['text'].apply(f_doc2vec)

    nbrs = NearestNeighbors(n_neighbors=1)
    nbrs.fit(model_df['doc_vector'].tolist())
    distances, indices = nbrs.kneighbors(data_df['doc_vector'].tolist())
    data_df['distance'] = pd.Series(distances.ravel())
    data_df['indice'] = pd.Series(indices.ravel())

    print(data_df['distance'].describe())
    print(data_df['indice'].value_counts())

    def f_get_model_intensity(indice):
        return model_df['intensity'][indice]

    def f_get_model_id_str(indice):
        return model_df['sentence_id'][indice]

    data_df['intensity'] = data_df['indice'].apply(f_get_model_intensity)
    data_df['indice_id_str'] = data_df['indice'].apply(f_get_model_id_str)

    data_df = data_df.drop(['doc_vector', 'indice'], axis=1)
    data_df['annotated'] = True
    data_df.to_csv('/tmp/output.csv', index=False)


if __name__ == "__main__":
    main()
