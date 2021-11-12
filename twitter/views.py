from typing import final
import numpy as np
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from .serializers import StatusDocumentSerializer
from .documents import StatusDocument
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FacetedSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django.shortcuts import render
from elasticsearch_dsl import (
    DateHistogramFacet,
    RangeFacet,
    TermsFacet,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class LatestStatus(APIView):
    def get(self, request, format=None):
        print(request)
        topic = request.GET.get('topic', None)
        source_panel = request.GET.get('source_panel', None)
        created_at_gt = request.GET.get('created_at_gte', None)
        created_at_lt = request.GET.get('created_at_lte', None)
        
        status = Status.objects.exclude(topic=None).exclude(user_mentions=None)

        if(topic):
            status = status.filter(topic = topic)
        if(list):
            status = status.filter(user__handle__handlerel__list = source_panel)
        if(created_at_gt):
            status = status.filter(created_at__gte = created_at_gt)
        if(created_at_lt):
            status = status.filter(created_at__lte = created_at_lt)

        nodes = {}
        links = {}
        for x in status.iterator():
            source = x.user.screen_name
            nodes[source] = 1 if source not in nodes else nodes[source] + 1
            links[source] = {} if source not in links else links[source]
            links_list = []

            targets =  list(map(lambda x: x['screen_name'],x.user_mentions.values('screen_name')))

            for target in targets:
                nodes[target] = 1 if target not in nodes else nodes[target] + 1

                links[source][target] = 1 if target not in links[source] else links[source][target] + 1


        max_size = max(map(lambda x: nodes[x], nodes))

        nodes = list(map(lambda x: {'id': x, 'name': x, '_size': 1 if ((nodes[x])/max_size)*30 <1 else ((nodes[x])/max_size)*30  }, nodes.keys()))

        index = 0
        has_link = {}
        for source in links:
            has_link[source] = True
            links[source] = dict(sorted(links[source].items(), reverse=True, key=lambda x: x[1])[:10])
            for target in links[source]:
                links_list.append({
                    'id':index,
                    'name':index,
                    'sid': source,
                    'tid': target,
                    '_svgAttrs': {'stroke-width': links[source][target]}
                })
                index +=1
                has_link[target] = True
        
        final_nodes = []
        for x in nodes:
            if(x['id'] in has_link):
                final_nodes.append(x)

        serializer = TestSerializer({'nodes':final_nodes,'links':links_list})
        return Response(serializer.data)


class StatusDocumentView(DocumentViewSet):
    """The Status view."""

    document = StatusDocument
    serializer_class = StatusDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
        FacetedSearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'content',
    )
    # Define filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'created_at': {
            'field': 'created_at',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'list': 'user.handle_set.handlerel_set.list.raw',
        'screen_names': 'user.screen_name.raw',

        'company_commodity': 'user.handle_set.handlerel_set.company.commodityrel_set.commodity.commodity.raw',
        'company_sectors': 'user.handle_set.handlerel_set.company.sectors.text.raw',
        'company_segments': 'user.handle_set.handlerel_set.company.segmentrel_set.segment.text.raw',
        'company_signatories': 'user.handle_set.handlerel_set.company.signatories.name.raw',
        'company_name': 'user.handle_set.handlerel_set.company.name.raw',
        'company_headquarters': 'user.handle_set.handlerel_set.company.headquarters.raw',

        'financial_commodity': 'user.handle_set.handlerel_set.financial.commodityrel_set.commodity.commodity.raw',
        'financial_signatories': 'user.handle_set.handlerel_set.financial.signatories.name.raw',
        'financial_type': 'user.handle_set.handlerel_set.financial.financial_types.type.raw',
        'financial_name': 'user.handle_set.handlerel_set.financial.name.raw',
        'financial_headquarters': 'user.handle_set.handlerel_set.financial.headquarters.raw',

        'journalist_name': 'user.handle_set.handlerel_set.journalist.contact_name.raw',
        'journalist_contact_title': 'user.handle_set.handlerel_set.journalist.contact_title.raw',
        'journalist_contact_country': 'user.handle_set.handlerel_set.journalist.contact_country.raw',
        'journalist_contact_subjects': 'user.handle_set.handlerel_set.journalist.contact_subjects.name.raw',

        'topic': 'topic_set.name.raw'

    }
    # Define filter fields
    faceted_search_fields = {
        'company_commodity': {'field': 'user.handle_set.handlerel_set.company.commodityrel_set.commodity.commodity.raw', 'global': True, 'options': {'size': 100}},
        'company_sectors': {'field': 'user.handle_set.handlerel_set.company.sectors.text.raw', 'global': True, 'options': {'size': 100}},
        'company_segments': {'field': 'user.handle_set.handlerel_set.company.segmentrel_set.segment.text.raw', 'global': True, 'options': {'size': 100}},
        'company_signatories': {'field': 'user.handle_set.handlerel_set.company.signatories.name.raw', 'global': True, 'options': {'size': 100}},
        'company_name': {'field': 'user.handle_set.handlerel_set.company.name.raw', 'global': True, 'options': {'size': 400}},
        'company_headquarters': {'field': 'user.handle_set.handlerel_set.company.headquarters.raw', 'global': True, 'options': {'size': 100}},
        'company_cnt': {'field':'user.handle_set.handlerel_set.company.name.raw', 'global': False, 'options': {'size': 400}},


        'financial_commodity': {'field': 'user.handle_set.handlerel_set.financial.commodityrel_set.commodity.commodity.raw', 'global': True, 'options': {'size': 100}},
        'financial_signatories': {'field': 'user.handle_set.handlerel_set.financial.signatories.name.raw', 'global': True, 'options': {'size': 100}},
        'financial_type': {'field': 'user.handle_set.handlerel_set.financial.financial_types.type.raw', 'global': True, 'options': {'size': 100}},
        'financial_name': {'field': 'user.handle_set.handlerel_set.financial.name.raw', 'global': True, 'options': {'size': 400}},
        'financial_headquarters': {'field': 'user.handle_set.handlerel_set.financial.headquarters.raw', 'global': True, 'options': {'size': 100}},
        'financial_cnt': {'field':'user.handle_set.handlerel_set.financial.name.raw', 'global': False, 'options': {'size': 400}},

        
        'journalist_name': {'field':'user.handle_set.handlerel_set.journalist.contact_name.raw','global': True, 'options': {'size': 400}},
        'journalist_contact_title': {'field':'user.handle_set.handlerel_set.journalist.contact_title.raw','global': True, 'options': {'size': 400}},
        'journalist_contact_country': {'field':'user.handle_set.handlerel_set.journalist.contact_country.raw','global': True, 'options': {'size': 400}},
        'journalist_contact_subjects': {'field':'user.handle_set.handlerel_set.journalist.contact_subjects.name.raw','global': True, 'options': {'size': 400}},
        'journalist_cnt': {'field':'user.handle_set.handlerel_set.financial.name.raw', 'global': False, 'options': {'size': 400}},


        'screen_names': 'user.screen_name.raw',
        'topic_result': {
            'field': 'topic_set.name.raw',
            'options': {
                'size': 100
            }
        },
        'topic_set': {
            'global': True,
            'field': 'topic_set.name.raw',
            'options': {
                'size': 100
            }
        },
        'hashtags': {'field': 'hashtags.text.raw', 'options': {
            'size': 30
        }},
        'videos': {'field': 'videos.video_url.raw', 'options': {
            'size': 12
        }},
        'videos_thumb': {'field': 'videos.media_url.raw', 'options': {
            'size': 12
        }},
        'images': {'field': 'photos.media_url.raw', 'options': {
            'size': 12
        }},
        'user_mentions': {'field': 'user_mentions.screen_name.raw', 'options': {
            'size': 30
        }},
        'urls': {'field': 'urls.expanded_url.raw','options':{
                'size': 30
            }},
        'created_at': {
            'field': 'created_at',
            'facet': DateHistogramFacet,
            'options': {
                'interval': 'day',
            }
        },
        'retweet_count': {
            'field': 'retweet_count',
            'metric': 'max',
        },
    }

    # suggestions
    suggester_fields = {
        'commodities_suggest': {
            'field': 'user.handle_set.company_handles.commodities_powerbroker.commodity.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 20,  # Override default number of suggestions
                # Whether duplicate suggestions should be filtered out.
                'skip_duplicates': True,
            },
        },
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'retweet_count',
    }
    # Specify default ordering
    ordering = ('-id',)

