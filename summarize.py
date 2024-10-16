import spacy
import re
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Charger les modèles SpaCy pour le français et l'anglais
nlp_fr = spacy.load('fr_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')

# Fonction de prétraitement
def preprocess_text(text, lang='en'):
    # Retirer les caractères spéciaux et normaliser la casse
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Sélectionner le modèle selon la langue
    if lang == 'fr':
        nlp = nlp_fr
    else:
        nlp = nlp_en
    
    # Tokenisation des phrases
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    return sentences

# Fonction pour calculer la similarité entre les phrases
def sentence_similarity(sentences):
    # Convertir les phrases en vecteurs TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Calculer la similarité cosinus entre toutes les paires de phrases
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# Fonction pour construire le score de TextRank
def build_text_rank(sentences, similarity_matrix):
    # Créer un graphe où chaque phrase est un nœud
    graph = nx.from_numpy_array(similarity_matrix)
    
    # Appliquer l'algorithme de PageRank
    scores = nx.pagerank(graph)
    
    # Classer les phrases par leur score
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    return ranked_sentences

# Fonction principale de résumé
def summarize_text(text, lang='en', num_sentences=2):
    sentences = preprocess_text(text, lang)
    similarity_matrix = sentence_similarity(sentences)
    ranked_sentences = build_text_rank(sentences, similarity_matrix)
    
    # Limiter le résumé au nombre de phrases désiré
    summary = ' '.join([sent for score, sent in ranked_sentences[:num_sentences]])
    return summary