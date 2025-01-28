

def entities(text, nlp):
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        if entity.label_ == 'ORG' and entity.text not in  entities:  
            entities.append( entity.text)
            
    return entities




def entities_detection(df, nlp):

    orgs=[]

    for _, row in df.iterrows():
        
        text= row['Headline'] + ' ' +  row['Body']
        org=entities(text,  nlp )
        orgs.append(org)

        print(f'Detected {len(org)} companies which are {', '.join(org)}')

    return orgs
        