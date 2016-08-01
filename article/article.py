import datetime
import requests
import jinja2
import json
import markdown


KNOWN_LICENCES = {
    "CC-BY-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.""",
    "CC-BY-SA-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.""",
    "CC-BY-NC-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.""",
    "CC-BY-ND-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/">Creative Commons Attribution-NoDerivatives 4.0 International License</a>.""",
    "CC-BY-NC-ND-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.""",
    "CC-BY-NC-SA-4.0": """<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.""",
}

contributors_dict = dict()


def add_contributors(people):
    for k in people:
        contributors_dict[k] = people[k]


def read_date(date_str):
    if len(date_str) == 10:
        return datetime.datetime.strptime(date_str, "%d/%m/%Y")
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")


class GistArticle(object):

    valid = False

    def __init__(self, gist_id):
        self.gist_id = gist_id
        # TODO: OAuth
        result = requests.get("https://api.github.com/gists/" + gist_id)
        if not result.status_code == 200:
            return
        self.data = json.loads(result.content)

        # Try loading up the article
        if 'article.json' not in self.data['files']:
            return

        self.meta = json.loads(self.data['files']['article.json']['content'])

        self.contributors = self.meta["contributors"]

        self.valid = True

    @property
    def file_names(self):
        return self.data['files'].keys()

    @property
    def image_names(self):
        image_ext = ('png', 'jpeg', 'jpg', 'gif', 'tif', 'tiff')
        return [
            fn for fn in self.file_names
            if fn.split('.')[-1].lower() in image_ext
        ]

    @property
    def avatar(self):
        return contributors_dict[self.contributors["authors"][0]]['avatar']

    @property
    def source(self):
        return "https://gist.github.com/" + self.gist_id

    @property
    def date(self):
        return read_date(self.meta['date_published'])

    @property
    def content(self):
        content = self.data["files"][self.meta["article"]]["content"]
        for img in self.image_names:
            raw_img = self.data["files"][img]["raw_url"]
            content = content.replace(img, raw_img)
        return content

    # HTML rendering targets

    @property
    def html_title(self):
        return self.meta['title']

    @property
    def html_authors(self):
        return contributors_dict[self.contributors["authors"][0]]['name']

    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ])

    @property
    def html_license(self):
        return KNOWN_LICENCES["CC-BY-4.0"]

    def to_json(self):
        return {
            "article_type": "gist",
            "gist_id": self.gist_id,
            "authors": ', '.join([
                contributors_dict[a_id]['name']
                for a_id in self.contributors["authors"]
            ]),
            "title": self.meta['title'],
            "description": self.meta['description'],
            "thumbnail": self.data["files"][self.meta["thumbnail"]]["raw_url"],
            "date": self.meta['date_published'],
        }
