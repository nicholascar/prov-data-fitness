# prov-data-fitness
This small repo demonstrates provenance queries that could be used to assess the fitness of a dataset for reuse based on
characteristics of that dataset's ancestor datasets and their associated Agents. Assessments are made by analysing
properties of the ancestor datasets or their associated Agents.

The queries are contained within methods starting with 'assess_' within the main.py file. All queries can be run on
example data by running the main.py file.

## Example Data
File *eg1.ttl* contains RDF data in the turtle format, compliant with the [PROV Ontology](https://www.w3.org/TR/prov-o/)
. An image of the data is contained in *eg1.png*. The tests run against *eg1.ttl* all pass or return a result.

File *eg2.ttl* contains data as per the image *eg2.png*. All tests run against *eg2.ttl* fail or return no result.

File *eg3-forward.ttl* contains data as per the image *eg3-forward.png*. This example data is presented to inform 
discussion about 'forward provenance' fitness methodologies but no code implementations are given.

Nicholas Car <nicholas.car@ga.gov.au>