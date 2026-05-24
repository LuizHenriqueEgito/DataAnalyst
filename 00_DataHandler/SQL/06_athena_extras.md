- Como tranformar uma coluna BIGINT em data
```sql
DATE_PARSE(CAST(anomesdia AS VARCHAR), '%Y%m%d')
```

- Como fazer operações com datas (Voltar um mês, adiantar um dia)
```sql
-- Voltando 1 mês
DATE_ADD(
    'month',
    -1,
    DATE_PARSE(CAST(anomesdia AS VARCHAR), '%Y%m%d')
)
-- Adiantando 1 dia
DATE_ADD(
    'day',
    1,
    DATE_PARSE(CAST(anomesdia AS VARCHAR), '%Y%m%d')
)
```

- Tenho uma tabela com YYYYMMDD como pegar a partição maxima de cada YYYYMM
```sql
SELECT *
FROM (
    SELECT
        tb.*,
        ROW_NUMBER() OVER (
            PARTITION BY CAST(anomesdia / 100 AS INTEGER)
            ORDER BY anomesdia DESC
        ) AS rn
    FROM tb_main tb
) t
WHERE rn = 1
```

- Como passar uma lista de YYYYMM e fazer com que a tabela encontre a partição máxima YYYYMMDD

```sql
WITH tb_data_values AS (
    SELECT * FROM (
        VALUES
            202505,
            202506,
            202507
    ) AS t(anomes)
)

SELECT *
FROM (
    SELECT 
        tb.*
        ,ROW_NUMBER() OVER (
            PARTITION BY CAST(anomesdia / 100 AS INTEGER)
            ORDER BY anomesdia DESC
        ) AS rn
    FROM tb_main tb
    WHERE CAST(anomesdia / 100 AS INTEGER) IN (
        SELECT anomes FROM tb_data_values
    )
) t
WHERE rn = 1
```

- Como passar uma lista de YYYYMM e fazer com que a tabela encontre as partições retroagidas em n meses
```sql
WITH tb_data_values AS (
    SELECT * FROM (
        VALUES
            202505,
            202506,
            202507
    ) AS t(anomes)
)

, tb_meses_retroagidos AS (
    SELECT
        anomes,
        
        -- converte para data (primeiro dia do mês)
        date_format(
            date_add(
                'month',
                -3,
                date_parse(CAST(anomes AS VARCHAR) || '01', '%Y%m%d')
            ),
            '%Y%m'
        ) AS anomes_retro
    FROM tb_data_values
)

SELECT *
FROM tb_main
WHERE CAST(anomesdia / 100 AS INTEGER) IN (
    SELECT CAST(anomes_retro AS INTEGER)
    FROM tb_meses_retroagidos
)
```
