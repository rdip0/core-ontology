## Competency Questions for RDIP Ontology

### Prefixes
```sparql
PREFIX rdip: [http://example.org/rdip#](http://example.org/rdip#)
PREFIX vivo: [http://vivoweb.org/ontology/core#](http://vivoweb.org/ontology/core#)
PREFIX bibo: [http://purl.org/ontology/bibo/](http://purl.org/ontology/bibo/)
PREFIX dcat: [http://www.w3.org/ns/dcat#](http://www.w3.org/ns/dcat#)
PREFIX prov: [http://www.w3.org/ns/prov#](http://www.w3.org/ns/prov#)
PREFIX cito: [http://purl.org/spar/cito/](http://purl.org/spar/cito/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX xsd:  [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema#)
```

### Question 1
For a given dataset, which software (and version) was used in the activity that generated it?

```
SELECT ?dataset ?activity ?software ?softwareTitle ?version
WHERE {
  ?dataset a dcat:Dataset ;
           prov:wasGeneratedBy ?activity .

  ?activity rdip:usedSoftware ?software .

  OPTIONAL { ?software rdip:title   ?softwareTitle . }
  OPTIONAL { ?software rdip:version ?version . }

  # Restrict to a specific dataset if needed:
  # FILTER (?dataset = rdip:ThaiRetinaDataset)
}
ORDER BY ?dataset ?software
```

### Question 2
Which formal methods or protocols were employed in a specific data production activity?

```sparql
SELECT ?activity ?activityTitle ?method ?methodTitle ?methodDesc
WHERE {
  ?activity a rdip:DataProductionActivity ;
            rdip:usedMethod ?method .

  OPTIONAL { ?activity rdip:title       ?activityTitle . }
  OPTIONAL { ?method   rdip:title       ?methodTitle . }
  OPTIONAL { ?method   rdip:description ?methodDesc  . }

  # Restrict to one activity if needed:
  # FILTER (?activity = rdip:CameraTrapAnnotationActivity)
}
ORDER BY ?activity ?method
```

# Question 3
For a given publication, which project produced it and who was the Principal Investigator (PI)?

```sparql
SELECT DISTINCT
  ?article ?articleTitle
  ?project ?projectTitle
  ?pi ?piName
WHERE {
  ?project rdip:hasOutput ?article .
  ?article a bibo:Article .
  OPTIONAL { ?article rdip:title ?articleTitle . }
  OPTIONAL { ?project rdip:title ?projectTitle . }

  ?project  rdip:hasActivity ?activity .
  ?activity rdip:hasActivityRole ?role .

  ?role a rdip:RoleInActivity ;
        rdip:roleLabel       ?roleLabel ;
        rdip:rolePerformedBy ?pi .

  FILTER (REGEX(?roleLabel, "Principal Investigator", "i"))

  OPTIONAL { ?pi rdfs:label ?piName . }
}
ORDER BY ?article ?pi
```

### Question 4
For a given project, which datasets were produced and what are their access levels and landing pages?

```sparql
SELECT ?project ?projectTitle ?dataset ?datasetTitle ?accessLevel ?landingPage
WHERE {
  ?project a rdip:ResearchProject ;
           rdip:hasOutput ?dataset .
  ?dataset a dcat:Dataset .

  OPTIONAL { ?project rdip:title       ?projectTitle . }
  OPTIONAL { ?dataset rdip:title       ?datasetTitle . }
  OPTIONAL { ?dataset rdip:accessLevel ?accessLevel . }
  OPTIONAL { ?dataset rdip:landingPage ?landingPage . }

  # Restrict to a specific project if needed:
  # FILTER (?project = rdip:Project_ThaiMedAI)
}
ORDER BY ?project ?dataset
```

### Question 5
Given a specific output (dataset, software or publication), what other outputs were produced by the same project?

```sparql
SELECT DISTINCT ?givenOutput ?project ?otherOutput ?otherType ?otherTitle
WHERE {
  ?givenOutput rdip:isOutputOf ?project .

  ?project rdip:hasOutput ?otherOutput .
  FILTER (?otherOutput != ?givenOutput)

  OPTIONAL { ?otherOutput a ?otherType . }
  OPTIONAL { ?otherOutput rdip:title ?otherTitle . }

  # Restrict to one given output if needed:
  # FILTER (?givenOutput = rdip:ThaiRetinaDataset)
}
ORDER BY ?givenOutput ?otherOutput
```

### Question 6
What was the specific role of a person in particular data production activities and projects?

```sparql
SELECT ?person ?personName ?activity ?activityTitle ?project ?projectTitle ?roleLabel
WHERE {
  ?activity a rdip:DataProductionActivity ;
            rdip:hasActivityRole ?role ;
            rdip:isPartOfProject ?project .

  ?role rdip:rolePerformedBy ?person ;
        rdip:roleLabel       ?roleLabel .

  OPTIONAL { ?person   rdfs:label ?personName . }
  OPTIONAL { ?activity rdip:title ?activityTitle . }
  OPTIONAL { ?project  rdip:title ?projectTitle . }

  # Restrict to one person if needed:
  # FILTER (?person = rdip:Ms_R_Thanaporn)
}
ORDER BY ?person ?project ?activity
```

### Question 7
For a specific dataset, which activity generated it, using what software, under which project, and who was the agent responsible?

```sparql
SELECT ?datasetTitle ?activityTitle ?softwareName ?softwareVersion ?projectName ?agentName
WHERE {
  # 1. Start with the Dataset
  ?dataset a dcat:Dataset ;
           rdip:title ?datasetTitle ;
           prov:wasGeneratedBy ?activity .

  # 2. Link to Activity and Software
  ?activity a rdip:DataProductionActivity ;
            rdip:title ?activityTitle ;
            rdip:usedSoftware ?software .

  ?software rdip:title ?softwareName .
  OPTIONAL { ?software rdip:version ?softwareVersion . }

  # 3. Link to Project
  ?activity rdip:isPartOfProject ?project .
  ?project  rdip:title ?projectName .

  # 4. Link to Person (Agent) via Role
  ?activity rdip:hasActivityRole ?role .
  ?role     rdip:rolePerformedBy ?agent .
  ?agent    rdfs:label ?agentName .

  # Restrict to a specific dataset context if needed:
  # FILTER (REGEX(?datasetTitle, "Thai Retina", "i"))
}
ORDER BY ?projectName ?datasetTitle
```