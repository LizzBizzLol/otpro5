from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom

class Node(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    label = StringProperty(required=True)
    relationships = RelationshipTo("Node", "CONNECTED_TO")

class Relationship(StructuredNode):
    type = StringProperty(required=True)
