# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy

# import spacy.cli
# spacy.cli.download("en_core_web_sm")

def entities_detection(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    ent = []
    for entity in doc.ents:
        if entity.label_ == 'ORG':  
            ent.append(entity.text)
            
    return ent



text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

print(entities_detection(text))