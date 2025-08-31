import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberSetAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

# Define the brand index
class BrandIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'brand-index'
        projection = AllProjection()
    brand = UnicodeAttribute(hash_key=True)

# Define the main Shoe model
class ShoeModel(Model):
    class Meta:
        table_name = os.environ['SHOES_TABLE_NAME']
        region = os.environ['AWS_REGION'] # Assumes region is in environment

    id = UnicodeAttribute(hash_key=True)
    brand = UnicodeAttribute()
    name = UnicodeAttribute()
    sizes = NumberSetAttribute()
    price = NumberAttribute()

    # Attach the index to the model
    brand_index = BrandIndex()