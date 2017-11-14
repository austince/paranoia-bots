from __future__ import unicode_literals

import random
from string import Template
import pycorpora

from .corpus import load_corpus

shows = pycorpora.get_file("film-tv/tv_shows")["tv_shows"]
body_parts = pycorpora.humans.bodyParts["bodyParts"]
nouns = pycorpora.words.nouns["nouns"]
verbs = pycorpora.words.verbs["verbs"]
adjs = pycorpora.words.adjs["adjs"]
adverbs = pycorpora.words.adverbs["adverbs"]
statesOfDrunk = pycorpora.words.states_of_drunkenness["states_of_drunkenness"]

people = load_corpus('words/people')

brainwash_template = Template('''
$noun is brainwashing our ${thing}s to be "$adj" "${verb}ers".
#${thing}s #ThinkAboutIt #TrustMe
''')


def brainwash(noun=random.choice(shows),
              thing=random.choice(people),
              adj=random.choice(statesOfDrunk),
              verb=random.choice(verbs)["present"]):
    return brainwash_template.substitute(locals())


all_wondering_template = Template('''
We all wonder what ${person}s do.
I'm positive they $adv $verb while ${verb2}ing $noun. #ThinkAboutIt
''')


def all_wondering(person=random.choice(people),
        adv=random.choice(adverbs),
        verb=random.choice(verbs)["present"],
        verb2=random.choice(verbs)["present"],
        noun=random.choice(nouns)):
    return all_wondering_template.substitute(locals())


jim_butcher_template = Template('''
Paranoid? Probably. But just because you're paranoid doesn't mean there isn't an $adj $thing about to eat your $part.
-- Jim Butcher
''')


def jim_butcher(adj=random.choice(adjs),
                thing=random.choice(nouns),
                part=random.choice(body_parts)):
    return jim_butcher_template.substitute(locals())


i_am_human_template = Template('''
Are we all bots? Act natural.
''')


def i_am_human():
    return i_am_human_template.substitute()

# All the generics just take a noun
# Simpler for now

generic1_template = Template('''
Can you trust the $noun? #TrustNoOne
''')

generic2_template = Template('''
What are they doing with $noun? #TrustNoOne
''')

generic3_template = Template('''
That is just what the $noun wants you to think. #TrustNoOne
''')

generic4_template = Template('''
I read on the radio that ${noun}s poisons us. #TrustNoOne
''')

def make_simple_response(noun):
    response_template = random.choice([
        generic1_template,
        generic2_template,
        generic3_template,
        generic4_template,
    ])

    return response_template.substitute(noun=noun)


if __name__ == "__main__":
    for i in range(20):
        print(brainwash().encode('utf-8'))
