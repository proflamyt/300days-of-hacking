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

```graphql

  #Full introspection query

    query IntrospectionQuery {
        __schema {
            queryType {
                name
            }
            mutationType {
                name
            }
            subscriptionType {
                name
            }
            types {
             ...FullType
            }
            directives {
                name
                description
                args {
                    ...InputValue
            }
            onOperation  #Often needs to be deleted to run query
            onFragment   #Often needs to be deleted to run query
            onField      #Often needs to be deleted to run query
            }
        }
    }

    fragment FullType on __Type {
        kind
        name
        description
        fields(includeDeprecated: true) {
            name
            description
            args {
                ...InputValue
            }
            type {
                ...TypeRef
            }
            isDeprecated
            deprecationReason
        }
        inputFields {
            ...InputValue
        }
        interfaces {
            ...TypeRef
        }
        enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
        }
        possibleTypes {
            ...TypeRef
        }
    }

    fragment InputValue on __InputValue {
        name
        description
        type {
            ...TypeRef
        }
        defaultValue
    }

    fragment TypeRef on __Type {
        kind
        name
        ofType {
            kind
            name
            ofType {
                kind
                name
                ofType {
                    kind
                    name
                }
            }
        }
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
