CREATE TABLE D_GENRE (
    ID_GENRE  BIGSERIAL       NOT NULL PRIMARY KEY,
    NM_GENRE  VARCHAR (50)    NOT NULL,
    LINDATE   DATE            NOT NULL,
    LINSOURCE VARCHAR (50) 	  NOT NULL
);
