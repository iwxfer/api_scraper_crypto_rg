from django.db import models
from datetime import datetime
from django.utils.timezone import now

def isotime(time):
    if time:
        return time.isoformat()
    return ''
        

class Scraper(models.Model):
    created_at = models.DateTimeField(default=now)
    currency = models.CharField(max_length=20, unique=True)
    frequency = models.IntegerField()
    value = models.FloatField(null=True, blank=True)
    value_updated_at = models.DateTimeField(default=now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "created_at": isotime(self.created_at),
            "currency": self.currency,
            "frequency": self.frequency,
            "value": self.value,
            "value_updated_at": isotime(self.value_updated_at)
        }
    
    @classmethod
    def to_list(cls, items):
        items_list = []
        for i in items:
            items_list.append(i.to_dict())
        
        return items_list
