CREATE TABLE test_tsv_bcp (  --table name
	c1 varchar(max),
	c2 varchar(max),
	c3 varchar(max)
)


--truncate table test_tsv_bcp
--drop table test_tsv_bcp

--convert dtypes after loading as text
/*
ALTER TABLE test_tsv_bcp ALTER COLUMN c1 numeric
ALTER TABLE test_tsv_bcp ALTER COLUMN c1 smallint --want it to actually end up as int, no decimals
ALTER TABLE test_tsv_bcp ALTER COLUMN c2 numeric
ALTER TABLE test_tsv_bcp ALTER COLUMN c2 smallint --want it to actually end up as int, no decimals
ALTER TABLE test_tsv_bcp ALTER COLUMN c3 float --want to keep decimal places

*/