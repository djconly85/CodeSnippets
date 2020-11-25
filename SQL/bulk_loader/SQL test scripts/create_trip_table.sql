CREATE TABLE test_trip_bcp (  --table name
	id	varchar,
	tour_id	varchar,
	hhno	varchar,
	pno	varchar,
	day	varchar,
	tour	varchar,
	half	varchar,
	tseg	varchar,
	tsvid	varchar,
	opurp	varchar,
	dpurp	varchar,
	oadtyp	varchar,
	dadtyp	varchar,
	opcl	varchar,
	otaz	varchar,
	dpcl	varchar,
	dtaz	varchar,
	mode	varchar,
	pathtype	varchar,
	dorp	varchar,
	deptm	varchar,
	arrtm	varchar,
	endacttm	varchar,
	travtime	varchar,
	travcost	varchar,
	travdist	varchar,
	vot	varchar,
	trexpfac	varchar,
	timeau	varchar,
	distau	varchar,
	distcong	varchar
)




SELECT COLUMN_NAME,DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'raw_trip2016_51' AND TABLE_SCHEMA='dbo'
