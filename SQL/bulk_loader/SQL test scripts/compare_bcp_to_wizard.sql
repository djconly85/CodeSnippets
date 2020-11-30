select top 1 * from raw_trip2035_209
where id = -1391883144
select top 1 * from test_trip_bcp
where id = -1391883144

select
	t1.id as wiz_id,
	t2.id as bcp_id,
	t1.travdist as wiz_travdist,
	t2.travdist as bcp_travdist
INTO #compare_trip_tb
FROM raw_trip2035_209 t1
	LEFT JOIN test_trip_bcp t2
		ON t1.id = t2.id

--check to see if any records where null
SELECT * FROM  #compare_trip_tb
WHERE bcp_id IS NULL

--instances where BCP-loaded difference is different from wizard difference,
--beyond what would be expected from rounding
SELECT * FROM #compare_trip_tb
WHERE (wiz_travdist - bcp_travdist) < 0