class Jogo:
    def __init__(self, nome: str, ano_lancamento: int, plataformas: list[str], categoria: str) -> None:
        self._nome = nome
        self._ano_lancamento = ano_lancamento
        self._plataformas = plataformas
        self._categoria = categoria
        
    @property
    def nome(self):
        return self._nome.upper()
    
    @property
    def ano_lancamento(self):
        return self._ano_lancamento
    
    @property
    def plataformas(self):
        return self._plataformas
    
    @property
    def categoria(self):
        return self._categoria