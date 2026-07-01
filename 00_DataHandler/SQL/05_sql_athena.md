## Datas:
- ###### DATE_DIFF:
```sql
-- Calcula a diferença entre duas datas em uma unidade especifica
SELECT DATE_DIFF('day', DATE'2024-01-01', DATE'2024-03-15')
-- Unidades aceitas: 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'.
```
- ###### DATE_ADD:
```sql
-- Soma ou Subtrai um intervalo a uma data
SELECT DATE_ADD('day', 7, DATE'2024-01-01')  -- 2024-01-08
SELECT DATE_ADD('day', -1, DATE'2024-01-08')  -- 2024-01-08
```
- ###### DATA_TRUNC:
```sql
-- Trunca a data para o inicio do período
SELECT DATE_TRUNC('month', DATE'2024-03-15')  -- 2024-03-01
SELECT DATE_TRUNC('year', DATE'2024-03-15')  -- 2024-01-01
SELECT DATE_TRUNC('week', DATE'2024-03-15')  -- 2024-03-11 (segunda-feira)
```
- ###### DATE_PARSE:
```sql
-- Transforma string em data
SELECT DATE_PARSE('2024-01-15', '%Y-%m-%d')
```
- ###### DATE_FORMAT:
```sql
-- Transforma data em string
SELECT DATE_FORMAT(current_date, '%d/%m/%Y')
```
- ###### CURRENT_DATE:
```sql
-- Pega o timestemp atual
SELECT CURRENT_DATE
```
- ###### EXTRACT:
```sql
-- Extrai ano mes ou dia de uma data
SELECT EXTRACT(YEAR FROM CURRENT_DATE) as ano
```
- ###### INTERVAL
```sql
-- Soma valores em uma data
SELECT CURRENT_DATE + INTERVAL '7' DAY
```

## Strings: 
- ###### SPLIT:
```sql
-- Retornar um Array
SELECT SPLIT('a,b,c', ',')
```
- ###### SPLIT_PART:
```sql
-- Retorna b é como transformar em lista e pegar o 2 indice
SELECT SPLIT_PART('a,b,c', ',', 2)
```
- ###### CONCAT:
```sql
-- Contatena duas strings
SELECT CONCAT('Olá', ' ', 'Mundo')
```
- ###### SUBSTR:
```sql
-- Faz o slice em uma string: retorna "abc"
SELECT SUBSTR('abcdef', 1, 3)
```
- ###### UPPER & LOWER:
```sql
SELECT UPPER('nome'), LOWER('sobrenome')
```

- ###### TRIM:
```sql
-- Remove espaços
SELECT TRIM('   oi   ')
```
- ###### REPLACE:
```sql
-- Substitui, aaa vira ooo
SELECT REPLACE('aaa', 'a', 'o')
```

## JSON:
- ###### JSON_EXTRACT:
```sql
-- Retorna JSON ("your_name")
SELECT JSON_EXTRACT('{"nome":"your_name"}', '$.nome')
```
- ###### JSON_EXTRACT_SCALAR:
```sql
-- Retorna string your_name
SELECT JSON_EXTRACT_SCALAR('{"nome":"your_name"}', '$.nome')
```
- ###### JSON_QUERY:
```sql
-- É como o extract
SELECT JSON_QUERY('{"a":1}', '$.a')
```

## Arrays/Mapas:
Usados quando temos colunas assim:
cliente_id | compras
-----------|-------------------------
1          | [100, 200, 300]
2          | [50, 80]

ou como `json`:
cliente_id | atributos
-----------|-------------------------
1          | {"idade": 30, "renda": 1500}
- ###### CARDINALITY:
```sql
-- Nos fala quantos itens o array tem
SELECT 
  cliente_id,
  CARDINALITY(compras) as qtd_compras
FROM tabela
```
- ###### UNNEST:
```sql
-- Transforma a linha com array em coluna
SELECT cliente_id, valor
FROM tabela
CROSS JOIN UNNEST(compras) AS t(valor)
/*
Antes:
| cliente_id | compras       |
| ---------- | ------------- |
| 1          | [100,200,300] |

Depois:
| cliente_id | valor |
| ---------- | ----- |
| 1          | 100   |
| 1          | 200   |
| 1          | 300   |

*/
```
- ###### ELEMENT_AT:
```sql
-- Pega um item especifico
SELECT ELEMENT_AT(compras, 1) as primeira_compra
FROM tabela
```
- ###### MAP_KEYS:
```sql
-- Pega as chaves de um dicionario
SELECT MAP_KEYS(atributos)
FROM tabela
```
- ###### MAP_VALUES:
```sql
-- Pega os valores de um json
SELECT MAP_VALUES(atributos)
FROM tabela
```

## Funções de janela:
- ###### LAG:
```sql
-- Olha para trás
SELECT 
  data,
  valor,
  LAG(valor) OVER (ORDER BY data) AS valor_anterior
FROM vendas
/*
| data       | valor | valor_anterior |
| ---------- | ----- | -------------- |
| 2024-01-01 | 100   | NULL           |
| 2024-01-02 | 150   | 100            |
| 2024-01-03 | 120   | 150            |
*/
```
- ###### LEAD:
```sql
-- Olha para frente
SELECT 
  data,
  valor,
  LEAD(valor) OVER (ORDER BY data) AS proximo_valor
FROM vendas
/*
| data       | valor | proximo_valor |
| ---------- | ----- | ------------- |
| 2024-01-01 | 100   | 150           |
| 2024-01-02 | 150   | 120           |
| 2024-01-03 | 120   | NULL          |
*/
```

## WHERE EXISTS:
```sql
-- Faz a filtragem caso exista
SELECT *
FROM clientes AS t1
WHERE EXISTS (
    SELECT 1
    FROM pedidos AS t2
    WHERE t1.id = t2.id
)
```