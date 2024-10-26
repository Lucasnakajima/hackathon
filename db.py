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
                "quantidade_disponivel": 2200,
                "preco_por_unidade": 7.00
            },
            {
                "id_material": "ALGODAO001",
                "nome": "Algodão",
                "quantidade_disponivel": 2200,
                "preco_por_unidade": 5.50
            },
            {
                "id_material": "FIO001",
                "nome": "Fio",
                "quantidade_disponivel": 2200,
                "preco_por_unidade": 4.50
            },
            {
                "id_material": "POLIESTER001",
                "nome": "Poliéster",
                "quantidade_disponivel": 2200,
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
        
        for tamanho in ["XS", "S", "M", "L", "XL"]:
            tamanhos[tamanho] = {
                "quantidade_tecido": self._ajusta_quantidades_por_tamanho(materiais_base["tecido"], tamanho),
                "quantidade_algodao": self._ajusta_quantidades_por_tamanho(materiais_base["algodao"], tamanho),
                "quantidade_fio": self._ajusta_quantidades_por_tamanho(materiais_base["fio"], tamanho),
                "quantidade_poliester": self._ajusta_quantidades_por_tamanho(materiais_base["poliester"], tamanho)
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

    def verifica_disponibilidade_material(self, id_material, quantidade_necessaria):
        """
        Verifica se há quantidade suficiente de um material disponível
        
        Retorna:
        - True se houver material suficiente
        - False se não houver
        """
        material = self.get_material(id_material)
        if not material:
            return False
        return material["quantidade_disponivel"] >= quantidade_necessaria

    def ajusta_estoque_material(self, id_material, quantidade_ajuste):
        """
        Adiciona ou remove uma quantidade do estoque de material.
        Use quantidade positiva para adicionar e negativa para remover.
        
        Retorna:
        - True se operação foi bem sucedida
        - False se não houver estoque suficiente para remoção
        """
        material = self.get_material(id_material)
        if not material:
            return False
            
        nova_quantidade = material["quantidade_disponivel"] + quantidade_ajuste
        
        if nova_quantidade < 0:
            return False
            
        self.atualiza_material(id_material, {"quantidade_disponivel": nova_quantidade})
        return True

    def calcula_materiais_necessarios(self, id_tipo, tamanho, quantidade=1):
        """
        Calcula a quantidade de materiais necessários para produzir uma quantidade
        específica de um tipo de roupa em um tamanho específico.
        
        Retorna:
        - Dict com as quantidades necessárias de cada material
        - None se o tipo de roupa não existir
        """
        tipo_roupa = self.get_tipo_roupa(id_tipo)
        if not tipo_roupa:
            return None
            
        materiais_tamanho = tipo_roupa["materiais_necessarios"]["tamanhos"][tamanho]
        return {
            "TECIDO001": materiais_tamanho["quantidade_tecido"] * quantidade,
            "ALGODAO001": materiais_tamanho["quantidade_algodao"] * quantidade,
            "FIO001": materiais_tamanho["quantidade_fio"] * quantidade,
            "POLIESTER001": materiais_tamanho["quantidade_poliester"] * quantidade
        }

    def verifica_disponibilidade_producao(self, id_tipo, tamanho, quantidade=1):
        """
        Verifica se há materiais suficientes para produzir uma quantidade
        específica de um tipo de roupa.
        
        Retorna:
        - Dict com status de disponibilidade de cada material
        - None se o tipo de roupa não existir
        """
        materiais_necessarios = self.calcula_materiais_necessarios(id_tipo, tamanho, quantidade)
        if not materiais_necessarios:
            return None
            
        disponibilidade = {}
        for id_material, qtd_necessaria in materiais_necessarios.items():
            disponibilidade[id_material] = self.verifica_disponibilidade_material(
                id_material, 
                qtd_necessaria
            )
            
        return disponibilidade

    def processa_producao(self, id_tipo, tamanho, quantidade=1):
        """
        Processa a produção de uma roupa, consumindo os materiais necessários.
        
        Retorna:
        - True se a produção foi bem sucedida
        - False se não há materiais suficientes
        """
        # Verifica disponibilidade
        disponibilidade = self.verifica_disponibilidade_producao(id_tipo, tamanho, quantidade)
        if not disponibilidade or False in disponibilidade.values():
            return False
            
        # Calcula materiais necessários
        materiais_necessarios = self.calcula_materiais_necessarios(id_tipo, tamanho, quantidade)
        
        # Consome os materiais
        for id_material, qtd_necessaria in materiais_necessarios.items():
            if not self.ajusta_estoque_material(id_material, -qtd_necessaria):
                return False
                
        return True

    def get_quantidade_material(self, id_material):
        """
        Retorna a quantidade disponível de um material específico.
        
        Parâmetros:
        - id_material: ID do material (ex: "TECIDO001")
        
        Retorna:
        - float: quantidade disponível do material
        - None: se o material não for encontrado
        """
        material = self.get_material(id_material)
        if not material:
            return None
        return material["quantidade_disponivel"]

    def get_quantidade_todos_materiais(self):
        """
        Retorna as quantidades disponíveis de todos os materiais.
        
        Retorna:
        - Dict com id_material e quantidade disponível
        Exemplo: {
            "TECIDO001": 1000.0,
            "ALGODAO001": 800.0,
            "FIO001": 600.0,
            "POLIESTER001": 400.0
        }
        """
        materiais = self.get_todos_materiais()
        return {
            material["id_material"]: material["quantidade_disponivel"]
            for material in materiais
        }

# Exemplo de uso
if __name__ == "__main__":
    db_handler = DatabaseHandler()

    print(db_handler.get_quantidade_todos_materiais())

