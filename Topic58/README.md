---
title: "XSS in React"
topic: "xss-react"
tags: [xss, react, javascript, frontend, dangerouslySetInnerHTML, web-security]
difficulty: intermediate
day: 58
layout: default
parent: Topics
nav_order: 58
---

# XSS in React

## What You Will Learn
- How React renders HTML and why it is mostly safe by default
- How React components can still be vulnerable to XSS
- The common patterns that introduce XSS in React apps
- How to avoid XSS when building React applications

## What Is It?

React is designed to prevent XSS by escaping output by default. But developers can bypass these protections — accidentally or intentionally — and introduce XSS vulnerabilities.

Understanding React's internal rendering model helps you find XSS in React applications.

## React Components

React components act like functions: they take **props** as input and return React elements.

React elements are created by components using the `createElement()` function, which takes three arguments:

```js
React.createElement(
    type,       // HTML tag or component
    [props],    // attributes
    [...children]  // child nodes
)
```

For example, this JSX:

```js
class HelloWorld extends React.Component {
    render() {
        return <p title="About">Hello, {decodeURIComponent(document.location)}</p>
    }
}
```

Becomes:

```js
class HelloWorld extends React.Component {
    render() {
        return React.createElement(
            'p',
            {title: 'About'},
            ["Hello, ", decodeURIComponent(document.location)]
        )
    }
}
```

Where:
- `type` = the tag name (`'p'`)
- `props` = list of attributes `{title: 'About'}`
- `children` = child node content

## Ways to Achieve XSS in React

### 1. Injecting into Props

If attacker-controlled input ends up in the `props` of a component, it can lead to XSS.

```js
render() {
    attackerProps = JSON.parse(attackerInput);
    return <div {...attackerProps} />;
}
```

If `attackerInput` is `{"dangerouslySetInnerHTML": {"__html": "<img src=x onerror=alert(1)>"}}`, the div renders with XSS.

### 2. dangerouslySetInnerHTML

The `dangerouslySetInnerHTML` prop renders raw HTML directly. It is React's explicit escape hatch — if you use it with attacker-controlled input, you have XSS.

```js
<div dangerouslySetInnerHTML={attackerInput} />
```

Never use `dangerouslySetInnerHTML` with unsanitized user input.

### 3. Attacker Input in href or formaction

React does not sanitize `javascript:` URLs in `href` attributes.

```js
<a href={attackerInput}>Click me</a>
```

If `attackerInput` is `javascript:alert(1)`, clicking the link executes JavaScript.

### 4. As a Function Argument

```js
fn = new Function("attackerInput");
fn();
```

`new Function()` is equivalent to `eval()`. Never pass user input to it.

### 5. eval()

```js
eval(attackerInput);
```

Classic — never use `eval()` with user data.

## Controlling type and children

If you can control the `type` argument (the HTML tag) and the `children` of `createElement()`, you may be able to inject XSS even without using `dangerouslySetInnerHTML`:

```js
React.createElement(attackerControlledType, {}, 'text');
// If attackerControlledType = "script", this renders a <script> tag
```

## Prevention

- Never use `dangerouslySetInnerHTML` with user input — if you must, sanitize with `DOMPurify`
- Validate URLs before using them in `href` — reject any URL starting with `javascript:`
- Never use `eval()`, `new Function()`, or `setTimeout(string, ...)` with user data
- Use Content Security Policy (CSP) headers as a defense-in-depth measure
- Treat `__html` in any prop as dangerous

```js
// Safe URL check
function isValidUrl(url) {
    return url.startsWith('https://') || url.startsWith('http://');
}
```

## Resources

- [PortSwigger — XSS in React](https://portswigger.net/web-security/cross-site-scripting)
- [Beyond XSS — Advanced Frontend Attacks](https://aszx87410.github.io/beyond-xss/en/)
- [React Docs — dangerouslySetInnerHTML](https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html)
- [DOMPurify — HTML Sanitization Library](https://github.com/cure53/DOMPurify)
- [TryHackMe — XSS](https://tryhackme.com/room/axss)
