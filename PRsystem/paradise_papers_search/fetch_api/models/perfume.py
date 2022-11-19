from neomodel import (
    StringProperty,
    ArrayProperty,
    FloatProperty,
    IntegerProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty
)
from django_neomodel import DjangoNode

from .nodeutils import NodeUtils


class Perfume(DjangoNode):
    node_id = StringProperty(index = True)

    name = StringProperty()
    size = StringProperty()
    smell = StringProperty()
    price = FloatProperty()
    rating = FloatProperty()
    url = StringProperty()
    comments = ArrayProperty()

    haveSimilarPrices = RelationshipFrom('.perfume.Perfume', 'haveSimilarPrices')
    haveSimilarPrices = RelationshipTo('.perfume.Perfume', 'haveSimilarPrices')
    sameAs = RelationshipFrom('.perfume.Perfume', 'sameAs')
    sameAs = RelationshipTo('.perfume.Perfume', 'sameAs')
    haveSimilarScents = RelationshipFrom('.perfume.Perfume', 'haveSimilarScents')
    haveSimilarScents = RelationshipTo('.perfume.Perfume', 'haveSimilarScents')


    deliverBy = RelationshipTo('.delivery_option.DeliveryOption', 'deliverBy')
    listedOn = RelationshipTo('.selling_platform.SellingPlatform', 'listedOn')
    productOf = RelationshipTo('.brand.Brand', 'productOf')

    # entities = Relationship('.entity.Entity', None)

    class Meta:
        app_label = "fetch_api"

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.node_id,
                'name': self.name,
                'size': self.size,
                'smell': self.smell,
                'price': self.price,
                'rating': self.rating,
                'comments': self.comments,
                'url' : self.url,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.haveSimilarPrices.all()),
            },
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.haveSimilarPrices.all()),
            },
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.sameAs.all()),
            },
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.sameAs.all()),
            },
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.haveSimilarScents.all()),
            },
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.haveSimilarScents.all()),
            },
            {
                'nodes_type': 'DeliveryOption',
                'nodes_related': self.serialize_relationships(self.deliverBy.all()),
            },
            {
                'nodes_type': 'SellingPlatform',
                'nodes_related': self.serialize_relationships(self.listedOn.all()),
            },
            {
                'nodes_type': 'Brand',
                'nodes_related': self.serialize_relationships(self.productOf.all())
            },
        ]
