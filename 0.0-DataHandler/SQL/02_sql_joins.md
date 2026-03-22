# JOIN

## INNER JOIN
Retorna apenas registros que têm correspondência em **ambas** as tabelas.
## LEFT JOIN (LEFT OUTER JOIN)
Retorna todos os registros da tabela à esquerda e os correspondentes da direita. Quando não há correspondência, retorna `NULL` para as colunas da direita.
## RIGHT JOIN (RIGHT OUTER JOIN)
Retorna todos os registros da tabela à direita e os correspondentes da esquerda. Quando não há correspondência, retorna `NULL` para as colunas da esquerda.
## FULL JOIN (FULL OUTER JOIN)
Retorna todos os registros de ambas as tabelas. Quando não há correspondência de um lado, preenche com `NULL`.
## UNION ALL
Combina os resultados de duas ou mais consultas, mantendo todas as linhas (inclui duplicatas). É mais rápido porque não faz verificação de duplicidade.
## UNION
Combina os resultados de duas ou mais consultas, removendo linhas duplicadas. É mais lento que `UNION ALL` porque precisa fazer a deduplicação.

# JOINS ESPECIFICOS (ATHENA)
## CROSS JOIN
Retorna o **produto cartesiano** - cada linha da primeira tabela combinada com todas as linhas da segunda.
## LATERAL JOIN
Permite usar colunas da tabela à esquerda dentro de uma subconsulta da direita. Muito útil para `UNNEST`
```SQL
SELECT cliente.nome, item
FROM clientes
CROSS JOIN UNNEST(cliente.compras) AS t(item)

-- Ou com LATERAL explícito
SELECT *
FROM tabela_a
CROSS JOIN LATERAL (
    SELECT * FROM tabela_b WHERE tabela_b.id = tabela_a.id
)
```
## SEMI JOIN
Não é uma palavra-chave específica, mas um padrão comum. Retorna registros da primeira tabela que têm correspondência na segunda, sem duplicar.
```SQL
SELECT *
FROM tabela_a
WHERE EXISTS (
    SELECT 1 
    FROM tabela_b 
    WHERE tabela_b.id = tabela_a.id
)

-- Ou
SELECT *
FROM tabela_a
WHERE id IN (SELECT id FROM tabela_b)
```
## ANTI JOIN
Retorna registros da primeira tabela que não têm correspondência na segunda.
```SQL
SELECT *
FROM tabela_a
WHERE NOT EXISTS (
    SELECT 1 
    FROM tabela_b 
    WHERE tabela_b.id = tabela_a.id
)

-- Ou
SELECT *
FROM tabela_a
WHERE id NOT IN (SELECT id FROM tabela_b)
```
