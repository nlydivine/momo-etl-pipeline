# MoMo SMS Data Processing  ERD DocumentationSystem 

## Design Justification

The ERD for the MoMo SMS Data Processing System was designed to accurately represent the structure of MoMo XML transaction data while following relational database best practices including normalization, referential integrity, and scalability.

Four core entities were identified from the data: USERS, TRANSACTIONS, TRANSACTION_CATEGORIES, and SYSTEM_LOGS. The USERS entity centralizes all participant identity  names, phone numbers, and  eliminating redundancy that would arise from embedding user details directly inside transaction records. The TRANSACTIONS entity serves as the hub of the schema, storing financial event data such as amount, currency, status, reference code, and raw SMS text, which ensures full traceability back to the original source message.emails data 

TRANSACTION_CATEGORIES was separated from TRANSACTIONS deliberately. Storing category types such as transfers, payments, and airtime purchases in a dedicated lookup table makes it easy to add or modify categories without altering transaction records, improving long-term maintainability. SYSTEM_LOGS was decoupled from TRANSACTIONS to maintain a clean audit trail; since one transaction can trigger multiple log entries at different processing stages, a one-to-many relationship was applied between TRANSACTIONS and SYSTEM_LOGS.

The most significant design decision was resolving the many-to-many relationship between USERS and TRANSACTIONS. Because a single transaction involves multiple users in different  sender, receiver, and  and a user can appear in many transactions, a junction table called TRANSACTION_PARTIES was introduced. This table holds transaction_id, user_id, and a role attribute, cleanly resolving the M:N relationship without multi-valued columns.agent roles 

All primary keys use integer IDs for join efficiency, and foreign keys enforce referential integrity across all entities. The resulting schema achieves Third Normal Form (3NF), supports high transaction volumes, and aligns directly with real MoMo financial data structures.
