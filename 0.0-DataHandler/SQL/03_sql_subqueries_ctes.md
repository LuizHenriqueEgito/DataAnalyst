# Subqueries & CTEs
No `SQL` *subqueries* e *CTEs* nos ajudam a criar tabelas temporárias em tempo de execução da query para auxiliar, na nossa query final. As vezes precisamos fazer algumas transformações em alguma(s) tabela(s) antes de continuar até nossa query final e é isso que *subqueries* e *CTEs* nos ajudam a fazer.

## Subqueries
É um pouco mais *poluida* do que *CTEs* durante o `FROM` nos criamos uma tabela com o tratamento que queremos, essa tabela é **pontual** e não pode ser reaproveitada além de deixar o código um pouco mais complexo e de dificil compreensão ela pode ser usada em queries simples.
```sql
SELECT * FROM (
    SELECT * FROM my_db.my_tb
    WHERE flag_filter = 1
)
```
## CTEs
Já com *CTEs* podemos criar tabelas temporarias (que existem durante a execução da sua query) esse tipo de tabela pode ser reutilizada, em queries mais complexas é recomendado utilizar *CTEs* ao invés de *subqueries*.
```sql
-- As CTEs são nomeadas para reutilização posterior
WITH tb_cte AS (
    SELECT * FROM my_db.my_tb
    WHERE flag_filter = 1
)

SELECT * FROM tb_cte
```