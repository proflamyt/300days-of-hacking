## SAGE MATH

###  Single Variable (x)

$$
x + 2x^2 + x^3 = 100
$$

Using SageMath

Define X as variable in the domain of integer numbers and solve for x 

ZZ (domains of integer numbers)

```py
x =  var('x', domain=ZZ)
leq = x + 2*x**2 + x**3
sol = solve(leq == 100, x)
print(sol) # 4
```

To verify 

$$
4 + 2*(4^2) + (4)^3 = 100
$$

we can confirm with 

```py
leq(x=4) # 100
```


solving 

$$
x_0^4 - 150x_0^3 + 4389x_0^2 - 43000x_0 +131100 = 0
$$

sage 
```
x =  var('x', domain=ZZ)
leq = x**4 - 150*x**3 + 4389*x**2 - 43000*x + 131100
sol = solve(leq == 0, x)
sol
```


### Linear Equation 

#### Two Variables (x, y)

$$
x + y = 10
$$


```py
x = var('x', domain=ZZ)
y = var('y', domain=ZZ)
sol = solve(x+y==10, (x,y))
sol
```

Solution

$$
x = t_0, y = -t_0 + 10
$$

Say we have 2 equations

$$
x + y = 10, 
x=y
$$


Solution

```py
x = var('x', domain=ZZ)
y = var('y', domain=ZZ)
sol = solve([x+y==10, x==y], (x,y))
sol
```

#### Three Variables (x, y, z)

$$
\begin{cases}
2x + y = 15 \\
x + y + z = 20 \\
3z = 30
\end{cases}
$$


Solution

```py
x = var('x', domain=ZZ)
y = var('y', domain=ZZ)
z = var('z', domain=ZZ)
sol = solve([x + x + y == 15, z + z + z==30, x+y+z ==20], (x,y,z))
sol
```



## Matrix

### Inverse of matrix Sage math

$$
\begin{bmatrix}
0 & 2 & 0 & 0 \\
3 & 0 & 0 & 0 \\
0 & 0 & 5 & 0 \\
0 & 0 & 0 & 7 \\
\end{bmatrix}
$$


```py
A = matrix([[0,2,0,0], [3,0,0,0], [0,0,5,0], [0,0,0,7]])
A.inverse()
```
