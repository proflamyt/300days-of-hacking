# Prototype Polution 

## Javascript Objects

### Object Literal

```javascript

var person = {
    name: "ola",
    home: "lagos"
};

```


### Constructor Function:

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


### Object Create

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


### Prototype

```javascript
person.prototype.age = 12;

if (person1 instanceof person) console.log(person1.age);
```


### Prototype Chain

```javascript

if (person1 instanceof person && person2 instanceof person) console.log(person1.__proto__ === person2.__proto__);

````


### Poluting All Object Prototype

```javascript

person1.__proto__.__proto__.new = 'poluted';

ola = {}

ola.new === 'poluted';

```

### Polution Scenario in Applications

#### Object.assign

```javascript

var input = '{"name":"olamide", "__proto__": {"isAdmin":true}}';

var source = JSON.parse(input)

let vuln = {}

Object.assign(vuln, source)

vuln.isAdmin === true

```