## SAGE MATH

Solving

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

```
```


