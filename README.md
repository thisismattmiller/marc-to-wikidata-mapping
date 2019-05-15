# marc-to-wikidata-mapping
Extracts NAF terms from MARC file and maps to Wikidata. This pipeline is designed to build a interfrace based on LC assets, so is not univerisal I'm putting the code up as there might be possible resuses:

`auth.py` - Takes the NAF and LCSH extracts from [id.loc.gov](http://id.loc.gov/download/) and builds a lookup files based on current NAF and LCSH terms currently in Wikidata
`extract.py` - Takes a MARC file and extracts some headings from 100, 700, 600, 610, 611 and maps them to their wikidata ID
`get_visual_wikidata.py` - Downloads data from wikidata from the mapped headings
`build_wikidata_with_labels.py` - Enriches the data with wikidata lables
`desc_and_labels.py` - Enriches the data using text provided in the wiki description
`build_infos.py` - Enriches the data from wikidata
`build_facets.py` - Builds facet data based on the data files

