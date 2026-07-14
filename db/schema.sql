CREATE TABLE customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    phone       VARCHAR(20) NOT NULL,
    email       VARCHAR(255)
);
create table accounts (
    account_id varchar(64) primary KEY,
    customer_id VARCHAR(64) NOT NULL,
    card_number varchar(255) NOT NULL,
    card_type varchar (64) NOT NULL,
    balance varchar(255) NOT NULL,
    foreign key (customer_id) references customers(customer_id)
 );
 CREATE TABLE transactions (
    transaction_id VARCHAR(64)  PRIMARY KEY,
    account_id     VARCHAR(64)  NOT NULL,
    amount         FLOAT        NOT NULL,
    merchant       VARCHAR(255),
    location       VARCHAR(255),
    timestamp      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    is_flagged     BOOLEAN      DEFAULT FALSE,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE fraud_claims (
    claim_id       VARCHAR(64)  PRIMARY KEY,
    customer_id    VARCHAR(64)  NOT NULL,
    account_id     VARCHAR(64)  NOT NULL,
    transactions   TEXT         NOT NULL,
    submitted_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id)  REFERENCES accounts(account_id)
);

CREATE TABLE claim_status (
    claim_id     VARCHAR(64)  NOT NULL,
    status       VARCHAR(100) DEFAULT 'Under Investigation',
    update_note  TEXT         DEFAULT 'Fraud team is reviewing your claim',
    updated_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (claim_id) REFERENCES fraud_claims(claim_id)
);