from django.test import TestCase
from elasticsearch import Elasticsearch, helpers


from twitter.documents import StatusDocument
from twitter.models import Status
from .models import Topic

topics = {
    'deforestation': '(native AND vegetation) (deforestation) (forests) (forestry) (tree AND cover) (forest AND cover) (rainforest) (tropical AND forest) (jungle) (afforestation) (reforestation)',
    'certification': '(Signatory) (Consumer AND Goods AND Forum AND Deforestation AND resolution) (CGF) (New AND York AND Declaration AND on AND Forests) (Soy AND Moratorium) (Cerrado AND Manifesto AND Statement AND of AND Support) (G4 AND Cattle AND Agreement) (Tropical AND Forest AND Alliance AND 2020 AND partner) (TFA) (Global AND Agribusiness AND Alliance) (Palm AND Oil AND Innovation AND Group) (World AND Business AND Council AND for AND Sustainable AND Development AND Forest AND Solutions) (WBCSD) (UN AND Global AND Compact) (WWF AND Global AND Forest AND Trade AND Network) (High AND Conservation AND Value AND Resource AND Network)(Natural AND Capital AND Coalition) (Zero-deforestation AND commitment) (Zero-conversion) (RSPO) (RTRS) (FSC) (PEFC) (RA) (Rainforest AND Alliance) (High AND conservation AND value) (HCV) (CDP) (Accountability AND framework AND initiative) (AFI)',
    'monitoring': '(Reporting) (Update) (Progress) (Verify) (verification) (Third-party) (Monitor) (Monitoring) (Achieved) (Achieve) (Failed) (Missed) (Cut-off) (Deforested AND after) (Cleared AND after) (Land AND after) (Converted) (Non-Compliant) (Risk AND assessment) (commodity AND assessment) (Assessment) (Assess AND risks) (Comply AND with AND laws) (Compliance) (Assess) (Monitor) (Audit) (Laws) (Legal) (Legally) (Legislation) (International) (national) (jurisdictional)',
    'nature': '(Forest) (Habitat) (Ecosystem) (Deforestation) (Trees) (Climate AND change) (Biodiversity) (Animals) (Species) (endangered) (Insects) (Nature) (Climate) (Natural AND capital) (GHG AND emissions) (Greenhouse AND gases) (Carbon AND dioxide) (Methane) (Emissions) (Net-Zero)',
    'climate': '(Climate) (Net-zero) (Net AND Zero) (Emissions) (Fossil AND fuels) (Oil) (Gas) (Renewable AND energy) (Hydropower) (Wind AND power) (Solar AND power) (Carbon AND dioxide) (Methane) (GHGs) (GHG AND emissions) (Greenhouse AND gases) (Pollution)',
    'risks': '(Risk) (business AND risk) (Impact) (Threat) (Relies AND on AND nature) (Dependent AND on AND nature) (Reputation) (Reputational AND risk) (Environmental AND social AND impact AND assessment) (Impact AND assessment)',
    'sourcing': '(Sustainable AND procurement) (Sustainability AND Audit) (Sustainability) (Supply AND Chain AND Governance) (Sustainably AND sourced) (Responsibly AND sourced) (Sourcing AND commitment) (Commit AND to AND source) (Traceability) (Trace) (Traceable) (Track) (Point AND of AND production) (To AND the AND mill) (Supply AND Chain) (Map) (Sustainable AND source) (Sourcing) (Natural AND sources) (Product AND source) (Sourcing AND procedure)',
    'protocol': '(Remediation) (Remediate) (Remedial AND action) (Free AND Prior AND Informed AND Consent) (FPIC) (Sourcing AND Region) (Land AND Holding) (Processing AND facility) (Mills) (Refinery) (Supplier AND list) (Suppliers) (Compliance) (Compliant) (Non-compliant) (Code AND of AND Conduct) (Exclude) (Dismiss) (Engage) (Blacklist) (Suppliers) (Exclude) (exclusion) (Corrective AND action AND plan) (Terminate AND of AND contract) (termination AND of AND contract)',
    'landuse': '(GHG AND emissions) (Land AND use AND change) (Land AND use) (Land-use) (Land AND use AND emissions) (Plantation) (Cropland) (Pasture) (Crops) (farmland) (Conservation) (Conservation AND area) (Protected AND area) (Reforest) (Reforestation) (Restore) (Restoration) (Smallholder) (Small-scale AND farmer) (Small AND scale AND farmer) (Local AND producer) (Private AND outgrower AND out AND grower) (Environment AND harm) (Environment AND damage) (Environment AND destroy) (Environment AND disrupt) (Forest) (Savannah) (Grassland) (Biome) (biosphere)',
    'commodities': '(Commodity) (Commodities) (Forest-risk AND commodity) (Forest-risk AND commodities) (Agricultural AND commodity) (Agricultural AND commodities) (Natural AND sources) (Product AND source) (Sourcing AND procedure)',
    'palm': '(High AND carbon AND stock) (HCS) (RSPO) (Roundtable AND on AND sustainable AND palm AND oil) (Roundtable AND for AND sustainable AND palm AND oil) (Peatlands) (Peat) (Palm AND oil) (Oil AND palm) (Plantation)',
    'paper': '(Paper) (Pulp) (Timber) (Wood) (Wood AND products) (Viscose) (Cellulose) (man-made AND cellulosic AND fibres) (MMCF) (Recycled) (Recycled AND content) (Packaging) (Paper AND packaging) (Fibre) (Fiber) (Virgin AND fibre)',
    'beef': '(Beef) (Cows) (Cattle) (Pasture AND land) (Meat) (Slaughterhouse) (Slaughter) (Calf) (Calves) (Leather) (Tanneries)',
    'soy': '(Soy) (Soybeans) (Soya) (Soy AND field) (Soy AND crop) (Cropland)',
    'social': '(Human AND rights) (Labour AND rights) (Labour AND unions) (Labor AND rights) (Labor AND unions) (ILO) (UN AND Global AND Compact) (UNDHR) (Discrimination) (Forced AND labour) (Child AND labour) (Freedom AND of AND association) (Collective AND bargaining) (Ethics) (Code AND of AND conduct) (Supplier AND Policy) (Gender) (Gender AND rights) (LGBQT+) (Smallholder) (Small-scale AND farmer) (Small AND scale AND farmer) (Local AND producer) (Private AND outgrower AND out AND grower) (Grievance AND mechanism) (Grievance AND issue) (Whistleblower AND whistleblowing) (Free AND Prior AND Informed AND Consent) (FPIC)',
    'esg': '(ESG) (Environment) (Social) (Governance) (Green AND bond) (Human AND rights) (Green AND investment) (Supply AND chain AND investment) (Green AND portfolio) (Sustainable AND finance) (Divestment) (Engagement) (Ethical AND investment) (Impact AND investment) (Paris AND Agreement) (Disclosure) (Responsible AND investment) (Socially AND responsible AND investment) (RI) (SRI) (Material AND risk) (Sustainability AND risk) (Reputational AND risk) (Climate AND risk) (Nature AND risk) (Natural AND capital) (Nature-related AND risk) (‘Nature AND and AND finance’) (Nature AND positive) (Nature AND negative) (Biodiversity) (Green AND taxonomy) (Green AND bonds)',
    'agenda': '(COP26) (COP) (Conference AND of AND the AND parties) (CBD15) (Convention AND on AND biological AND diversity) (Kunming) (Glasgow) (Climate AND Week) (ClimateWeekNYC) (NYClimateWeek) (Paris AND Agreement) (Sustainable AND development AND goals) (SDGs) (SDG) (30by30) (Dasgupta AND Review) (Economics AND of AND Biodiversity) (UNFCCC) (HLPF) (GFANZ)',
    'fires': '(Fire) (Fires) (Forest AND Fires) (Wildfires) (Amazon AND Fires) (Cerrado AND Fires) (Pantanal AND Fires) (Chaco AND Fires) (Brazil AND Fires) (Peatland AND fires) (Burning AND peat) (Devastating AND fires) (Borneo AND Fires)',
}

es = Elasticsearch(['localhost:9200/'])

for topic in topics:
    t = Topic(
        name=topic,
        query=topics[topic]
    )
    t.save()

for topic in Topic.objects.all():
    print(topic)
    topics_bulk = []
    topics_bulk_es = {}
    if (topic.name == 'none'):
        continue
    s = StatusDocument.search().query('query_string',default_field='content',query=topic.query).scan()


    for hit in s:
        topics_bulk.append(Topic.status.through(topic_id=topic.name, status_id=hit.id))
        if (hit.id not in topics_bulk_es) :
            topics_bulk_es[hit.id] = []
        topics_bulk_es[hit.id].append(topic.name)
        #topic.status.add(Status.objects.get(pk=hit.id))
    Topic.status.through.objects.bulk_create(topics_bulk,ignore_conflicts=True)
    break


def gendata():
    for id in topics_bulk_es:
        yield {
            '_op_type': 'create',
            "_index": "forest500test",
            "topic_set.name": topics_bulk_es[id],
        }

helpers.bulk(es, gendata())

# s = StatusDocument.search().filter(topic)
# for hit in s:
    
#     #print(f'{topic.name}: {hit.content}')
#     topic.status.add(Status.objects.get(pk=hit.id))

