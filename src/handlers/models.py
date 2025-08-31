import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberSetAttribute, NumberAttribute, ListAttribute, MapAttribute, \
    UTCDateTimeAttribute
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
        region = os.environ.get('AWS_REGION')

    id = UnicodeAttribute(hash_key=True)
    brand = UnicodeAttribute()
    name = UnicodeAttribute()
    sizes = NumberSetAttribute()
    price = NumberAttribute()

    # Attach the index to the model
    brand_index = BrandIndex()

class OrderModel(Model):
    class Meta:
        table_name = os.environ['ORDERS_TABLE_NAME']
        region = os.environ.get('AWS_REGION')
    orderId = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    items = ListAttribute(of=MapAttribute)
    shipping = MapAttribute()
    totalPrice = NumberAttribute()
    createdAt = UTCDateTimeAttribute()