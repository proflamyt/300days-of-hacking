---
title: "Rust"
topic: "rust"
tags: [rust, memory-safety, systems-programming, ownership, borrow-checker]
difficulty: intermediate
day: 83
layout: default
parent: Topics
nav_order: 83
---

# Rust

## What You Will Learn
- What Rust is and why it matters for systems security
- How ownership and borrowing prevent memory safety bugs
- Key Rust syntax for security-relevant code
- How Rust is used in security tooling

## What Is It?

**Rust** is a systems programming language focused on **memory safety** and **performance**. Unlike C/C++, Rust eliminates entire classes of memory bugs at compile time — no buffer overflows, use-after-free, or null pointer dereferences by default.

Rust is increasingly used in security tooling, operating system components, and exploit mitigation research.

## Why It Matters

- Most CVEs in C/C++ projects are memory safety bugs — Rust prevents these by design
- The Rust compiler acts as a security reviewer — it rejects unsafe code patterns at compile time
- Many new security tools (fuzzing engines, network proxies) are written in Rust
- Android and Linux kernel now include Rust code for security-critical components

## Key Concepts

### Ownership

Every value in Rust has exactly one **owner**. When the owner goes out of scope, the value is dropped (freed). This eliminates double-free and use-after-free bugs.

```rust
let s = String::from("hello");   // s owns the string
let s2 = s;                       // ownership moves to s2
// println!("{}", s);             // ERROR: s no longer owns the string
println!("{}", s2);               // OK
```

### Borrowing and References

Instead of transferring ownership, you can **borrow** a value with a reference:

```rust
let s = String::from("hello");

let len = calculate_length(&s);  // borrow s (pass reference)
println!("{}: {}", s, len);       // s still valid

fn calculate_length(s: &str) -> usize {
    s.len()  // read-only borrow
}
```

### Mutable References

`mut` makes a variable changeable. `&mut` passes a mutable reference:

```rust
let mut a = 3;
// &mut = "Here, you can change this."
// &    = "You can only look, not touch."

fn change(x: &mut i32) {
    *x += 1;
}
change(&mut a);
```

Rust enforces: **only one mutable reference** to a value at a time. This prevents data races.

### No Null Pointers

Rust has no null pointers. Instead it uses `Option<T>`:

```rust
let name: Option<&str> = Some("Alice");
let empty: Option<&str> = None;

match name {
    Some(n) => println!("Name: {}", n),
    None    => println!("No name"),
}
```

### Error Handling

No exceptions in Rust. Functions return `Result<T, E>`:

```rust
use std::fs::File;

fn open_file() -> Result<File, std::io::Error> {
    File::open("secret.txt")
}

match open_file() {
    Ok(file)  => println!("Opened file"),
    Err(e)    => println!("Error: {}", e),
}
```

## Memory Safety Without a GC

Rust achieves memory safety without a garbage collector:

| Bug | C/C++ | Rust |
|-----|-------|------|
| Buffer overflow | Possible | Compile-time bounds checking |
| Use-after-free | Possible | Compiler rejects invalid lifetimes |
| Double-free | Possible | Ownership prevents it |
| Null pointer deref | Possible | No null — use `Option` |
| Data race | Possible | Compiler rejects unsafe concurrent access |

## Unsafe Rust

Sometimes you need raw pointer access (for FFI or low-level code). Rust provides an `unsafe` block:

```rust
let raw_ptr: *const i32 = &42;
unsafe {
    println!("{}", *raw_ptr);  // dereference raw pointer
}
```

Most security vulnerabilities in Rust code are in `unsafe` blocks.

## Rust Security Tools

- **cargo-audit**: Check dependencies for known CVEs
- **cargo-fuzz**: LibFuzzer integration for fuzzing Rust code
- **rustScan**: Fast port scanner written in Rust

```bash
# Install cargo-audit
cargo install cargo-audit

# Audit project dependencies
cargo audit

# Fuzz a function
cargo fuzz run fuzz_target
```

## Resources

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/)
- [Rust By Example](https://doc.rust-lang.org/rust-by-example/)
- [Rustlings — Practice Exercises](https://github.com/rust-lang/rustlings)
- [cargo-audit](https://github.com/RustSec/rustsec/tree/main/cargo-audit)
- [Memory Safety in Rust (Google)](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html)
