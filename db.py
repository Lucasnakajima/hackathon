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
        self.materiais_collection = self.db["materiais"]
        self.tipos_roupa_collection = self.db["tipos_roupa"]
        self.encomendas_collection = self.db["encomendas"]
        
        # Inicializa dados base
        self._inicializar_dados()

    def _inicializar_dados(self):
        """Inicializa os dados base de materiais e tipos de roupa"""
        self._inserir_materiais_base()
        self._inserir_tipos_roupa_base()

    def atualiza_estoque_roupa(self, id_tipo, tamanho, nova_quantidade):
        """
        Atualiza a quantidade em estoque de uma roupa específica em um tamanho específico.
        """
        return self.tipos_roupa_collection.update_one(
            {"id_tipo": id_tipo},
            {"$set": {f"materiais_necessarios.tamanhos.{tamanho}.quantidade_estoque": nova_quantidade}}
        )

    def ajusta_estoque_roupa(self, id_tipo, tamanho, quantidade_ajuste):
        """
        Adiciona ou remove uma quantidade do estoque existente.
        """
        roupa = self.get_tipo_roupa(id_tipo)
        if not roupa:
            return False
            
        estoque_atual = roupa["materiais_necessarios"]["tamanhos"][tamanho]["quantidade_estoque"]
        nova_quantidade = estoque_atual + quantidade_ajuste
        
        if nova_quantidade < 0:
            return False
            
        self.atualiza_estoque_roupa(id_tipo, tamanho, nova_quantidade)
        return True

    def _ajusta_quantidades_por_tamanho(self, quantidade_base, tamanho):
        """Ajusta as quantidades de material baseado no tamanho"""
        razoes = {
            "XS": 0.50,
            "S": 0.75,
            "M": 1.00,
            "L": 1.50,
            "XL": 2.00
        }
        return quantidade_base * razoes[tamanho]

    def _inserir_materiais_base(self):
        """Insere os materiais base no banco de dados"""
        materiais = [
            {
                "id_material": "TECIDO001",
                "nome": "Tecido",
                "quantidade_disponivel": 1000,
                "preco_por_unidade": 7.00
            },
            {
                "id_material": "ALGODAO001",
                "nome": "Algodão",
                "quantidade_disponivel": 800,
                "preco_por_unidade": 5.50
            },
            {
                "id_material": "FIO001",
                "nome": "Fio",
                "quantidade_disponivel": 600,
                "preco_por_unidade": 4.50
            },
            {
                "id_material": "POLIESTER001",
                "nome": "Poliéster",
                "quantidade_disponivel": 400,
                "preco_por_unidade": 10.00
            }
        ]

        for material in materiais:
            self.insere_material(material)

    def _inserir_tipos_roupa_base(self):
        """Insere os tipos de roupa base no banco de dados"""
        tipos_roupa = [
            self._criar_tipo_roupa(
                id_tipo="TSHIRT001",
                nome="T-shirt",
                materiais_base={
                    "tecido": 1.00,
                    "algodao": 0.80,
                    "fio": 0.40,
                    "poliester": 1.30
                },
                tempo_producao=45
            ),
            self._criar_tipo_roupa(
                id_tipo="CALCOES001",
                nome="Calções",
                materiais_base={
                    "tecido": 0.80,
                    "algodao": 0.70,
                    "fio": 0.40,
                    "poliester": 1.40
                },
                tempo_producao=60
            ),
            # ... outros tipos podem ser adicionados aqui
        ]

        for tipo_roupa in tipos_roupa:
            self.insere_tipo_roupa(tipo_roupa)

    def _criar_tipo_roupa(self, id_tipo, nome, materiais_base, tempo_producao):
        """Helper para criar um tipo de roupa com todos os tamanhos"""
        tamanhos = {}
        estoques_iniciais = {"XS": 50, "S": 45, "M": 40, "L": 35, "XL": 30}

        for tamanho in ["XS", "S", "M", "L", "XL"]:
            tamanhos[tamanho] = {
                "quantidade_tecido": self._ajusta_quantidades_por_tamanho(materiais_base["tecido"], tamanho),
                "quantidade_algodao": self._ajusta_quantidades_por_tamanho(materiais_base["algodao"], tamanho),
                "quantidade_fio": self._ajusta_quantidades_por_tamanho(materiais_base["fio"], tamanho),
                "quantidade_poliester": self._ajusta_quantidades_por_tamanho(materiais_base["poliester"], tamanho),
                "quantidade_estoque": estoques_iniciais[tamanho]
            }

        return {
            "id_tipo": id_tipo,
            "nome": nome,
            "materiais_necessarios": {"tamanhos": tamanhos},
            "tempo_producao": tempo_producao
        }

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

    def get_encomendas_por_cliente_nome(self, nome_cliente):
        """
        Retorna todas as encomendas de um cliente específico usando o nome.
        Usa regex para fazer uma busca case-insensitive e parcial.
        
        Parâmetros:
        - nome_cliente: Nome do cliente (parcial ou completo)
        
        Retorna:
        - Lista de encomendas do cliente
        """
        return list(self.encomendas_collection.find({
            "cliente.nome": {
                "$regex": nome_cliente,
                "$options": "i"  # case-insensitive
            }
        }).sort("data_criacao", -1))  # ordenado por data, mais recente primeiro

    def get_encomendas_por_cliente_email(self, email_cliente):
        """
        Retorna todas as encomendas de um cliente específico usando o email.
        
        Parâmetros:
        - email_cliente: Email exato do cliente
        
        Retorna:
        - Lista de encomendas do cliente
        """
        return list(self.encomendas_collection.find({
            "cliente.email": email_cliente.lower()
        }).sort("data_criacao", -1))  # ordenado por data, mais recente primeiro

# Exemplo de uso
if __name__ == "__main__":
    db_handler = DatabaseHandler()

    print(db_handler.get_estoque_por_tamanho("TSHIRT001"))
