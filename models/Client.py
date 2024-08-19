from typing import Optional
from pydantic import BaseModel, validator
import re
from typing import ClassVar

#Fazer validação dos atributos

class Client(BaseModel):
    id: Optional[int] = None
    cpf: Optional[str] = None
    name: str
    email: str
    password: str

    #String com nome dos atributos
    dictId: ClassVar[str] = 'id'
    dictCpf: ClassVar[str] = 'cpf'
    dictName: ClassVar[str] = 'name'
    dictEmail: ClassVar[str] = 'email'
    dictPassword: ClassVar[str] = 'password'


    # @validator('email')
    # def validate_email(self, value):
    #     if not re.match('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', value):
    #         raise ValueError('Email inválido')
    #     return value
    
    # @validator('name')
    # def validate_name(self, value):
    #     if not re.match('^[a-zA-ZÀ-ú]+(?: [a-zA-ZÀ-ú]+)*$', value):
    #         raise ValueError('Nome inválido')
    #     return value
    
    # @validator('cpf')
    # def validate_cpf(self, value):
    #     if not re.match('^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
    #         raise ValueError('CPF inválido')
    #     return value