---
title: "Bridging Rust and Python: Building Python Extensions with PyO3"
date: "2025-09-24"
description: "Learn how to use Rust inside Python by creating Python extensions with PyO3 and maturin. We'll walk through setup, code examples, and practical use cases."
keywords: "PyO3, Rust Python bindings, maturin, Python extensions in Rust, Rust Python integration, speed up Python with Rust, cdylib, Rust tutorial, Python performance, Rust Python FFI"
author: "Esubalew Chekol"
tags: ["Rust", "Python", "PyO3", "maturin", "Tutorial"]
og:title: "Build Fast Python Extensions with Rust and PyO3"
og:description: "Complete guide to creating high-performance Python modules using Rust, PyO3, and maturin."
og:image: "blog/og-pyo3.png"
og:type: "article"
---

Rust and Python are a match made in heaven:  
- **Python** is flexible and has an amazing ecosystem.  
- **Rust** is fast, safe, and low-level.  

What if you could use **Rust’s performance** directly inside your Python programs? That’s exactly what [PyO3](https://github.com/PyO3/pyo3) lets you do.  

In this guide, we’ll build a Python extension in Rust that processes input events, translates text, and even converts **TOML** to **JSON**—all callable from Python.  

---

## Step 1: Project Setup

First, create a Rust library project:

```bash
cargo new --lib afrim_py
cd afrim_py
````

Update `Cargo.toml`:

```toml
[lib]
name = "afrim_py"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.21", features = ["extension-module"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
toml = "0.8"
pythonize = "0.21"
```

Install [maturin](https://github.com/PyO3/maturin) for packaging:

```bash
pip install maturin
```

---

## Step 2: Writing Rust Functions for Python

Let’s start with a simple Rust function exposed to Python.

```rust
use pyo3::prelude::*;
use toml;

/// Convert TOML to JSON and return it as a Python string.
#[pyfunction]
fn convert_toml_to_json(content: &str) -> PyResult<String> {
    let data: toml::Value = toml::from_str(content)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    Ok(serde_json::to_string(&data)?)
}
```

In `lib.rs`, register it as part of a Python module:

```rust
#[pymodule]
fn afrim_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_toml_to_json, m)?)?;
    Ok(())
}
```

---

## Step 3: Exposing Rust Structs as Python Classes

You can also expose Rust structs as Python classes. For example, here’s a `Preprocessor` with methods:

```rust
#[pyclass]
pub struct Preprocessor {
    buffer: String,
}

#[pymethods]
impl Preprocessor {
    #[new]
    fn new() -> Self {
        Self { buffer: String::new() }
    }

    fn process(&mut self, input: &str) {
        self.buffer.push_str(input);
    }

    fn get_buffer(&self) -> String {
        self.buffer.clone()
    }
}
```

Now Python can do:

```python
from afrim_py import Preprocessor

p = Preprocessor()
p.process("Hello")
print(p.get_buffer())  # "Hello"
```

---

## Step 4: Building and Installing

Run:

```bash
maturin develop
```

This builds your Rust code into a Python extension and installs it locally.

---

## Step 5: Using It in Python

Here’s a taste of what you can now do:

```python
from afrim_py import convert_toml_to_json, Preprocessor

print(convert_toml_to_json("[info]\nname = 'sample'"))
# {"info": {"name": "sample"}}

p = Preprocessor()
p.process("Rust ❤️ Python")
print(p.get_buffer())
# "Rust ❤️ Python"
```

---

## Why This Matters

* **Performance:** Rust handles heavy tasks much faster than pure Python.
* **Safety:** No segfaults or data races.
* **Integration:** You can extend existing Python libraries instead of rewriting them.

This approach is perfect for:

* Accelerating parsing, preprocessing, or machine learning pipelines.
* Reusing Rust libraries in Python apps.
* Building new Python modules powered by Rust.

---

## Final Thoughts

With **PyO3** and **maturin**, bridging Rust and Python is easier than ever.
You write safe, fast Rust code—and expose it directly as Python modules.

If you're building performance-critical Python tools, give this combo a try. It's like giving Python a **turbo engine** without losing its simplicity.

---

*Happy hacking with Rust & Python!*

```

---
