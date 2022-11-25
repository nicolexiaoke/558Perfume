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
    has_offline_store = StringProperty()
    
    listedOn  = RelationshipFrom('.perfume.Perfume', 'listedOn')
    

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
    ]
