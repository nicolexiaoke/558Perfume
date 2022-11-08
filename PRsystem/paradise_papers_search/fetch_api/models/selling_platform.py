from neomodel import (
    StringProperty,
    IntegerProperty,
    StructuredNode,
    RelationshipFrom,
    RelationshipTo
)

from .nodeutils import NodeUtils

class SellingPlatform(StructuredNode, NodeUtils):
    name      = StringProperty()
    node_id       = StringProperty(index = True)
    
    listedOn  = RelationshipFrom('.perfume.Perfume', 'listedOn')
    provideDelivery = RelationshipTo('.delivery_option.DeliveryOption', 'provideDelivery')
    

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                'node_id': self.node_id,
            },
        }

    '''------------------------------------------------------------------------------------------------'''
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.listedOn.all()),
            },
            {
                'nodes_type': 'DeliveryOption',
                'nodes_related': self.serialize_relationships(self.provideDelivery.all()),
            },
    ]
