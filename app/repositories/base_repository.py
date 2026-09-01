import json
import os
from abc import ABC, abstractmethod
from pathlib import Path


class BaseRepository(ABC):
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados
        self._assegurar_arquivo()
    
    def _assegurar_arquivo(self):
        """Cria o arquivo de dados se não existir"""
        if not os.path.exists(self.arquivo_dados):
            os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _carregar(self):
        """Carrega dados do arquivo"""
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _salvar(self, dados):
        """Salva dados no arquivo"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    @abstractmethod
    def salvar(self, entidade):
        pass
    
    @abstractmethod
    def obter_por_id(self, id):
        pass
    
    @abstractmethod
    def listar_todos(self):
        pass
    
    @abstractmethod
    def atualizar(self, entidade):
        pass
    
    @abstractmethod
    def deletar(self, id):
        pass
