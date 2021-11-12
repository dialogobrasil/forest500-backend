from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry

from twitter.models import *

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


def text_suggest():
    return fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            #'suggest': fields.CompletionField(),
        }
    )


@registry.register_document
class StatusDocument(Document):
    class Index:
        name = 'forest500test'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    topic_set = fields.ObjectField(properties={
        'name': text_suggest(),
    })

    user = fields.ObjectField(
        properties={
            'screen_name': text_suggest(),
            'profile_image_url': fields.TextField(),
            'name': text_suggest(),
            'id' : text_suggest(),
            'handle_set': fields.ObjectField(
                properties={
                    'handlerel_set': fields.ObjectField(
                        properties={
                            'type': text_suggest(),
                            'list': text_suggest(),
                            'company': fields.ObjectField(
                                properties={
                                    "name": text_suggest(),
                                    "headquarters": text_suggest(),
                                    "sectors": fields.ObjectField(
                                        properties={
                                            'text': text_suggest()
                                        }
                                    ),
                                    "commodityrel_set": fields.ObjectField(
                                        properties={
                                            'type': text_suggest(),
                                            'commodity': fields.ObjectField(properties={
                                                'commodity': text_suggest()
                                            })
                                        }
                                    ),
                                    "segmentrel_set": fields.ObjectField(
                                        properties={
                                            'type': text_suggest(),
                                            'segment': fields.ObjectField(properties={
                                                'text': text_suggest()
                                            })
                                        }
                                    ),
                                    "signatories": fields.ObjectField(
                                        properties={
                                            'name': text_suggest()
                                        }
                                    ),
                                }
                            ),
                            'financial': fields.ObjectField(
                                properties={
                                    "name": text_suggest(),
                                    "headquarters": text_suggest(),
                                    "financial_types": fields.ObjectField(properties={
                                        'type': text_suggest(),
                                    }),
                                    "commodityrel_set": fields.ObjectField(
                                        properties={
                                            'type': text_suggest(),
                                            'commodity': fields.ObjectField(properties={
                                                'commodity': text_suggest()
                                            })
                                        }
                                    ),
                                    "signatories": fields.ObjectField(
                                        properties={
                                            'name': text_suggest()
                                        }
                                    ),
                                }
                            ),
                            'journalist': fields.ObjectField(
                                properties={
                                    "contact_name": text_suggest(),
                                    "contact_title": text_suggest(),
                                    "contact_country": text_suggest(),
                                    "contact_subjects": fields.ObjectField(
                                        properties={
                                            'name': text_suggest(),
                                        }
                                    ),
                                }
                            ),
                        }
                    )
                }
            )
        }
    )

    hashtags = fields.ObjectField(
        properties={
            'text': text_suggest(),
        }
    )

    user_mentions = fields.ObjectField(
        properties={
            'screen_name': text_suggest(),
        }
    )

    content = text_suggest()

    id = text_suggest()

    photos = fields.ObjectField(
        properties={
            'media_url': text_suggest(),
            'url': fields.ObjectField(
                properties={
                    'url': fields.TextField(),
                }
            ),
        }
    )

    videos = fields.ObjectField(
        properties={
            'media_url': text_suggest(),
            'url': fields.ObjectField(
                properties={
                    'url': fields.TextField(),
                }
            ),
            'video_url': text_suggest(),
        }
    )

    urls = fields.ObjectField(
        properties={
            'url': text_suggest(),
            'expanded_url': text_suggest(),
        }
    )

    created_at = fields.DateField()

    class Django:
        model = Status
        fields = [
            'retweet_count',
            'favorite_count',
        ]

