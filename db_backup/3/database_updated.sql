PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "student_management_app_studentdetails" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "register_number" integer NOT NULL UNIQUE,
    "name" varchar(250) NOT NULL,
    "gender" varchar(50) NOT NULL,
    "date_of_birth" datetime NOT NULL,
    "blood_group" varchar(100) NOT NULL,
    "caste" varchar(150) NOT NULL,
    "community" varchar(150) NOT NULL,
    "religion" varchar(150) NOT NULL,
    "mail_id" varchar(250) NOT NULL,
    "phone_number" varchar(20) NOT NULL,
    "aadhar_number" varchar(50) NOT NULL,
    "address" varchar(254) NOT NULL,
    "date_of_joining" datetime NOT NULL,
    "degree" varchar(50) NOT NULL,
    "department" varchar(250) NOT NULL,
    "student_photo" varchar(100) NOT NULL,
    "father_name" varchar(250) NOT NULL,
    "mother_name" varchar(250) NOT NULL,
    "father_occupation" varchar(250) NOT NULL,
    "mother_occupation" varchar(250) NOT NULL,
    "parent_phone_number" varchar(250) NOT NULL,
    "parent_annual_income" varchar(250) NOT NULL,
    "family_photo" varchar(100) NOT NULL,
    "bank_name" varchar(254) NOT NULL,
    "bank_account_number" varchar(50) NOT NULL,
    "ifsc_code" varchar(20) NOT NULL
);

DELETE FROM sqlite_sequence;

COMMIT;
