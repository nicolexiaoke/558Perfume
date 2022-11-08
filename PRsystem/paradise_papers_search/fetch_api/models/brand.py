from neomodel import (
    StringProperty,
    IntegerProperty,
    StructuredNode,
    RelationshipFrom,
    Relationship
)

from .nodeutils import NodeUtils


class Brand(StructuredNode, NodeUtils):
    name          = StringProperty()
    node_id       = StringProperty(index = True)
    
    productOf     = RelationshipFrom('.perfume.Perfume', 'productOf')


    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                'node_id': self.node_id,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Perfume',
                'nodes_related': self.serialize_relationships(self.productOf.all()),
            },
        ]
