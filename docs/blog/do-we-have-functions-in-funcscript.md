---
title: "Do We Have Functions in FuncScript?"
date: "2025-12-19"
description: "Exploring whether FuncScript has functions in the traditional programming sense. A deep dive into lambda expressions, reusable code blocks, and how to think about functions in a JSON-with-superpowers world."
keywords: "FuncScript, fs-cli, functions, lambda, JSON, expression language, functional programming, KeyValueCollection, map, Range"
author: "Esubalew Chekol"
tags: ["FuncScript", "Functions", "Lambda", "Programming", "JSON", "Tutorial"]
og:title: "Do We Have Functions in FuncScript?"
og:description: "Exploring functions and lambda expressions in FuncScript - from simple returns to complex transformations"
og:image: "/blog/og-do-we-have-functions.png"
og:type: "article"
---

> FuncScript is a superset of JSON that lets you promote property values into expressions. Instead of static literals, `{ x: 1 + 2; }` is perfectly legal. You can execute FuncScript using fs-cli or experiment in FuncScript Studio.

---

## What is FuncScript?

[FuncScript](https://www.funcscript.org/)<sup>1</sup> is a superset of JSON that lets you promote property values into expressions. Instead of static literals, `{ x: 1 + 2; }` is perfectly legal. You can execute FuncScript using [fs-cli](https://www.funcscript.org/developers/fs-cli/)<sup>2</sup> (the command line interface) or experiment in [FuncScript Studio](https://www.funcscript.org/fsstudio/)<sup>3</sup> (a web-based environment).

This article assumes you have basic knowledge of FuncScript. If you're new to it, I recommend starting with the [official documentation](https://www.funcscript.org/) or reading my previous article on [fs-cli basics](/blog/my-first-view-on-funcscript-cli).

---

## Do functions exist in FuncScript?

Well, I don't know if there is a "function" in FuncScript in the modern programming language sense.

A function is nothing but a block of code that does something specific. The main ideas are: (1) we can have separated concerns where we do tasks step by step, and (2) we can make code reusable. Instead of hardcoding everything, we can have a block of code dedicated to a specific task.

We don't have a way of creating a function in the format traditional programming languages use, but we can achieve it in a way that looks like JSON. Please remember that FuncScript is nothing but a powerful JSON.

---

## Everything in braces is a function

To make things easier, let's assume FuncScript code is JSON, and the JSON itself is a function. So let's say everything in `{}` is a function where the key is the name of the function and the value is the return value.

To be more specific, if we have a FuncScript code `{a: 10;}`, that means `a` is the name of the function and `10` is what the function `a` returns.

Please note that in reality everything with `{}` is called `KeyValueCollection`, but we must pretend it's not for this exploration.

Here's how we can run this in fs-cli:

```bash
fs-cli '{a: 10}'
# Type: KeyValueCollection
# Value: { "a": 10 }
```

From here on, I'll show FuncScript code and output separately for clarity. You can run these in fs-cli or FuncScript Studio.

Let's achieve this same thing in Rust to make a connection with traditional programming languages. I'll use [run](https://run.esubalew.dev/)<sup>4</sup> for simplicity:

```rust
rust>>> fn ten() -> i32 { 10 }
rust>>> ten()
10
```

That's essentially what we just did in FuncScript - or even simpler!

To make it cleaner and return only `10` instead of the whole `KeyValueCollection`, we use `eval`:

```javascript
{
  a: 10;
  eval a;
}
// Output: 10
```

So that's the most basic function in FuncScript.

---

## But where are the parentheses?

You might ask: where is the `()` - the parameter symbol that can either be empty or hold some parameters? Like we see in Rust: `fn ten() -> i32 { 10 }`.

Let's first look at Python:

```python
>>> def say_hello(): return 'Hello'
>>> say_hello()
'Hello'
```

Now let's adapt this in FuncScript - maybe in an even simpler way than Python:

```javascript
{
  say_hello: () => "hello";
  eval say_hello();
}
// Output: "hello"
```

If we want to make it a two-step process, we can remove the `eval` and see the full structure:

```javascript
{
  say_hello: () => "hello";
  result: say_hello();
}
// Output: { say_hello: "[Function]", result: "hello" }
```

---

## Functions with parameters

What if we have parameters, like printing "Hello, name" where `name` is an argument the function receives?

In Python:

```python
>>> name = "Esubalew"
>>> def say_hello(name): return "hello " + name
>>> say_hello(name)
'hello Esubalew'
```

Now let's do the exact same thing in FuncScript:

```javascript
{
  name: "Esubalew";
  say_hello: (name) => "Hello " + name;
  eval say_hello();
}
// Output: "Hello Esubalew"
```

Or if we don't have the argument ready and want to pass it at runtime:

```javascript
{
  say_hello: (name) => "Hello " + name;
  eval say_hello("Augustus");
}
// Output: "Hello Augustus"
```

---

## Complex transformations with functions

FuncScript can handle deeper and more complex tasks. Let's assume we want to multiply a range of numbers with some rate and write a function that does that:

```javascript
{
  rate: 1/100;
  numbers: Range(1, 2);
  multiply: (number) => {
    old: number;
    newer: number * rate;
  };
  multiplied: numbers map (number) => multiply(number);
  eval multiplied;
}
// Output: [{ old: 1, newer: 0.01 }, { old: 2, newer: 0.02 }]
```

Remove `eval` and FuncScript shows the whole structure:

```javascript
{
  rate: 1/100;
  numbers: Range(1, 2);
  multiply: (number) => {
    old: number;
    newer: number * rate;
  };
  multiplied: numbers map (number) => multiply(number);
}
// Output: { rate: 0.01, numbers: [1, 2], multiply: "[Function]", multiplied: [...] }
```

The `eval` keyword can also help us extract specific values:

```javascript
{
  rate: 1/100;
  numbers: Range(1, 2);
  multiply: (number) => {
    old: number;
    newer: number * rate;
  };
  multiplied: numbers map (number) => multiply(number);
  eval multiplied[0].newer;
}
// Output: 0.01
```

---

## Simplifying step by step

If we want to make the function more flexible, we can pass parameters instead of using external bindings:

```javascript
{
  multiply: (number, rate) => {
    old: number;
    newer: number * rate;
  };
  multiplied: Range(1, 6) map (number) => multiply(number, 1/100);
  eval multiplied;
}
// Output: [{ old: 1, newer: 0.01 }, { old: 2, newer: 0.02 }, ...]
```

Or even shorter with inline lambdas:

```javascript
{
  multiplied: Range(1, 2) map (n) => {
    old: n;
    newer: n / 100;
  };
  eval multiplied;
}
// Output: [{ old: 1, newer: 0.01 }, { old: 2, newer: 0.02 }]
```

Or get rid of naming entirely and go fully inline:

```javascript
{
  eval Range(1, 2) map (n) => {
    old: n;
    newer: n / 100;
  };
}
// Output: [{ old: 1, newer: 0.01 }, { old: 2, newer: 0.02 }]
```

---

## Conclusion

So, do we have functions in FuncScript? Not in the traditional `function` or `def` keyword sense. But we absolutely have:

- **Lambda expressions**: `(param) => expression`
- **Named bindings**: Store lambdas as reusable values
- **Higher-order functions**: `map`, and other helpers that accept functions
- **Closures**: Lambdas can reference outer bindings like `rate`

FuncScript takes a different approach. Instead of defining functions as separate entities, everything lives inside the JSON-like structure. Your "functions" are just properties that happen to hold lambdas. This makes FuncScript feel less like traditional programming and more like building reactive, self-computing documents.

The beauty is in the simplicity: what starts as `{a: 10}` can evolve into complex transformations while maintaining that familiar JSON shape.

---

> Want to read this in another format? [Read on CS](/cs/do-we-have-functions-in-funcscript)

---

<sup>1</sup> FuncScript is a superset of JSON that overlaps with much of JavaScript syntax yet introduces its own twists. [FuncScript](https://www.funcscript.org/)

<sup>2</sup> fs-cli is the command line interface for executing FuncScript expressions. [fs-cli](https://www.funcscript.org/developers/fs-cli/)

<sup>3</sup> FuncScript Studio is a web-based environment for experimenting with FuncScript. [FuncScript Studio](https://www.funcscript.org/fsstudio/)

<sup>4</sup> run is a universal multi-language runner and smart REPL written in Rust that lets you execute code in 25+ languages from the command line. [run](https://run.esubalew.dev/)
