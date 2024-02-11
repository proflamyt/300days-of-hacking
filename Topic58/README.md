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
return <div> Hello The website is :, {decodeURIComponent(document.location)}</div>
}
}
```
Will be transcribed to 

```js
class HelloWorld extends React.Component {
render() {
return React.creteElement (
  type: 'div'
  props: null
  [decodeURIComponent(document.location)]
    )
}
}
```
where :

type represents the tag name 
props is the list of attributes 
children contains the child node(s) of the element



## ways to achieve xss 

### Injecting the props
