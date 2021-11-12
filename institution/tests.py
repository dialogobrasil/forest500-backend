from django.test import TestCase
from numpy import isnan
import pandas as pd
from institution.models import *
from twitter.models import *
import re

sign = ["TNFD IWG","TNFD Observers","Finance for Biodiversity Pledge","Finance @ Biodiversity Community","PBAF","NYDF","CPIC","Natural Capital Declaration (2013)","Business for Nature: Call to Action","UNEPFI","UKSIF","Equator Principles","Capitals Coalition","SBTN","UN PRI","WBCSD","Global Compact","UN Net Zero Asset Owners Alliance","Investors letter to the Brazilian govt (Sept 2019)","Retail soy group letter from business (Amazon fires 2021)"]

companies_df = pd.read_excel('fixtures/institution.xlsx',sheet_name=0)
for index,row in companies_df.iterrows():
    company = Company(
        name = row['k'],
        headquarters = row['Headquarters'],
        region = row['HQ region'],
        ceo_name = row['CEO Name'],
    )
    company.save()

    brands_sheet = row['Brands'].split(', ') if not pd.isna(row['Brands']) else []
    for brand_name in brands_sheet:
        brand = Brand(
            name = brand_name,
            company = company
        )
        brand.save()

    sectors_sheet = row['Company sectors'].split('|')
    for sector_name in sectors_sheet:
        sector = Sector(
            text = sector_name
        )
        sector.save()
        company.sectors.add(sector)

    commodities_sheet = row['Commodities (powerbroker_'].split(', ')
    for commodity_name in commodities_sheet:
        commodity = Commodity(
            commodity = commodity_name,
        )
        commodity.save()

        commodityRel = CommodityRel.objects.update_or_create(
            commodity = commodity,
            company = company,
            type = 'powerbroker',
        )

    commodities_sheet = row['Commodities (Other)'].split(', ') if not pd.isna(row['Commodities (Other)']) else []
    for commodity_name in commodities_sheet:
        commodity = Commodity(
            commodity = commodity_name,
        )
        commodity.save()

        commodityRel = CommodityRel.objects.update_or_create(
            commodity = commodity,
            company = company,
            type = 'other',
        )


    segments_sheet = row['Segments (powerbroker)'].split(', ') if not pd.isna(row['Segments (powerbroker)']) else []
    for segment_name in segments_sheet:
        segment = Segment(
            text = segment_name,
        )
        segment.save()

        segmentRel = SegmentRel.objects.update_or_create(
            segment = segment,
            company = company,
            type = 'powerbroker',
        )

    segments_sheet = row['Segments (Other)'].split(', ') if not pd.isna(row['Segments (Other)']) else []
    for segment_name in segments_sheet:
        segment = Segment(
            text = segment_name,
        )
        segment.save()

        segmentRel = SegmentRel.objects.update_or_create(
            segment = segment,
            company = company,
            type = 'other',
        )


    handles_sheet = re.split(r', ',row['Twitter handle Key: Orange, = no handle found']) if not pd.isna(row['Twitter handle Key: Orange, = no handle found']) else []
    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()

        handleRel = HandleRel.objects.update_or_create(
            handle = handle,
            company = company,
            type = 'default',
            list = 'company'
        )

    handles_sheet = re.split(r', ',row['Alternate handles']) if not pd.isna(row['Alternate handles']) else []
    handles_sheet = [x for x in handles_sheet if not 'http' in x]

    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()

        handleRel = HandleRel.objects.update_or_create(
            handle = handle,
            company = company,
            type = 'alternate',
            list = 'company'           

        )

    handles_sheet = re.split(r', ',row['CEOTwitterhandle']) if not pd.isna(row['CEOTwitterhandle']) else []
    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()

        handleRel = HandleRel.objects.update_or_create(
            handle = handle,
            company = company,
            type = 'ceo',
            list = 'company'
        )
        #company.ceo_handle.add(handle)

    signatories_sheet = re.split(r', ',row['Signatories of which initiatives']) if not pd.isna(row['Signatories of which initiatives']) else []
    signatories_sheet = list(map(lambda x: x.replace('\n',''), signatories_sheet))
    for signatory_name in signatories_sheet:
        signatory = Signatory(
            name = signatory_name
        )
        signatory.save()
        company.signatories.add(signatory)

financial_df = pd.read_excel('fixtures/institution.xlsx',sheet_name=1)
for index,row in financial_df.iterrows():
    if(index == 0):
        continue
    
    financial = Financial(
        name = row[1],
        headquarters = row[3],
        region = row[4],
        ceo_name = row[10],
    )
    financial.save()

    types_sheet = row[5].split(', ') if not pd.isna(row[5]) else []
    for type_name in types_sheet:
        financialType = FinancialType(
            type = type_name
        )
        financialType.save()
        financial.financial_types.add(financialType)

    commodities_sheet = row[6].split(', ') if not pd.isna(row[6]) else []
    for commodity_name in commodities_sheet:
        commodity = Commodity(
            commodity = commodity_name,
        )
        commodity.save()

        CommodityRel.objects.update_or_create(
            commodity = commodity,
            financial = financial,
            type = 'default'
        )

    handles_sheet = row[8].split(', ') if not pd.isna(row[8]) else []
    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()

        HandleRel.objects.update_or_create(
            handle = handle,
            financial = financial,
            type = 'default',
            list = 'financial'
        )

    handles_sheet = row[9].split(', ') if not pd.isna(row[9]) else []
    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()

        HandleRel.objects.update_or_create(
            handle = handle,
            financial = financial,
            type = 'alternate',
            list = 'financial'
        )


    handles_sheet = row[12].split(', ') if not pd.isna(row[12]) else []
    for handle_name in handles_sheet:
        handle = Handle(
            handle = handle_name,
        )
        handle.save()
        
        HandleRel.objects.update_or_create(
            handle = handle,
            financial = financial,
            type = 'ceo',
            list = 'financial'
        )

    for i in range(14,34):
        if(row[i] == True):
            signatory = Signatory(
                name = sign[i-14]
                )
            signatory.save()
            financial.signatories.add(signatory)

journalist_df = pd.read_excel('fixtures/institution.xlsx',sheet_name=2)
for index,row in journalist_df.iterrows():
    handle = Handle(
        handle = row['ContactTwitterUsername']
    )
    handle.save()
    journalist = Journalist(
        contact_name = row['Contact Name'],
        outlet_name = row['Outlet Name'],
        contact_title = row['Contact Title'],
        contact_city = row['Contact Sys. City'],
        contact_country = row['Contact Sys. Country'],
        cision_contact = True if row['GC Cision contact?'] == 'Cision' else False
    )
    journalist.save()

    HandleRel.objects.update_or_create(
        handle=handle,
        journalist=journalist,
        type='default',
        list = 'journalist'
    )

    subjecters_sheet = row['Contact Subjects'].split(', ') if not pd.isna(row['Contact Subjects']) else []
    for subject_name in subjecters_sheet:
        subject = Subject(
            name = subject_name
        )
        subject.save()
        journalist.contact_subjects.add(subject)


for handle in Handle.objects.all():
    print(handle)
    try:
        u = User.objects.get(screen_name__iexact=handle.handle)
        handle.user = u
        handle.save()
    except :
        print(handle,' dontExist')
