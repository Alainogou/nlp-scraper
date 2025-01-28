

def entities_detection(text, nlp):
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        if entity.label_ == 'ORG' and entity.text not in  entities:  
            entities.append( entity.text)
            
    return entities
