TODO: Ajuste remova as imagens deixe apenas o código SQL
# GROUP BY
A clausula `GROUP BY` faz a agregação de linhas iguais e resume elas. A maneira como ele funciona é a seguinte:
1. Agrupa as linhas por uma (ou varias) coluna(s) através dos seus valores;
2. Junta os semelhantes;
3. Aplica a função de agregação (ou as funções de agregação)

IMPORTANTE: O que está no `SELECT` precisa estar ou no agrupamento `GROUP BY` ou em alguma função de agregação.

```SQL
SELECT
    geography
    ,card_type
    ,AVG(estimated_salary) AS mean_estimated_salary
    ,AVG(credit_score) AS mean_credit_score
FROM customer
GROUP BY geography, card_type
```
## Funções de agregação
- `COUNT`: Conta linhas
```sql
SELECT COUNT(*) FROM tb_main  -- Conta tudo até nulos
SELECT COUNT(coluna_a) from tb_main  -- conta ignorando nulos na coluna passada
```
- `SUM`: Soma valores de uma coluna;
- `AVG`: Faz a média de uma coluna;
- `MIN / MAX`: Pega o minimo ou o máximo de uma coluna;
- `COUNT(DISTINCT coluna_a)`: Faz a contagem de valores únicos em uma coluna.

## Contando Duplicados
```SQL
SELECT
    COUNT(DISTINCT id_customer) AS total_ids_unicos
    ,COUNT(id_customer) AS total_ids
FROM customers
WHERE dt_ref = DATE'2000-02-02'
```

## HAVING
O `HAVING` filtra grupos de resultados **após** aplicar o `GROUP BY`. É um `WHERE` para grupos.
```SQL
SELECT
    geography
    ,card_type
    ,AVG(estimated_salary) AS mean_estimated_salary
    ,AVG(credit_score) AS mean_credit_score
FROM customer
GROUP BY geography, card_type
HAVING AVG(estimated_salary) < 100000
```
Utilizando `WHERE` para filtrar antes do agrupamento `GROUP BY`
```SQL
SELECT
    geography
    ,card_type
    ,AVG(estimated_salary) AS mean_estimated_salary
    ,AVG(credit_score) AS mean_credit_score
FROM customer
WHERE is_active_member == 1
GROUP BY geography, card_type
HAVING AVG(estimated_salary) < 100000
```