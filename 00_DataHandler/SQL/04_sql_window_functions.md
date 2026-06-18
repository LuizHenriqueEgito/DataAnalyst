# WINDOW FUNCTIONS
Sem `window functions` quando fazemos `GROUP BY` perdemos as colunas fora do agrupamento com `window functions` as colunas se mantém. Perceba que se quisessemos um número de algum agrupamento sem `window functions` criariamos uma tabela agrupada e depois realizamos o cruzamento mas isso não é preciso utilizando `window functions`.

Toda `window functions` segue a ordem:
```SQL
FUNCAO() OVER(...)

# Por exemplo
SUM(vendas) OVER(...)
```
- `OVER()`: Over sem nada, a janela é a tabela inteira. O valor de SUM(vendas) vai ficar em TODAS as linhas da tabela.
- `PARTITION BY`: É como um `GROUP BY` que não agrupa.
- `ORDER BY`: A janela passa a respeitar uma ordem, você vai acumulando.

Você tem as seguintes opções:
```SQL
# Janela = Tabela inteira
OVER()
-- Tabela
-- ------
-- 100
-- 200
-- 300

-- FUNCAO(100, 200, 300)

# Divide a tabela em grupos
OVER(PARTITION BY ...)
-- PARTITION Sul
-- -------------
-- 100
-- 200

-- PARTITION Norte
-- -------------
-- 300
-- 400

# Não cria grupos cria ordem e a função de agregação vai acumulando
OVER(ORDER BY ...)
-- Linha 1 vê:
-- 100

-- Linha 2 vê:
-- 100
-- 200

-- Linha 3 vê:
-- 100
-- 200
-- 300

# Cria grupos e ordena dentro dos grupos
OVER(PARTITION BY ... ORDER BY ...)
-- Cliente A
-- ----------
-- 100
-- 100+50
-- 100+50+200

-- Cliente B
-- ----------
-- 80
-- 80+40
```

# RANK() & DENSE_RANK()
Cria `rankings` de registros ordenados, por exemplo ordenar clientes com base na renda_anual, identificando empates corretamente.
```SQL
-- Isso ordena, mas não rankeia
SELECT * FROM clientes
ORDER BY renda_anual
```
- `RANK`: Mesmo valor $=$ mesmo rank, pula números no próximo
- `DENSE_RANK`: Mesmo valor = mesmo rank, NÃO pula números
## 1. RANK()
`RANK` empata valores, os valores não são unicos e ao passar o valor ele pula, por exemplo se existir duas pessoas em terceiro lugar a proxima será a quinta.
```SQL
SELECT
    nome, email, renda_anual
    -- Quero ranquear (rank) em cima (over) de um conjunto de valores (renda_anual)
    -- com isso ordenamos e criamos uma nova coluna chamda posicao
    ,RANK() OVER(ORDER BY renda_anual DESC) AS posicao
FROM clientes
```
| nome | email | renda_anual | posicao |
|---|---|---|---|
| Ana | ana@email.com | 220000 | 1 |
| Bruno | bruno@email.com | 195000 | 2 |
| Carla | carla@email.com | 195000 | 2 |
| Diego | diego@email.com | 175000 | 4 |
| Elisa | elisa@email.com | 175000 | 4 |
| Felipe | felipe@email.com | 150000 | 6 |

## 2. DENSE_RANK()
`DENSE_RANK` empata valores, mas não pula o número.
```SQL
SELECT
    nome, email, renda_anual
    -- Quero ranquear (rank) em cima (over) de um conjunto de valores (renda_anual)
    -- com isso ordenamos e criamos uma nova coluna chamda posicao
    ,DENSE_RANK() OVER(ORDER BY renda_anual DESC) AS posicao
FROM clientes
```
| nome | email | renda_anual | posicao |
|---|---|---|---|
| Ana | ana@email.com | 220000 | 1 |
| Bruno | bruno@email.com | 195000 | 2 |
| Carla | carla@email.com | 195000 | 2 |
| Diego | diego@email.com | 175000 | 3 |
| Elisa | elisa@email.com | 175000 | 3 |
| Felipe | felipe@email.com | 150000 | 4 |

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
| nome | email | renda_anual |
|---|---|---|
| Bruno | bruno@email.com | 195000 |

