DROP   SEQUENCE log_seq CASCADE;
CREATE SEQUENCE log_seq START 1;

DROP TABLE log;
CREATE TABLE log
(
    id             INT4 DEFAULT nextval('log_seq'),
    ts             TIMESTAMP,
    instrument     TEXT,
    granularity    TEXT,
    implementation INTEGER,
    component      TEXT,
    type           TEXT,
    message        TEXT
);

DROP TABLE model_config;
CREATE TABLE model_config
(
    id             INTEGER,
    implementation INTEGER,
    output         TEXT,
    atr            INTEGER,
    ma             INTEGER,
    continuation   INTEGER,
    reversal       INTEGER
);

DROP TABLE intelligence_config;
CREATE TABLE intelligence_config
(
    id             INTEGER,
    implementation INTEGER,
    output         INTEGER,
    distance       INTEGER,
    tp             INTEGER,
    sl             INTEGER,
    trl            INTEGER,
    min_seq        INTEGER,
    mac            INTEGER
);

DROP TABLE broker_config;
CREATE TABLE broker_config
(
    id            INTEGER,
    implementation INTEGER,
    risk          FLOAT
);

DROP TABLE account_config;
CREATE TABLE account_config
(
    implementation INTEGER,
    account        TEXT
);



