TODO: Ajuste remova as imagens deixe apenas o código SQL
# Dataset
![alt text](images/image_0.png)

## Filters
![alt text](images/image_1.png)

## IN
![alt text](images/image_2.png)

## NOT IN
![alt text](images/image_3.png)

## BETWEEN
![alt text](images/image_4.png)

## NLARGEST & NSMALLEST
![alt text](images/image_5.png)

## NA's
![alt text](images/image_6.png)
![alt text](images/image_7.png)

## Linhas Duplicadas
![alt text](images/image_8.png)
![alt text](images/image_9.png)
![alt text](images/image_10.png)

## DISTINCT
O `DISTINCT` remove linhas duplicadas do resultado de uma consulta, retornando apenas valores únicos.
![alt text](images/image_11.png)

## CASE WHEN
O `CASE WHEN` faz uma clausula *if* *else* na sua coluna. Ele também pode fazer interações entre as colunas.
![alt text](images/image_12.png)

## COALESCE
Retorna o primeiro valor não nulo de uma lista de argumentos, é útil para lidar com valores `NULL`.
```SQL
COALESCE(valor1, valor2, valor3, ..., valorN)
```

## Ordem de Precedencia de uma Query
1. FROM
2. JOIN
3. WHERE
4. GROUP BY
5. HAVING
6. SELECT
7. DISTINCT
8. ORDER BY
9. LIMIT

```txt
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```
