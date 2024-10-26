from pymongo import MongoClient

class DatabaseHandler:
    def __init__(self, db_name="scitech"):
        # Configuração da conexão
        usuario = "root"
        senha = "root"
        self.client = MongoClient(
            f"mongodb://{usuario}:{senha}@localhost:27017/?authMechanism=DEFAULT&authSource=admin"
        )
        self.db = self.client[db_name]
        
        # Coleções
        self.materiais_collection = self.db["materiais"]  # Renomeado de tecidos para materiais
        self.tipos_roupa_collection = self.db["tipos_roupa"]
        self.encomendas_collection = self.db["encomendas"]

    # Funções para Materiais (renomeadas de Tecidos)
    def insere_material(self, material):
        """
        Insere ou atualiza um material.
        Se já existir um material com o mesmo id_material, atualiza os dados.
        Se não existir, insere um novo.
        
        {
            "id_material": str,
            "nome": str,
            "quantidade_disponivel": float,
            "preco_por_unidade": float
        }
        """
        return self.materiais_collection.update_one(
            {"id_material": material["id_material"]},
            {"$set": material},
            upsert=True
        )

    def atualiza_material(self, id_material, atualizacao):
        """Atualiza informações de um material específico"""
        return self.materiais_collection.update_one(
            {"id_material": id_material},
            {"$set": atualizacao}
        )

    def get_material(self, id_material):
        """Busca um material específico"""
        return self.materiais_collection.find_one({"id_material": id_material})

    def get_todos_materiais(self):
        """Retorna todos os materiais"""
        return list(self.materiais_collection.find())

    # Funções para Tipos de Roupa
    def insere_tipo_roupa(self, tipo_roupa):
        """
        Insere ou atualiza um tipo de roupa.
        Se já existir um tipo com o mesmo id_tipo, atualiza os dados.
        Se não existir, insere um novo.
        """
        return self.tipos_roupa_collection.update_one(
            {"id_tipo": tipo_roupa["id_tipo"]},
            {"$set": tipo_roupa},
            upsert=True
        )

    def atualiza_tipo_roupa(self, id_tipo, atualizacao):
        """Atualiza informações de um tipo de roupa"""
        return self.tipos_roupa_collection.update_one(
            {"id_tipo": id_tipo},
            {"$set": atualizacao}
        )

    def get_tipo_roupa(self, id_tipo):
        """Busca um tipo de roupa específico"""
        return self.tipos_roupa_collection.find_one({"id_tipo": id_tipo})

    def get_todos_tipos_roupa(self):
        """Retorna todos os tipos de roupa"""
        return list(self.tipos_roupa_collection.find())

    # Funções para Encomendas
    def insere_encomenda(self, encomenda):
        """
        Insere ou atualiza uma encomenda.
        Se já existir uma encomenda com o mesmo id_encomenda, atualiza os dados.
        Se não existir, insere uma nova.
        """
        return self.encomendas_collection.update_one(
            {"id_encomenda": encomenda["id_encomenda"]},
            {"$set": encomenda},
            upsert=True
        )

    def atualiza_status_encomenda(self, id_encomenda, novo_status):
        """Atualiza o status de uma encomenda"""
        return self.encomendas_collection.update_one(
            {"id_encomenda": id_encomenda},
            {"$set": {"status": novo_status}}
        )

    def get_encomenda(self, id_encomenda):
        """Busca uma encomenda específica"""
        return self.encomendas_collection.find_one({"id_encomenda": id_encomenda})

    def get_encomendas_por_status(self, status):
        """Retorna todas as encomendas com um determinado status"""
        return list(self.encomendas_collection.find({"status": status}))

    def get_todas_encomendas(self):
        """Retorna todas as encomendas"""
        return list(self.encomendas_collection.find())

    def get_estoque_total_todos_tipos(self):
        """
        Retorna o estoque total de todas as roupas, somando todos os tamanhos.
        
        Retorna:
        - Dict com id_tipo e quantidade total
        Exemplo: {
            "TSHIRT001": 200,
            "CALCAS001": 150,
            ...
        }
        """
        todos_tipos = self.get_todos_tipos_roupa()
        estoque_total = {}
        
        for tipo in todos_tipos:
            total = sum(
                tamanho_info["quantidade_estoque"] 
                for tamanho_info in tipo["materiais_necessarios"]["tamanhos"].values()
            )
            estoque_total[tipo["id_tipo"]] = total
            
        return estoque_total

    def get_estoque_por_tamanho(self, id_tipo):
        """
        Retorna as quantidades em estoque para cada tamanho de um tipo específico de roupa.
        
        Parâmetros:
        - id_tipo: ID do tipo de roupa (ex: "TSHIRT001")
        
        Retorna:
        - Dict com tamanhos e suas quantidades
        Exemplo: {
            "XS": 50,
            "S": 45,
            "M": 40,
            "L": 35,
            "XL": 30
        }
        """
        tipo_roupa = self.get_tipo_roupa(id_tipo)
        if not tipo_roupa:
            return None
            
        return {
            tamanho: info["quantidade_estoque"]
            for tamanho, info in tipo_roupa["materiais_necessarios"]["tamanhos"].items()
        }

    def close_connection(self):
        self.client.close()

