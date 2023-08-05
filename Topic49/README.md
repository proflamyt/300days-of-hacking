# GraphQL

 GraphQL schema can be manipulated using three types of operation: 
 - Queries are similar to get requests in REST API
- Mutations add, change, or remove data.
- Subscriptions  set up a permanent connection which a server can proactively push data to a client in the specified format

### QUery 

```graphql

    query {
        products {
            id
            name
            published
        }
    }
```

```graphql
# id 5
    query {
        product(id: 5) {
            id
            name
            published
        }
    }

```


#### INTROSPECTION

Introspection helps you to understand how you can interact with a GraphQL API

```graphql

#Introspection probe request

    {
        "query": "{__schema{queryType{name}}}"
    }

```


### Mutation

```graphql

    mutation {
        createProduct(name: "Flamin' Cocktail Glasses", published: true) {
            id
            name
            listed
        }
    }

```
