"""
Scrapes obituaries from genaeologytrails.com.
"""

import re
import requests
import nltk
from bs4 import BeautifulSoup

BS4_DECODER = "html.parser"


def preprocess_obit(obit_text):
    """Create sets of words from obit text."""
    tokenizer = nltk.RegexpTokenizer("\w+")
    tokens = tokenizer.tokenize(obit_text)

    words = set()
    for token, tag in nltk.pos_tag(tokens):
        # Eliminate pronouns, plural pronouns, punctuation and digits
        if tag not in ["NNP", "NNPS", "CD", "IN"]:
            words.add(token.lower())

    return words


EXAMPLE_OBITS = [
    preprocess_obit(x) for x in (
    "Little Willie, an infant son of Jas. Allen, of Selma, was burned to death last week.",

    "KILLED BY A TRAM CAR - Bert Hatcher, a chainer at Piper Mines, Bibb County, was killed "
    "last week by being struck by a wild tram are which broke loose and ran down into the mine"
    " at a terrific speed. A mule was also killed and several miners had narrow escapes.",
        
    "MITCHELL, Rev. JAMES M."
    "Departed this life on the 13th Instant, Rev. James M. Mitchell, of this vicinity, in the 30th year of his age.  "
    "He was a native son of East Tennessee, and settled in this place during the summer of 1836.  He has consequently "
    "resided in this community, during the period of about two years only.  But not withstanding the shortness of his "
    "sojourn here, all will unite in bearing testimony to his amiable character, and worthy deportment.  As a citizen, "
    "he was distinguished for his attachment to the good order of society, and the promotion of correct principles.  "
    "As a friend, he was ardent and unshaken.  As a Husband and Father, he was kind, tender and affectionate; and as a "
    "Christian, he was zealous, and highly exemplary."
    "During his last illness, he exhibited many satisfactory evidences that he was prepared to receive that Crown of "
    "glory, which is held in reservation for all the truly faithful, at the right hand of God.  Under these mournfully "
    "pleasing circumstances he left us, and is gone from this world forever. All must regret his loss; for the chasm "
    "occasioned in society by his exit, may not soon be filled.  He cannot return to us, but we may go to him. "
    "Blessed are the death which die in the lord form henceforth; Yea, saith the Spirit, that they may rest from their "
    "labors; and their works do follow them."
    )
]


def get_jaccard_sim(a, b):
    """Get the character-wise Jaccard similarity of two strings."""
    return float(len(a.intersection(b))) / len(a.union(b))


def find_obits_on_page(page_url):
    resp_content = requests.get(page_url).content.decode('latin')
    page = BeautifulSoup(resp_content, BS4_DECODER)

    for para in page.find_all("p"):
        tokens = preprocess_obit(para.text)
        sims = [get_jaccard_sim(tokens, ex) for ex in EXAMPLE_OBITS]
        print(sims, tokens)


def find_obit_pages(state_site_url):
    return _find_obit_candidates(state_site_url)


def _find_obit_candidates(url):
    """Recursive helper for find_obit_pages"""
    print("Searching: %s" % url)
    resp_content = requests.get(url).content.decode('latin')

    to_search, matches = [], []
    site_home = BeautifulSoup(resp_content, BS4_DECODER)
    links = site_home.find_all("a", href=True)
    for link in links:
        # Check if the link leads forward in the site. If so, search it.
        if link["href"].startswith(url) and len(link["href"]) > len(url):
            to_search.append(link["href"])

            # Search the link string for the word "Obituaries". If it exists, it's a match.
            if re.search("obit(ua(ry|ries))?", link.text.lower()):
                print("FOUND: %s" % link["href"])
                matches.append(link["href"])

    for link in to_search:
        matches.extend(_find_obit_candidates(link))

    return matches


if __name__ == "__main__":
    state_sites = [line.strip() for line in open("state_sites.txt", 'r')]
    # print(find_obit_pages(state_sites[0]))
    find_obits_on_page("http://genealogytrails.com/ala/dallas/news_deathobits.html")
