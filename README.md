MoMo ETL Pipeline

Project Description

A fullstack application that processes MTN Mobile Money (MoMo) SMS data in XML format, cleans and categorizes transactions, stores them in a relational database, and visualizes the data through an interactive dashboard.

Team Name
[Team 11]

Team Members

Tiffany Lina Turate - lina-tiffany
Admire Chagaresango - octaviusthe3rd
Lydivine Nshuti - nlydivine

Architecture Diagram
[https://drive.google.com/file/d/1jXpKmj3E2HYtPRAqd0D4uXrv3F4ObXXv/view]

Scrum Board
[https://trello.com/b/nh1maeFP/momo-etl-pipeline]



Database Design

Overview

The database is designed to store, query, and analyze MoMo SMS transaction data. It follows a relational model with five core tables that maintain data integrity through foreign key constraints.

Entity Relationship Diagram (ERD)
The full ERD is available in /docs/erd_diagram.png

Database Schema
The database consists of the following:

users (Stores all MoMo users (senders and receivers))

transactions (Core table storing all transaction records parsed from SMS data)

transaction_categories (Classifies transactions by type (e.g. Incoming Money, Payment, Withdrawal))

transaction_parties (Junction table linking users to transactions with their role (sender/receiver))

system_logs (Tracks the processing status of each transaction through the pipeline)

Relationships

A user can be involved in many transactions (as sender or receiver)
A transaction can involve many users
This many-to-many relationship is resolved through the transaction_parties junction table
Each transaction belongs to one transaction_category
Each transaction has exactly one system_log entry (1:1 relationship)

SQL Setup Script
The full database setup script is located at /database/database_setup.sql. It includes:

DDL statements to create all tables with constraints
Foreign key relationships for referential integrity
Sample data for testing

JSON Data Models
JSON representations of all database entities are located at /examples/json_schemas.json.

These schemas show how the relational data is serialized for API responses, including a complete nested transaction object that combines transaction details, category, parties (with full user info), and system log into a single response object.