# Médias Móveis
Analisar tendências em séries temporais, como vendas ou preços.
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
| mes | total_receita_mes | media_movel_3_meses |
|---|---|---|
| 2026-01 | 45000 | 45000,00 |
| 2026-02 | 52000 | 48500,00 |
| 2026-03 | 48000 | 48333,33 |
| 2026-04 | 61000 | 53666,67 |
| 2026-05 | 58000 | 55666,67 |
| 2026-06 | 67000 | 62000,00 |

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
| mes | total_vendido_mes | vendas_mes_anterior | diferenca |
|---|---|---|---|
| 2026-01 | 320 | NULL | NULL |
| 2026-02 | 410 | 320 | 90 |
| 2026-03 | 380 | 410 | -30 |
| 2026-04 | 455 | 380 | 75 |
| 2026-05 | 502 | 455 | 47 |

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
| mes | total_vendido_mes | acumulado |
|---|---|---|
| 2026-01 | 320 | 320 |
| 2026-02 | 410 | 730 |
| 2026-03 | 380 | 1110 |
| 2026-04 | 455 | 1565 |
| 2026-05 | 502 | 2067 |

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
| nome_produto | total_receita | percentual_acumulado |
|---|---|---|
| Notebook X1 | 185000 | 49,40 |
| Monitor 4K | 98000 | 75,57 |
| Teclado Mecânico | 41000 | 86,52 |
| Mouse Gamer | 32000 | 95,06 |
| Webcam HD | 18500 | 100,00 |

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
| id_cliente | nome | renda_anual | faixa_renda |
|---|---|---|---|
| 101 | Ana | 220000 | 1 |
| 102 | Bruno | 195000 | 1 |
| 103 | Carla | 185000 | 2 |
| 104 | Diego | 175000 | 2 |
| 105 | Elisa | 150000 | 3 |
| 106 | Felipe | 140000 | 3 |
| 107 | Gabriela | 120000 | 4 |
| 108 | Hugo | 95000 | 4 |

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
| mes | total_vendido_mes | max_vendas_3_meses | min_vendas_3_meses |
|---|---|---|---|
| 2026-01 | 320 | 320 | 320 |
| 2026-02 | 410 | 410 | 320 |
| 2026-03 | 380 | 410 | 320 |
| 2026-04 | 455 | 455 | 380 |
| 2026-05 | 502 | 502 | 380 |

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
| mes | total_vendido_mes | total_geral |
|---|---|---|
| 2026-01 | 320 | 15,48 |
| 2026-02 | 410 | 19,84 |
| 2026-03 | 380 | 18,38 |
| 2026-04 | 455 | 22,01 |
| 2026-05 | 502 | 24,29 |

# Análises segmentadas com PARTITION BY
```SQL
SELECT
    marca_produto
    ,nome_produto
    ,preco_unit
    RANK() OVER (PARTITION BY marca_produto ORDER BY preco_unit DESC) AS posicao
FROM produtos
```
| marca_produto | nome_produto | preco_unit | posicao |
|---|---|---|---|
| Dell | XPS 13 | 6800 | 1 |
| Dell | Inspiron 15 | 3200 | 2 |
| Dell | Vostro 14 | 2900 | 3 |
| HP | Omen 16 | 7500 | 1 |
| HP | Pavilion x360 | 4100 | 2 |
| Lenovo | ThinkPad X1 | 8900 | 1 |
| Lenovo | Legion 5 | 6200 | 2 |
| Lenovo | IdeaPad 3 | 2600 | 3 |