import requests
import article
import json
from datetime import datetime


gist_ids = [
    # Add your new article to the top of this list
    # ---------- GIST ID ----------- #,  # **: Short description
    "ff695dc21d2ecad6d17615a767b2a0e8",  # LH: Primary-Secondary Approaches
    "4ef0f1b64a3cb0b4829c892ccc227d77",  # SK: Inversions of airborne TDEM
    "5bf4c95c56129ae1725921004b28b4ac",  # PF: A first peak into the black box
    "dad772ba49ad31ddf3a3f7944511682b",  # LH: Implementations of FDEM
    "0f202e7177997084c3c384e110b99af5",  # LH: IPython in Teaching
    "567b8a12fd9028178a7637421065ac70",  # SK: Moving between dimensions
    "071a3fb3cb2eebc4185ef9c2944cf9e8",  # RC: Exploring Julia
    "b43df5192cfa4eb596bce911eea3e531",  # SK: Nudging Geophysics
    "ab1b08887a78b0c3ecc606e37ca62516",  # RC: SimPEG at SciPy2014
]


with open("www/contributors.json", 'r') as f:
    article.add_contributors(json.loads(f.read()))

articles = []
for gist_id in gist_ids:
    ga = article.GistArticle(gist_id)
    articles.append(ga.to_json())

articles = sorted(
    articles,
    key=lambda d: datetime.strptime(d['date'], '%d/%m/%Y')
)[::-1]

with open("www/articles.json", "w") as f:
    f.write(json.dumps(articles, indent=4))
