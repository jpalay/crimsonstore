from django.db import models


#
import re

from django.db.models import Q
#
# Create your models here.

	
class Catalog(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=150)
  publisher = models.CharField(max_length=300)
  description = models.TextField()
  def __unicode__(self):
    return u'%s' % (self.name)

class Product(models.Model):
  category = models.ForeignKey('ProductCategory',
                            related_name='products')
  name = models.CharField(max_length=300)
  slug = models.SlugField(max_length=150)
  description = models.TextField()
  photo = models.ImageField(upload_to='product_photos/')
  manufacturer = models.CharField(max_length=300,
                                           blank=True)
  price_in_dollars = models.DecimalField(max_digits=6,
                                      decimal_places=2)
  def __unicode__(self):
    return u'%s' % (self.name)

class ProductCategory(models.Model):
  catalog = models.ForeignKey('Catalog',
                             related_name='product_categories')
  parent = models.ForeignKey('self', blank=True, null=True,
                             related_name='children')
  name = models.CharField(max_length=300)
  slug = models.SlugField(max_length=150)
  description = models.TextField(blank=True)
  def __unicode__(self):
    if self.parent:
      return u'%s: %s - %s' % (self.catalog.name,
                               self.parent.name,
                               self.name)
    return u'%s: %s' % (self.catalog.name, self.name)


class EventCategory(models.Model):
  catalog = models.ForeignKey('Catalog',
                             related_name='event_categories')
  name = models.CharField(max_length=300)
  slug = models.SlugField(max_length=150) 
  description = models.TextField() 
  def __unicode__(self):
    return u'%s' % (self.name)

class Event(models.Model):
  name = models.CharField(max_length=300)
  slug = models.SlugField(max_length=150)
  date = models.DateField()
  price_in_dollars = models.DecimalField(max_digits=6,
                                      decimal_places=2)
  category = models.ForeignKey('EventCategory',
                           related_name='events')
  description = models.TextField()
  photographer = models.CharField(max_length=300)
  def __unicode__(self):
    return u'%s' % (self.name)

class Photo(models.Model):
  event = models.ForeignKey('Event',
                           related_name='photos')
  photo = models.ImageField(upload_to='product_photos/')



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
