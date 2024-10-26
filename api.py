from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from db import DatabaseHandler
from datetime import datetime

app = FastAPI(title="SciTech API")
db = DatabaseHandler()

class Material(BaseModel):
    id_material: str
    nome: str
    quantidade_disponivel: float
    preco_por_unidade: float

class MaterialQuantidade(BaseModel):
    id_material: str
    quantidade: float

class Encomenda(BaseModel):
    id_encomenda: str
    data_criacao: str
    cliente: Dict
    itens: List[Dict]
    status: str
    valor_total: float
    prazo_entrega: str
    observacoes: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "SciTech API v1.0"}

# Endpoints para Materiais
@app.get("/materiais/", response_model=List[Material])
async def get_materiais():
    return db.get_todos_materiais()

@app.get("/materiais/{id_material}")
async def get_material(id_material: str):
    material = db.get_material(id_material)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material

@app.get("/materiais/quantidade/{id_material}")
async def get_quantidade_material(id_material: str):
    quantidade = db.get_quantidade_material(id_material)
    if quantidade is None:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return {"id_material": id_material, "quantidade": quantidade}

@app.get("/materiais/quantidades/")
async def get_todas_quantidades():
    return db.get_quantidade_todos_materiais()

@app.post("/materiais/ajuste/")
async def ajustar_quantidade_material(material: MaterialQuantidade):
    sucesso = db.ajusta_estoque_material(
        material.id_material, 
        material.quantidade
    )
    if not sucesso:
        raise HTTPException(
            status_code=400, 
            detail="Não foi possível ajustar o estoque"
        )
    return {"message": "Estoque ajustado com sucesso"}

# Endpoints para Encomendas
@app.get("/encomendas/")
async def get_encomendas():
    return db.get_todas_encomendas()

@app.get("/encomendas/{id_encomenda}")
async def get_encomenda(id_encomenda: str):
    encomenda = db.get_encomenda(id_encomenda)
    if not encomenda:
        raise HTTPException(status_code=404, detail="Encomenda não encontrada")
    return encomenda

@app.get("/encomendas/status/{status}")
async def get_encomendas_por_status(status: str):
    return db.get_encomendas_por_status(status)

@app.get("/encomendas/cliente/nome/{nome}")
async def get_encomendas_por_cliente_nome(nome: str):
    return db.get_encomendas_por_cliente_nome(nome)

@app.get("/encomendas/cliente/email/{email}")
async def get_encomendas_por_cliente_email(email: str):
    return db.get_encomendas_por_cliente_email(email)

@app.post("/encomendas/")
async def criar_encomenda(encomenda: Encomenda):
    resultado = db.insere_encomenda(encomenda.dict())
    if not resultado:
        raise HTTPException(
            status_code=400, 
            detail="Não foi possível criar a encomenda"
        )
    return {"message": "Encomenda criada com sucesso"}

@app.put("/encomendas/{id_encomenda}/status/{novo_status}")
async def atualizar_status_encomenda(id_encomenda: str, novo_status: str):
    resultado = db.atualiza_status_encomenda(id_encomenda, novo_status)
    if not resultado:
        raise HTTPException(
            status_code=400, 
            detail="Não foi possível atualizar o status"
        )
    return {"message": "Status atualizado com sucesso"}

# Endpoints para Produção
@app.get("/producao/materiais-necessarios/{id_tipo}/{tamanho}/{quantidade}")
async def calcular_materiais_necessarios(id_tipo: str, tamanho: str, quantidade: int = 1):
    materiais = db.calcula_materiais_necessarios(id_tipo, tamanho, quantidade)
    if not materiais:
        raise HTTPException(
            status_code=404, 
            detail="Tipo de roupa não encontrado"
        )
    return materiais

@app.get("/producao/verificar-disponibilidade/{id_tipo}/{tamanho}/{quantidade}")
async def verificar_disponibilidade(id_tipo: str, tamanho: str, quantidade: int = 1):
    disponibilidade = db.verifica_disponibilidade_producao(id_tipo, tamanho, quantidade)
    if disponibilidade is None:
        raise HTTPException(
            status_code=404, 
            detail="Tipo de roupa não encontrado"
        )
    return disponibilidade

@app.post("/producao/processar/{id_tipo}/{tamanho}/{quantidade}")
async def processar_producao(id_tipo: str, tamanho: str, quantidade: int = 1):
    sucesso = db.processa_producao(id_tipo, tamanho, quantidade)
    if not sucesso:
        raise HTTPException(
            status_code=400, 
            detail="Não foi possível processar a produção"
        )
    return {"message": "Produção processada com sucesso"}
