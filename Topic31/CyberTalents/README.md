# Reverse Engineering


Reversed Binary 

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+1Ch] [rbp-4h]

  if ( argc > 1 )
  {
    v4 = check_password(argv[1]);
    if ( v4 == -1 )
    {
      puts("Wrong password: at least look at disassembly");
      return 2;
    }
    else if ( v4 == -2 )
    {
      puts("Wrong password: hint, it's a matrix");
      return 3;
    }
    else
    {
      if ( !v4 )
      {
        puts("Congratulations!!!");
        print_password(argv[1]);
      }
      return 0;
    }
  }
  else
  {
    printf("Usage: %s <password>\n", *argv);
    return 1;
  }
}
```

Decompiled check_password

```c
__int64 __fastcall check_password(const char *a1)
{
  int i; // [rsp+10h] [rbp-30h]
  int j; // [rsp+14h] [rbp-2Ch]
  int v4; // [rsp+18h] [rbp-28h]
  int k; // [rsp+1Ch] [rbp-24h]
  char *v6; // [rsp+20h] [rbp-20h]
  char v7; // [rsp+28h] [rbp-18h]
  unsigned __int64 v8; // [rsp+38h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  v6 = (char *)'{1\x15Q:\x1D\bO';
  v7 = 114;
  if ( strlen(a1) != 9 )
    return 0xFFFFFFFFLL;
  for ( i = 0; i <= 2; ++i )
  {
    for ( j = 0; j <= 2; ++j )
    {
      v4 = 0;
      for ( k = 0; k <= 2; ++k )
        v4 = (a1[3 * k + j] * *((char *)&v6 + 3 * i + k) + v4) % 127;
      if ( i == j )
      {
        if ( v4 != 1 )
          return 0xFFFFFFFELL;
      }
      else if ( v4 )
      {
        return 0xFFFFFFFELL;
      }
    }
  }
  return 0;
}
```


### Solving check password with z3

```py
#!/usr/bin/env python3
"""
This code solves for the input that makes the function return 0.

The function performs matrix multiplication mod 127 and checks if the result
is the identity matrix. This means we need to find the modular inverse of the
given 3x3 matrix.
"""

# ============================================================================
# SOLUTION 1: Using Z3 (Fast and Simple)
# ============================================================================
from z3 import *

def solve_with_z3():
    print("=" * 70)
    print("SOLVING WITH Z3")
    print("=" * 70)
    
    # The given matrix (buf)
    buf = [79, 8, 29, 58, 81, 21, 49, 123, 114]
    
    # Create Z3 variables for param_1 (9 bytes)
    param_1 = [Int(f'p{i}') for i in range(9)]
    
    solver = Solver()
    
    # Constraint: all bytes must be printable ASCII (or at least valid bytes)
    for p in param_1:
        solver.add(p >= 0, p <= 127)
    
    # Matrix multiplication: buf * param_1 should equal identity matrix (mod 127)
    # For each output position (i, j):
    for i in range(3):
        for j in range(3):
            # Compute dot product of row i of buf with column j of param_1
            result = Sum([buf[k + i * 3] * param_1[j + k * 3] for k in range(3)])
            
            if i == j:
                # Diagonal elements should be 1 (mod 127)
                solver.add(result % 127 == 1)
            else:
                # Off-diagonal elements should be 0 (mod 127)
                solver.add(result % 127 == 0)
    
    print("Solving constraints...")
    if solver.check() == sat:
        model = solver.model()
        solution = [model[p].as_long() for p in param_1]
        
        print("\n✓ Solution found!")
        print(f"Bytes: {solution}")
        print(f"Hex:   {' '.join(f'{b:02x}' for b in solution)}")
        print(f"String: {bytes(solution)}")
        
        # Verify the solution
        verify_solution(buf, solution)
        return solution
    else:
        print("✗ No solution found")
        return None


def verify_solution(buf, param_1):
    """Verify that the solution produces the identity matrix mod 127"""
    print("\nVerifying solution:")
    for i in range(3):
        for j in range(3):
            result = sum(buf[k + i * 3] * param_1[j + k * 3] for k in range(3)) % 127
            expected = 1 if i == j else 0
            status = "✓" if result == expected else "✗"
            print(f"  [{i},{j}]: {result} (expected {expected}) {status}")


solve_with_z3()
```
