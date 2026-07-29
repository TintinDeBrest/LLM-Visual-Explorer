# projections.py

from sklearn.decomposition import PCA 

def compute_pca(embeddings):
    pca = PCA(n_components=3)
    xyz = pca.fit_transform(embeddings)
    return xyz, pca
