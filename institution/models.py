from django.db import models
from django.db.models.fields.related import ManyToManyField
from twitter.models import *

class Brand(models.Model):
    name = models.TextField(primary_key=True)
    company = models.ForeignKey('Company',on_delete=models.PROTECT)

class Sector(models.Model):
    text = models.TextField(primary_key=True)

class Handle(models.Model):
    handle = models.TextField(primary_key=True)
    id = models.TextField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True)

class Signatory(models.Model):
    name = models.TextField(primary_key=True)

class Segment(models.Model):
    text = models.TextField(primary_key=True)

class Commodity(models.Model):
    commodity = models.TextField(primary_key=True)

class Company(models.Model):
    name = models.TextField(primary_key=True)
    sectors = models.ManyToManyField(Sector)
    headquarters = models.TextField()
    region = models.TextField()
    commodities = models.ManyToManyField(Commodity,through='CommodityRel')
    segments = models.ManyToManyField(Segment,through='SegmentRel')
    handles = models.ManyToManyField(Handle,through='HandleRel')
    ceo_name = models.TextField()
    signatories = models.ManyToManyField(Signatory)

class FinancialType(models.Model):
    type = models.TextField(primary_key=True)

class Financial(models.Model):
    name = models.TextField(primary_key=True)
    headquarters = models.TextField()
    region = models.TextField()
    financial_types = models.ManyToManyField(FinancialType)
    commodities = models.ManyToManyField(Commodity,through='CommodityRel')
    handles = models.ManyToManyField(Handle,through='HandleRel')
    ceo_name = models.TextField()
    signatories = models.ManyToManyField(Signatory)

class Subject(models.Model):
    name = models.TextField(primary_key=True)

class Journalist(models.Model):
    contact_name = models.TextField(primary_key=True)
    outlet_name = models.TextField()
    contact_title = models.TextField()
    handle = models.ManyToManyField(Handle,through='HandleRel')
    contact_subjects = models.ManyToManyField(Subject)
    contact_city = models.TextField()
    contact_country = models.TextField()
    cision_contact = models.BooleanField()

class SegmentRel(models.Model):
    segment = models.ForeignKey(Segment,on_delete=models.PROTECT)
    company = models.ForeignKey(Company,on_delete=models.PROTECT)
    type = models.TextField()

class CommodityRel(models.Model):
    commodity = models.ForeignKey(Commodity,on_delete=models.PROTECT)
    company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.PROTECT)
    financial = models.ForeignKey(Financial,blank=True,null=True,on_delete=models.PROTECT)
    type = models.TextField()

class HandleRel(models.Model):
    handle = models.ForeignKey(Handle,on_delete=models.PROTECT)
    company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.PROTECT)
    financial = models.ForeignKey(Financial,blank=True,null=True,on_delete=models.PROTECT)
    journalist = models.ForeignKey(Journalist,blank=True,null=True,on_delete=models.PROTECT)
    type = models.TextField()
    list = models.TextField(blank=True,null=True)
