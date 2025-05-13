DROP TABLE IF EXISTS eligible_members;

CREATE TABLE eligible_members (
    id                     BIGSERIAL PRIMARY KEY,
    member_id              VARCHAR(20) UNIQUE,
    referral_code          VARCHAR(20),
    benefit_start_date     TIMESTAMP,
    benefit_end_date       TIMESTAMP,
    dob                    DATE,
    first_name             VARCHAR(100),
    last_name              VARCHAR(100),
    middle_name            VARCHAR(10),
    gender                 VARCHAR(5) CHECK (gender IN ('M', 'F', 'O', 'N') OR gender IS NULL),
    address_line_1         VARCHAR(200),
    address_line_2         VARCHAR(200),
    city                   VARCHAR(100),
    state                  CHAR(2),
    zip_code               VARCHAR(10),
    primary_phone_number   VARCHAR(15),
    secondary_phone_number VARCHAR(15),
    email                  VARCHAR(100),
    coverage_type          VARCHAR(10) CHECK (coverage_type IN ('PRIMARY', 'SECONDARY') OR coverage_type IS NULL),
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);