def ajusta_quantidades_por_tamanho(quantidade_base, tamanho):
    razoes = {
        "XS": 0.50,
        "S": 0.75,
        "M": 1.00,
        "L": 1.50,
        "XL": 2.00
    }
    return quantidade_base * razoes[tamanho]

# Exemplo de uso
if __name__ == "__main__":
    db_handler = DatabaseHandler()

    def atualiza_estoque_roupa(self, id_tipo, tamanho, nova_quantidade):
        """
        Atualiza a quantidade em estoque de uma roupa específica em um tamanho específico.
        
        Parâmetros:
        - id_tipo: ID do tipo de roupa (ex: "TSHIRT001")
        - tamanho: Tamanho da roupa (ex: "XS", "S", "M", "L", "XL")
        - nova_quantidade: Nova quantidade em estoque
        
        Retorna:
        - Resultado da operação de update
        """
        return self.tipos_roupa_collection.update_one(
            {"id_tipo": id_tipo},
            {"$set": {f"materiais_necessarios.tamanhos.{tamanho}.quantidade_estoque": nova_quantidade}}
        )

    def ajusta_estoque_roupa(self, id_tipo, tamanho, quantidade_ajuste):
        """
        Adiciona ou remove uma quantidade do estoque existente.
        Use quantidade positiva para adicionar e negativa para remover.
        
        Parâmetros:
        - id_tipo: ID do tipo de roupa (ex: "TSHIRT001")
        - tamanho: Tamanho da roupa (ex: "XS", "S", "M", "L", "XL")
        - quantidade_ajuste: Quantidade a ser adicionada (positivo) ou removida (negativo)
        
        Retorna:
        - True se operação foi bem sucedida
        - False se não houver estoque suficiente para remoção
        """
        # Primeiro, obtém a quantidade atual
        roupa = self.get_tipo_roupa(id_tipo)
        if not roupa:
            return False
            
        estoque_atual = roupa["materiais_necessarios"]["tamanhos"][tamanho]["quantidade_estoque"]
        nova_quantidade = estoque_atual + quantidade_ajuste
        
        # Verifica se há estoque suficiente em caso de remoção
        if nova_quantidade < 0:
            return False
            
        # Atualiza com a nova quantidade
        self.atualiza_estoque_roupa(id_tipo, tamanho, nova_quantidade)
        return True

    # Exemplo de inserção de materiais
    materiais = [
        {
            "id_material": "TECIDO001",
            "nome": "Tecido",
            "quantidade_disponivel": 1000,  # metros quadrados
            "preco_por_unidade": 7.00  # €/m²
        },
        {
            "id_material": "ALGODAO001",
            "nome": "Algodão",
            "quantidade_disponivel": 800,  # metros cúbicos
            "preco_por_unidade": 5.50  # €/m³
        },
        {
            "id_material": "FIO001",
            "nome": "Fio",
            "quantidade_disponivel": 600,  # metros
            "preco_por_unidade": 4.50  # €/m
        },
        {
            "id_material": "POLIESTER001",
            "nome": "Poliéster",
            "quantidade_disponivel": 400,  # metros quadrados
            "preco_por_unidade": 10.00  # €/m²
        }
    ]

    # Inserindo os materiais
    for material in materiais:
        db_handler.insere_material(material)

    # Exemplos de inserção de tipos de roupa com estoque por tamanho
    tipos_roupa = [
        {
            "id_tipo": "TSHIRT001",
            "nome": "T-shirt",
            "materiais_necessarios": {
                "tamanhos": {
                    "XS": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.00, "XS"),  # 0.50
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.80, "XS"),  # 0.40
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "XS"),  # 0.20
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.30, "XS"),  # 0.65
                        "quantidade_estoque": 50
                    },
                    "S": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.00, "S"),  # 0.75
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.80, "S"),  # 0.60
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "S"),  # 0.30
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.30, "S"),  # 0.98
                        "quantidade_estoque": 45
                    },
                    "M": {
                        "quantidade_tecido": 1.00,  # valor base mantido
                        "quantidade_algodao": 0.80,
                        "quantidade_fio": 0.40,
                        "quantidade_poliester": 1.30,
                        "quantidade_estoque": 40
                    },
                    "L": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.00, "L"),  # 1.50
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.80, "L"),  # 1.20
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "L"),  # 0.60
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.30, "L"),  # 1.95
                        "quantidade_estoque": 35
                    },
                    "XL": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.00, "XL"),  # 2.00
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.80, "XL"),  # 1.60
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "XL"),  # 0.80
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.30, "XL"),  # 2.60
                        "quantidade_estoque": 30
                    }
                }
            },
            "tempo_producao": 45
        },
        {
            "id_tipo": "CALCOES001",
            "nome": "Calções",
            "materiais_necessarios": {
                "tamanhos": {
                    "XS": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.80, "XS"),  # 0.40
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.70, "XS"),  # 0.35
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "XS"),  # 0.20
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.40, "XS"),  # 0.70
                        "quantidade_estoque": 50
                    },
                    "S": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.80, "S"),  # 0.60
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.70, "S"),  # 0.53
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "S"),  # 0.30
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.40, "S"),  # 1.05
                        "quantidade_estoque": 45
                    },
                    "M": {
                        "quantidade_tecido": 0.80,  # valor base mantido
                        "quantidade_algodao": 0.70,
                        "quantidade_fio": 0.40,
                        "quantidade_poliester": 1.40,
                        "quantidade_estoque": 40
                    },
                    "L": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.80, "L"),  # 1.20
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.70, "L"),  # 1.05
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "L"),  # 0.60
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.40, "L"),  # 2.10
                        "quantidade_estoque": 35
                    },
                    "XL": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.80, "XL"),  # 1.60
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.70, "XL"),  # 1.40
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.40, "XL"),  # 0.80
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.40, "XL"),  # 2.80
                        "quantidade_estoque": 30
                    }
                }
            },
            "tempo_producao": 60
        },
        {
            "id_tipo": "CAMISOLA001",
            "nome": "Camisola",
            "materiais_necessarios": {
                "tamanhos": {
                    "XS": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.50, "XS"),  # 0.25
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.35, "XS"),  # 0.18
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.50, "XS"),  # 0.25
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.15, "XS"),  # 0.58
                        "quantidade_estoque": 50
                    },
                    "S": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.50, "S"),  # 0.38
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.35, "S"),  # 0.26
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.50, "S"),  # 0.38
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.15, "S"),  # 0.86
                        "quantidade_estoque": 45
                    },
                    "M": {
                        "quantidade_tecido": 0.50,  # valor base mantido
                        "quantidade_algodao": 0.35,
                        "quantidade_fio": 0.50,
                        "quantidade_poliester": 1.15,
                        "quantidade_estoque": 40
                    },
                    "L": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.50, "L"),  # 0.75
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.35, "L"),  # 0.53
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.50, "L"),  # 0.75
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.15, "L"),  # 1.73
                        "quantidade_estoque": 35
                    },
                    "XL": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(0.50, "XL"),  # 1.00
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.35, "XL"),  # 0.70
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.50, "XL"),  # 1.00
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.15, "XL"),  # 2.30
                        "quantidade_estoque": 30
                    }
                }
            },
            "tempo_producao": 30
        },
        {
            "id_tipo": "CALCAS001",
            "nome": "Calças",
            "materiais_necessarios": {
                "tamanhos": {
                    "XS": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.20, "XS"),  # 0.60
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.95, "XS"),  # 0.48
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.35, "XS"),  # 0.18
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.50, "XS"),  # 0.75
                        "quantidade_estoque": 50
                    },
                    "S": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.20, "S"),  # 0.90
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.95, "S"),  # 0.71
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.35, "S"),  # 0.26
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.50, "S"),  # 1.13
                        "quantidade_estoque": 45
                    },
                    "M": {
                        "quantidade_tecido": 1.20,  # valor base mantido
                        "quantidade_algodao": 0.95,
                        "quantidade_fio": 0.35,
                        "quantidade_poliester": 1.50,
                        "quantidade_estoque": 40
                    },
                    "L": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.20, "L"),  # 1.80
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.95, "L"),  # 1.43
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.35, "L"),  # 0.53
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.50, "L"),  # 2.25
                        "quantidade_estoque": 35
                    },
                    "XL": {
                        "quantidade_tecido": ajusta_quantidades_por_tamanho(1.20, "XL"),  # 2.40
                        "quantidade_algodao": ajusta_quantidades_por_tamanho(0.95, "XL"),  # 1.90
                        "quantidade_fio": ajusta_quantidades_por_tamanho(0.35, "XL"),  # 0.70
                        "quantidade_poliester": ajusta_quantidades_por_tamanho(1.50, "XL"),  # 3.00
                        "quantidade_estoque": 30
                    }
                }
            },
            "tempo_producao": 75
        }
    ]
    
    # Inserindo os tipos de roupa
    for tipo_roupa in tipos_roupa:
        db_handler.insere_tipo_roupa(tipo_roupa)


