# Executar o backend do socioclub Localmente

## Passo 1: Instale as Dependências

1. Abra o terminal ou prompt de comando.

2. Execute o seguinte comando para instalar o FastAPI:

```bash
pip install fastapi
```
3. Em seguida, instale o uvicorn para servir sua aplicação web:

```bash
pip install "uvicorn[standard]"
```

4. No terminal, navegue até o diretório onde está localizado o seu projeto Python.

5. Execute o seguinte comando para iniciar sua API localmente:

```bash
uvicorn app:app --reload
```

Substitua main pelo nome do arquivo Python principal que contém sua aplicação FastAPI e app pelo nome da variável que contém a sua instância FastAPI, se for diferente.

Verifique se sua API está funcionando corretamente acessando http://localhost:8000 (ou outra porta, dependendo da configuração).

