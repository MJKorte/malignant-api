CREATE TABLE `Variants` (
	`Chromosome` char(5) NOT NULL,
	`Pos` int(14) NOT NULL,
	`ID` char(15) NOT NULL,
	`REF` char(45) NOT NULL,
	`ALT` char(60) NOT NULL,
	`AF` float(25) NOT NULL,
	`genesymbol` char(16) NOT NULL,
	`gene` char(16) NOT NULL,
	`uniprot_acc` char(16) NOT NULL
);

