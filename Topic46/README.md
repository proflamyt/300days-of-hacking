---
title: "Prototype Pollution"
topic: "prototype-pollution"
tags: [prototype-pollution, javascript, web-security, xss, object-prototype, nodejs]
difficulty: intermediate
day: 46
layout: default
parent: Topics
nav_order: 46
---

# Prototype Pollution

## What You Will Learn
- What JavaScript prototypes are and how the prototype chain works
- How prototype pollution works as a vulnerability
- How Object.assign and JSON.parse can be exploited
- How to identify and prevent prototype pollution

## What Is It?

Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects.

Since JavaScript objects inherit from `Object.prototype`, polluting it affects every object in the application.

## Why It Matters

Prototype pollution can lead to:
- Property injection that bypasses security checks
- Denial of service (breaking application logic)
- Remote code execution in Node.js applications
- XSS when polluted properties reach the DOM

## JavaScript Objects

### Object Literal

```javascript
var person = {
    name: "ola",
    home: "lagos"
};
```

### Constructor Function

```javascript
person = function(name, place) {
    this.name = name;
    this.home = place;
}

person1 = new person("ola", "lagos");
```

### ES6 Class

```javascript
class Person {
  constructor(name, place) {
    this.name = name;
    this.home = place;
  }

  method() {
    // Method implementation
  }
}

const obj = new Person("ola", "lagos");
```

### Object.create

```javascript
const person = {
  method() {
    // Method implementation
  }
};

const person1 = Object.create(person);
person1.name = "ola";
person1.home = "lagos";
```

### Function Factory

```javascript
function createPerson(name, place) {
  return {
    name: name,
    home: place,
    method: function() {
      // Method implementation
    }
  };
}

const person1 = createPerson("ola", "lagos");
```

## The Prototype Chain

### Accessing Prototypes

```javascript
person.prototype.age = 12;

if (person1 instanceof person) console.log(person1.age);
```

### Prototype Chain Lookup

```javascript
if (person1 instanceof person && person2 instanceof person) {
  console.log(person1.__proto__ === person2.__proto__); // true
}
```

## Prototype Pollution in Practice

### Polluting All Object Prototypes

```javascript
person1.__proto__.__proto__.new = 'polluted';

ola = {};
ola.new === 'polluted'; // true — every object now has this property
```

### Pollution via Object.assign

```javascript
var input = '{"name":"olamide", "__proto__": {"isAdmin":true}}';

var source = JSON.parse(input);

let vuln = {};

Object.assign(vuln, source);

vuln.isAdmin === true; // true — admin check bypassed!
```

### Server-Side (Node.js) Impact

If an attacker can pollute `Object.prototype`, properties that do not exist on an object will now return the attacker's value:

```javascript
// Before pollution:
let user = {};
user.isAdmin; // undefined

// After prototype pollution:
Object.prototype.isAdmin = true;
user.isAdmin; // true — even though user object was not modified
```

This can bypass `if (user.isAdmin)` checks in authentication code.

### RCE via Prototype Pollution in Node.js

Some Node.js libraries use polluted properties in ways that lead to code execution, for example through `child_process.spawn` options that get merged from a polluted prototype.

## Prevention

```javascript
// Use Object.create(null) for dictionaries — no prototype
const safe = Object.create(null);

// Block __proto__ in merge functions
function safeAssign(target, source) {
    for (let key of Object.keys(source)) {
        if (key === '__proto__' || key === 'constructor') continue;
        target[key] = source[key];
    }
}

// Use JSON schema validation on user input
// Use Object.freeze(Object.prototype) in testing
```

## Resources

- [PortSwigger — Prototype Pollution](https://portswigger.net/web-security/prototype-pollution)
- [TryHackMe — Prototype Pollution](https://tryhackme.com/)
- [HackTricks — Prototype Pollution](https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-prototype-pollution)
- [Research — Prototype Pollution in Popular Libraries](https://snyk.io/blog/prototype-pollution-high-severity-vulnerability-found-in-19-npm-packages/)
