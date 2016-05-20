from rdflib import Graph


def assess_license_3_or_4(data_file):
    """
    Determines weather or not a dataset's ancestors all have a CC-BY 3.0 or 4.0 license
    :return: boolean
    """
    g = Graph().parse(data_file, format='turtle')

    return not g.query('''
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX ccby: <https://creativecommons.org/licenses/by/>
        PREFIX : <http://example.org/provenance/one#>
        ASK WHERE {
            :e5 prov:wasDerivedFrom+ ?dataset.
            ?dataset dct:license ?license.
            FILTER (?license != ccby:4.0 && ?license != ccby:3.0).
        }
    ''')


def assess_min_drep_points(data_file, min_points):
    """
    Determines weather or not a dataset's ancestors' attributed Agents all have drep:dataOwnerRepPoints > min_points
    :return: boolean
    """
    g = Graph().parse(data_file, format='turtle')

    return not g.query('''
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX ccby: <https://creativecommons.org/licenses/by/>
        PREFIX drep: <http://promsns.org/ns/drep#>
        PREFIX : <http://example.org/provenance/one#>
        SELECT * WHERE {
            :e5 prov:wasDerivedFrom+ ?dataset.
            ?dataset prov:wasAttributedTo ?agent.
            ?agent drep:dataOwnerRepPoints ?pnts.
            FILTER (?pnts < ''' + str(min_points) + ''').
        }
    ''')


def assess_find_method_code(data_file):
    """
    Finds the code associated with the production of a Dataset by traversing a simple PROV-O data processing model
    :return: string (URL) or None
    """
    g = Graph().parse(data_file, format='turtle')

    for r in g.query('''
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX ccby: <https://creativecommons.org/licenses/by/>
        PREFIX drep: <http://promsns.org/ns/drep#>
        PREFIX : <http://example.org/provenance/one#>
        SELECT ?code_data WHERE {
            :e5 prov:wasGeneratedBy ?a.
            ?a prov:used ?code.
            ?code a prov:Plan;
              dcat:distribution ?d.
            ?d dcat:downloadURL ?code_data
        }
    '''):
        return str(r[0])


# Test all methods
if __name__ == '__main__':
    # True: all the dataset's ancestor datasets have either a CC-BY 3.0 or CC-BY 4.0 license
    print 'eg1 Ancestor licenses CC-BY 3.0 or 4.0: ',
    print assess_license_3_or_4('eg1.ttl')
    # False: one of the all the dataset's ancestor dataset has a CC-B& 2.5 license
    print 'eg2 Ancestor licenses CC-BY 3.0 or 4.0: ',
    print assess_license_3_or_4('eg2.ttl')
    print
    # True: all the dataset's ancestor datasets' attributed Agents have drep:dataOwnerRepPoints > 3
    print 'eg1 Ancestor\'s Agents dataOwnerRepPoints > 3: ',
    print assess_min_drep_points('eg1.ttl', 3)
    # False: not all the dataset's ancestor datasets' attributed Agents have drep:dataOwnerRepPoints > 6
    print 'eg1 Ancestor\'s Agents dataOwnerRepPoints > 6: ',
    print assess_min_drep_points('eg2.ttl', 6)
    print
    # URL of method code returned
    print 'eg1 dataset\'s method code: ',
    print assess_find_method_code('eg1.ttl')
    # URL of method code not returned
    print 'eg2 dataset\'s method code: ',
    print assess_find_method_code('eg2.ttl')
    print


