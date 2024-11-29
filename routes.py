from fastapi import APIRouter, HTTPException, Depends
from models import Node
from auth import get_current_user

router = APIRouter()

# GET всех узлов
@router.get("/nodes")
async def get_all_nodes():
    nodes = Node.nodes.all()
    return [{"id": node.id, "label": node.label} for node in nodes]

# GET узла и всех его связей
@router.get("/nodes/{node_id}")
async def get_node_and_relationships(node_id: str):
    node = Node.nodes.get_or_none(id=node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {
        "id": node.id,
        "label": node.label,
        "relationships": [{"target_id": rel.id, "target_label": rel.label} for rel in node.relationships]
    }

# POST добавление узла/связей
@router.post("/nodes", dependencies=[Depends(get_current_user)])
async def add_node_and_relationships(node_data: dict):
    node = Node(id=node_data["id"], label=node_data["label"]).save()
    # Добавить связи, если есть
    for rel in node_data.get("relationships", []):
        target_node = Node.nodes.get_or_none(id=rel["target_id"])
        if target_node:
            node.relationships.connect(target_node)
    return {"message": "Node and relationships added successfully"}

# DELETE узла/связей
@router.delete("/nodes/{node_id}", dependencies=[Depends(get_current_user)])
async def delete_node_and_relationships(node_id: str):
    node = Node.nodes.get_or_none(id=node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    node.delete()
    return {"message": "Node and relationships deleted successfully"}
