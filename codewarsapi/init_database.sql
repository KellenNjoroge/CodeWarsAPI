CREATE TABLE IF NOT EXISTS problem (
    slug varchar PRIMARY_KEY,
    language varchar PRIMARY_KEY,
    name varchar,
    description varchar,
    projectId varchar,
    solutionId varchar,
    code varchar,
    exampleFixture varchar,
    setup varchar
);

CREATE TABLE CurrentSession(
    Lock char(1) not null DEFAULT 'X',
    projectId varchar,
    solutionId varchar,

    constraint PK_T1 PRIMARY KEY (Lock),
    constraint CK_T1_Locked CHECK (Lock='X')
);

insert into CurrentSession values ("X", "", "");
