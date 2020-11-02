CREATE TABLE {0} (  --table name
	hhno INT,
	fraction_with_jobs_outside REAL,
	hhsize INT,
	hhvehs SMALLINT,
	hhwkrs SMALLINT,
	hhftw SMALLINT,
	hhptw SMALLINT,
	hhret SMALLINT,
	hhoad SMALLINT,
	hhuni SMALLINT,
	hhhsc SMALLINT,
	hh515 SMALLINT,
	hhcu5 SMALLINT,
	hhincome INT,
	hownrent SMALLINT,
	hrestype SMALLINT,
	hhparcel INT,
	zone_id SMALLINT,
	hhtaz SMALLINT,
	hhexpfac SMALLINT,
	samptype SMALLINT
)

	



SELECT COLUMN_NAME,* 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'raw_hh2035_111' AND TABLE_SCHEMA='dbo'
