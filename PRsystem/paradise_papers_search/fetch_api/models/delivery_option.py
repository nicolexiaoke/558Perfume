from neomodel import (
    StringProperty,
    IntegerProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)

from .nodeutils import NodeUtils


class DeliveryOption(StructuredNode, NodeUtils):
    description = StringProperty()
    node_id     = StringProperty(index = True)

    deliverBy   = RelationshipFrom('.perfume.Perfume', 'deliverBy')
    provideDelivery   = RelationshipFrom('.selling_platform.SellingPlatform', 'provideDelivery')

    # officers    = Relationship('.officer.Officer', None)
    # entities    = Relationship('.entity.Entity', None)

    @property
    def serialize(self):
        return{
            'node_properties': {
                'description': self.description,
                'node_id': self.node_id,
            },
        }


    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.deliverBy.all()),
            },
            {
                'nodes_type': 'SellingPlatform',
                'nodes_related': self.serialize_relationships(self.provideDelivery.all()),
            },
        ]
