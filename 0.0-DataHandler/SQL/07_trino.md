# Rode o Trino no Docker
Isso pega a `imagem` docker e já sobe o container:
```bash
docker run -d --name trino -p 8080:8080 trinodb/trino
```

# Rodando novamento
Depois de ter a `imagem` docker podemos rodar novamente o container com o `trino`:
```bash
docker start trino
```
Isso sobe seu servidor `trino`.

# Rodando Queries
Para rodar queries no trino no terminal rode:
```bash
docker exec -it trino trino
```
Agora é só rodar suas queries.