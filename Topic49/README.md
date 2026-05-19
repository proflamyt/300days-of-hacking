---
title: "GraphQL"
topic: "graphql"
tags: [graphql, api, introspection, mutation, query, web-security, injection]
difficulty: intermediate
day: 49
layout: default
parent: Topics
nav_order: 49
---

# GraphQL

## What You Will Learn
- How GraphQL differs from REST APIs
- How queries, mutations, and subscriptions work
- How introspection can be used to discover the API schema
- Common GraphQL security vulnerabilities

## What Is It?

**GraphQL** is a query language for APIs. Unlike REST where each endpoint returns a fixed structure, GraphQL lets the client request exactly the data it needs. The client controls the shape of the response.

GraphQL has a single endpoint (usually `/graphql`) and all operations are sent as POST requests.

## Why It Matters

GraphQL is increasingly used in modern web applications. Its flexibility introduces security issues:
- Introspection can expose the entire schema to attackers
- Overly permissive resolvers can leak sensitive data
- Batching attacks can bypass rate limiting
- Injection vulnerabilities still apply

## Key Concepts

### Three Operation Types

GraphQL schemas can be manipulated using three types of operations:

| Operation | Description |
|-----------|-------------|
| **Query** | Read data — similar to GET in REST |
| **Mutation** | Add, change, or remove data — similar to POST/PUT/DELETE |
| **Subscription** | Set up a persistent connection — server pushes data to client in real time |

## Queries

```graphql
# Fetch all products
query {
    products {
        id
        name
        published
    }
}
```

```graphql
# Fetch product with id 5
query {
    product(id: 5) {
        id
        name
        published
    }
}
```

## Mutations

```graphql
mutation {
    createProduct(name: "Flamin' Cocktail Glasses", published: true) {
        id
        name
        listed
    }
}
```

## Introspection

Introspection helps you understand how to interact with a GraphQL API. It returns the full schema — all types, queries, mutations, and fields.

```graphql
# Introspection probe — check if introspection is enabled
{
    "query": "{__schema{queryType{name}}}"
}
```

```graphql
# Full introspection query
query IntrospectionQuery {
    __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
            kind
            name
            fields(includeDeprecated: true) {
                name
                type {
                    kind
                    name
                    ofType { kind name }
                }
            }
        }
    }
}
```

### Using Introspection for Recon

If introspection is enabled, an attacker can map the entire API:

```bash
# Use graphql-voyager or InQL Burp plugin to visualize the schema
# Or use clairvoyance to guess the schema even without introspection
```

## Common GraphQL Vulnerabilities

### 1. Introspection Enabled in Production

If introspection is not disabled, attackers can discover all fields — including hidden admin fields.

### 2. Injection

GraphQL resolvers that pass user input to databases can be vulnerable to SQL injection or NoSQL injection:

```graphql
# Malicious query if resolver passes name directly to SQL
query {
    user(name: "' OR '1'='1") {
        id
        email
        password
    }
}
```

### 3. Batching Attacks

GraphQL allows sending multiple queries in one request. This bypasses rate limiting:

```json
[
  {"query": "mutation { login(user: \"admin\", pass: \"pass1\") }"},
  {"query": "mutation { login(user: \"admin\", pass: \"pass2\") }"},
  {"query": "mutation { login(user: \"admin\", pass: \"pass3\") }"}
]
```

### 4. Excessive Data Exposure

Resolvers that return entire objects when only part of the data is needed can expose sensitive fields.

## Security Testing Checklist

```bash
# Check if introspection is enabled
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{queryType{name}}}"}' | jq .

# Try accessing admin fields
# Try deeply nested queries (DoS via query depth)
# Try batched queries (rate limit bypass)
# Try SQL/NoSQL injection in string arguments
```

## Resources

- [PortSwigger — GraphQL API Vulnerabilities](https://portswigger.net/web-security/graphql)
- [HackTricks — GraphQL Attacks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql)
- [InQL — Burp Suite GraphQL Plugin](https://github.com/doyensec/inql)
- [GraphQL Security Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
