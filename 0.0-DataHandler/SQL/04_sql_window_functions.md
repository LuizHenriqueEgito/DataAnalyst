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
Comparar valores entre linhas consecutivas, como crescimento ou queda. Por exemplo: comparar as vendas de um mês com o mês anterior (ou próximo).
```SQL
WITH vendas_mensais AS (
    SELECT
        DATE_FORMAT(data_venda, '%Y-%m') AS mes
        ,SUM(qtd_vendida) AS total_vendido_mes
    FROM vendas
    GROUP BY DATE_FORMAT(data_venda, '%Y-%m')
    ORDER BY mes
)

SELECT
    mes
    ,total_vendido_mes
    ,LAG(total_vendido_mes, 1, NULL) OVER(ORDER BY mes) AS vendas_mes_anterior
    ,total_vendido_mes - LAG(total_vendido_mes) OVER(ORDER BY mes) AS diferenca
FROM vendas_mensais
ORDER BY mes
```
# Somas acumuladas com SUM()
Faz o `cumsum` de uma coluna.
```SQL
WITH vendas_mensais AS (
    SELECT
        DATE_FORMAT(data_venda, '%Y-%m') AS mes
        ,SUM(qtd_vendida) AS total_vendido_mes
    FROM vendas
    GROUP BY DATE_FORMAT(data_venda, '%Y-%m')
    ORDER BY mes
)

SELECT
    mes
    ,total_vendido_mes
    ,SUM(total_vendido_mes) OVER (ORDER BY mes) AS acumulado
FROM vendas_mensais
ORDER BY mes
```
# Percentuais acumulados para análise de Pareto
Mostrar o percentual acumulado em relação ao ttoal (ex: Regra de Pareto - 80/20). Exemplo prático, identificar quais produtos contribuem mais para o faturamento.
```SQL
SELECT
    nome_produto
    ,total_receita
    ,SUM(total_receita) OVER(ORDER BY total_receita DESC) / SUM(total_receita) OVER() * 100 AS percentual_acumulado
FROM (
    SELECT
        produto.id_produto
        ,produto.nome_produto
        ,SUM(vendas.receita_vendas) AS total_receita
    FROM produtos
    LEFT JOIN vendas
    ON produtos.id_produto = vendas.id_produto
    GROUP BY id_produto, nome_produto
)
```
# Categorização de valores com NTILE()
Divide os dados em quantis, permitindo classificar, segmentar ou dividir valores por faixas. Por exemplo criar 4 grupos de clientes com renda semelhante. Cada cliente deve ser classificado em uma "faixa de renda" (1 = mais alto, 4 = mais baixo).
```SQL
SELECT
    id_cliente
    ,nome
    ,renda_anual
    NTILE(4) OVER(ORDER BY renda_anual DESC) AS faixa_renda
FROM clientes
```
# Identificar Máximo e Mínimo com MAX() e MIN()
Identificar máximo e mínimo com MAX() e MIN(). Determinar valores máximos/mínimos em janelas específicas. Exemplo: Obter o maior valor de vendas dentro de um grupo de 3 meses consecutivos.
```SQL
SELECT
    DATE_FORMAT(data_venda, '%Y-%m') AS mes
    ,SUM(qtd_vendida) AS total_vendido_mes
    ,MAX(SUM(qtd_vendida)) OVER(ORDER BY DATE_FORMAT(data_venda, '%Y-%m') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS max_vendas_3_meses
    ,MIN(SUM(qtd_vendida)) OVER(ORDER BY DATE_FORMAT(data_venda, '%Y-%m') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS min_vendas_3_meses
FROM vendas
GROUP BY DATE_FORMAT(data_venda, '%Y-%m')
ORDER BY mes
```
# Analisando a contribuição percentual com funções de janela
Identificar os principais produtos ou clientes responsáveis pelas receitas. Calcular a participação percentual de cada mês em relação ao todo em termos de vendas.
```SQL
SELECT
    DATE_FORMAT(data_venda, '%Y-%m') AS mes
    ,SUM(qtd_vendida) AS total_vendido_mes
    ,SUM(SUM(qtd_vendida) / SUM(SUM(qtd_vendida))) OVER() * 100 AS total_geral
FROM vendas
GROUP BY DATE_FORMAT(data_venda, '%Y-%m')
```
# Análises segmentadas com PARTITION BY
```SQL
SELECT
    marca_produto
    ,nome_produto
    ,preco_unit
    RANK() OVER (PARTITION BY marca_produto ORDER BY preco_unit DESC) AS posicao
FROM produtos
```