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


class MDArticle(object):

    def __init__(self, slug):
        with open("articles/{}.json".format(slug), "r") as f:
            self.meta = json.loads(f.read())
        with open("articles/{}.md".format(slug), "r") as f:
            self.content = f.read()

        self.contributors = self.meta["contributors"]

    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ])

    @property
    def avatar(self):
        return contributors_dict[self.contributors["authors"][0]]['avatar']

    @property
    def source(self):
        return "https://gist.github.com/" + self.gist_id

    @property
    def date(self):
        return read_date(self.meta['date_published'])

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
