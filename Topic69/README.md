# Frontend Vulnerabilities


## Google Chrome Dev

```js
debug(postMessage, 'argument[1] == "*"')
monitorEvents(window, 'message')
```


### Enable Override

- Open the Sources Tab.
- Enlarge to view Override Tab, Click Override
- Click Add Override Folder
- Select which directory you want to save your changes to.
- At the top of your viewport, click Allow to give DevTools read and write access to the directory.


```
url.searchParams

url.searchParams.get

url.searchParams.has

window.location.href

window.location.search

history.pushState

history.replaceState
```

### Conditional Breakpoint



reference : https://aszx87410.github.io/beyond-xss/en/