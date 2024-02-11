# XSS In React 

### React Component

They act like functions, take in props as input and return react elements .

React elements are created by components by using the `createElement()` function , it takes in 3 argument , a string and two arrays

```js
React.createElement(
type,
[props],
[...children]
)
```

The React component generates this function by suppling it arguments based on the content of its return statement

For Example :

```js
class HelloWorld extends React.Component {
render() {
return <p title=About  > Hello The website is :, {decodeURIComponent(document.location)}</p>
}
}
```
Will be transcribed to 

```js
class HelloWorld extends React.Component {
render() {
return React.creteElement (
  type: 'p'
  props: {title:'About'}
  [ "Hello The website is :",decodeURIComponent(document.location)]
    )
}
}
```
where :

*type* represents the tag name 
*props* is the list of attributes 
*children* contains the child node(s) of the element



## ways to achieve xss 

### Injecting the props

An object of an attacker input ending up into props could lead to xss

```js
render() {
	attackerProps = JSON.parse(attackerInput)
 	return  <div attackerProps> </div>
}

```
### If developer uses dangerouslySetInnerHTML prop with attacker controlled input

```js
<div dangerouslySetInnerHTML={attackerInput} />
```

### Attacker Input ending directly In tag href and formaction

```js
<a href={attackerInput}>
```

As function argument

```js
fn = new Function("attackerInput")
fn()
```


If you can control the type and children and/or the props it is possible to get an xss on reactjs

