class Usuario:
    def __init__(self, nome: str, nickname: str, senha: str):
        self._nome = nome
        self._nickname = nickname
        self._senha = senha
        
    @property
    def nome(self):
        return self._nome
    
    @property
    def nickname(self):
        return self._nickname
    
    @property
    def senha(self):
        return self._senha