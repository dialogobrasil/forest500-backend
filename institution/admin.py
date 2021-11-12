from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(Financial)
admin.site.register(Journalist)
admin.site.register(Handle)
admin.site.register(HandleRel)
admin.site.register(CommodityRel)
admin.site.register(SegmentRel)