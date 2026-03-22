# RANK() & DENSE_RANK()
Cria `rankings` de registros ordenados, por exemplo ordenar clientes com base na renda_anual, identificando empates corretamente.
```SQL
-- Isso ordena, mas não rankeia
SELECT * FROM clientes
ORDER BY renda_anual
```
- `RANK`: Mesmo valor = mesmo rank, pula números no próximo
- `DENSE_RANK`: Mesmo valor = mesmo rank, NÃO pula números
## RANK()
`RANK` empata valores, os valores não são unicos e ao passar o valor ele pula, por exemplo se existir duas pessoas em terceiro lugar a proxima será a quinta.
```SQL
SELECT
    nome, email, renda_anual
    -- Quero ranquear (rank) em cima (over) de um conjunto de valores (renda_anual)
    -- com isso ordenamos e criamos uma nova coluna chamda posicao
    ,RANK() OVER(ORDER BY renda_anual DESC) AS posicao
FROM clientes
```

## DENSE_RANK()
`DENSE_RANK` empata valores, mas não pula o número.
```SQL
SELECT
    nome, email, renda_anual
    -- Quero ranquear (rank) em cima (over) de um conjunto de valores (renda_anual)
    -- com isso ordenamos e criamos uma nova coluna chamda posicao
    ,DENSE_RANK() OVER(ORDER BY renda_anual DESC) AS posicao
FROM clientes
```
| Aluno | Nota | rank_pos | dense_rank_pos |
|-------|------|----------|----------------|
| Ana | 100 | 1 | 1 |
| Bruno | 90 | 2 | 2 |
| Carla | 90 | 2 | 2 |
| Diego | 80 | 4 | 3 |
| Elisa | 80 | 4 | 3 |

# ROW_NUMBER()
Encontramos o N-ésimo maior valor com `ROW_NUMBER()`, a sua diferença para o `RANK` e `DENSE_RANK` é que ela não considera empate.
```SQL
SELECT nome, email, renda_anual FROM (
    SELECT
        nome, email, renda_anual
        -- Pega a posição
        ,ROW_NUMBER() OVER(ORDER BY renda_anual DESC) AS posicao
    FROM clientes
) AS tb_result
WHERE posicao = 2
```
| Aluno | Nota | rank_pos | dense_rank_pos | row_number |
|-------|------|----------|----------------| ---------- |
| Ana | 100 | 1 | 1 | 1 |
| Bruno | 90 | 2 | 2 | 2 |
| Carla | 90 | 2 | 2 | 3 |
| Diego | 80 | 4 | 3 | 4 |
| Elisa | 80 | 4 | 3 | 5 |

# Médias Móveis
Analisar tendências em séries temporais, como vnedas ou preços.
```SQL
SELECT
    DATE_FORMAT(data_venda, '%Y-%m') AS mes
    ,SUM(receita_venda) AS total_receita_mes
    -- Aqui fazemos a média movel
        -- Pega a média da soma da receita agrupada por mês
        -- ordenada pelo mês e o calculo é feito na linha atual + duas para trás
        -- é dai que vem o ROWS BETWEEN 2 PRECEDING AND CURRENT ROW (pegue a atual e duas para trás)
    ,AVG(SUM(receita_venda)) OVER(ORDER BY DATE_FORMAT(data_venda, '%Y-%m') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel_3_meses
FROM vendas
GROUP BY DATE_FORMAT(data_venda, '%Y-%m')
ORDER BY mes
```

# Comparação de valores com LAG() - Análise YoY

# Somas acumuladas com SUM()

# Percentuais acumulados para análise de Pareto

# Categorização de valores com NTILE()

# Identificar Máximo e Mínimo com MAX() e MIN()

# Analisando a contribuição percentual com funções de janela

# Análises segmentadas com PARTITION BY