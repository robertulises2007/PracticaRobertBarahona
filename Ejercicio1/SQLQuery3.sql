use PracticaIMHN;

CREATE TABLE dbo.DemandaProyectada(
	idDemanda bigint PRIMARY KEY NOT NULL,
	CodigoCliente varchar(50) NOT NULL,
	MesCreacion datetime NOT NULL,
	FechaModificacion datetime NOT NULL,
	Fecha datetime NOT NULL,
	Mes varchar(20) NOT NULL,
	NoMes int NOT NULL,
	Año int NOT NULL,
	Semestre varchar(2) NOT NULL,
	Trimestre varchar(2) NOT NULL,
	Linea varchar(100) NOT NULL,
	BaseTipo varchar(2) NULL,
	BaseNumero varchar(5) NULL,
	Categoria varchar(100) NULL,
	Sublinea varchar(100) NULL,
	CodigoColor varchar(50) NULL,
	Talla varchar(100) NOT NULL,
	Cantidad int NOT NULL,
	Base varchar(100) NULL
	)