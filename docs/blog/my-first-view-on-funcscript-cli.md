---
title: "My First View on FuncScript CLI"
date: "2025-12-17"
description: "A beginner's exploration of fs-cli, the FuncScript command line interface. Lessons learned about quoting, argument handling, string types, and number limits when working with this JSON-with-superpowers expression language."
keywords: "FuncScript, fs-cli, CLI, command line, JSON, expression language, JavaScript, programming, REPL, npm, npx, BigInteger, number limits"
author: "Esubalew Chekol"
tags: ["FuncScript", "CLI", "Tutorial", "Programming", "JSON"]
og:title: "My First View on FuncScript CLI"
og:description: "Lessons learned from exploring fs-cli - quoting rules, argument handling, string type quirks, and number limits"
og:image: "/blog/og-my-first-view-on.png"
og:type: "article"
---

> FuncScript is a superset of JSON that lets you promote property values into expressions. Instead of static literals, `{ x: 1 + 2; }` is perfectly legal. It keeps JSON's predictability while gaining a concise expression language.

---

## What is FuncScript?

[FuncScript](https://www.funcscript.org/) is a superset of JSON that lets you promote property values into expressions. Instead of static literals, `{ x: 1 + 2; }` is perfectly legal. It keeps JSON's predictability while gaining a concise expression language. The [fs-cli](https://www.funcscript.org/developers/fs-cli/) is a lightweight Node.js command line interface that wraps the FuncScript runtime. There's also [FuncDraw](https://www.funcdraw.app/), a UI tool built using FuncScript.

This article documents my first experience with `fs-cli`. Note that these observations were made on a specific version of the tool and may not apply to future updates. Think of this as field notes from a curious explorer.

---

## What is the lesson I took

Well most of the issues seem to have a workaround: using `""` is the preferred way of doing FuncScript. Instead of:

```bash
npx fs-cli 3 + 'cool'
```

I will do:

```bash
npx fs-cli "3 + 'cool'"
```

And also:

```bash
npx fs-cli "'cool' + 4"
```

---

## I should not be confused with things in quotes

When we come to most programming languages, if not all, things in `""` means they are string literals. But here fs-cli expects one argument and if we have more than that, either that is going to be rejected or fs-cli panics.

So if we have `npx fs-cli "4 + 3"`, the `"4 + 3"` is not a string. It is the expression `4 + 3`. Here `" "` is being used to define the expression. It is like entering in Python REPL<sup>1</sup> and executing `4 + 4`:

```python
>>> 4 + 3
7
```

As for other languages like Python, string concatenation works naturally:

```python
>>> "Hello" + "Hello"
'HelloHello'
```

We can do this in fs-cli but a little bit differently. Instead of separately treating the operands, we quote everything in `""`:

```bash
npx fs-cli "'Hello' + 'Hello'"
# Type: String
# Value: "HelloHello"
```

The reason we are not doing something like Python is because in fs-cli we are talking with the shell, not only with fs-cli. In Python, in the above example, we are in Python's world where everything is in Python's environment.

---

## Fs-cli is a one argument tool

fs-cli expects one argument. If we don't respect that, results are going to be unexpected. As I mentioned in the section above, it is recommended that we use quotes when passing that argument.

It first looks like we can ignore quotes if we are passing a valid data type, and this works fine for most of the types:

```bash
npx fs-cli 3
# Type: Integer
# Value: 3

npx fs-cli 3.3
# Type: Float
# Value: 3.3

npx fs-cli true
# Type: Boolean
# Value: true

npx fs-cli "{}"
# Type: KeyValueCollection
# Value: {}
```

But the issue I discovered is this breaks sometimes or on some Types:

```bash
npx fs-cli []
# zsh: no matches found: []
```

Wrapping this in quotes solved the issue:

```bash
npx fs-cli "[]"
# Type: List
# Value: []
```

> Don't do things unquoted. Or make sure you know which behavior results in the action you executed.

---

## Data type String is wronged

Because of the fact that things are naturally expected to be defined in `""`, strings are hard to appear.

`npx fs-cli "3"` is interpreted as Integer and `npx fs-cli "true"` is interpreted as a Boolean and `npx fs-cli "trued"` as Null Type.

But fortunately this is more like a joke than a real issue. If we want to get a string, we need to define a string like `"true"`. We can do that by defining it like `npx fs-cli "'true'"` or we can escape the character we want to use with double quotes:

```bash
npx fs-cli "'38934'"
# Type: String
# Value: "38934"
```

---

## Numbers are limited so take care

If I try an extremely large number it will break or maybe panic. I'll use [run](https://run.esubalew.dev/)<sup>2</sup> to compare with Python. This means if we are not careful, mathematical operations may lead to the FuncScript limit and cause hidden bugs.

It is true that unlike the reality of the world which says numbers are unlimited (since the term infinity), they are limited when it comes to the programming world. We have two types of limits about how large the number we can write in a computer: **physical limit** and **implementation limit**. The former is the limit of our machine's RAM and the latter is the limit set by the implementation of the underlying programming languages we use.

```bash
# Python handles large numbers fine
run py "print(1000000000000000000 * 1000)"
# 1000000000000000000000

# fs-cli works up to a point
npx fs-cli "1000000000000000000 * 1000"
# Type: BigInteger
# Value: "1000000000000000000000"

# But then fails
npx fs-cli "1000000000000000000 * 10000000000000000000000000"
# Failed to parse expression
```

### Range limits

The highest limit of using `Range` is around `Range(0, 10000000)`. If we add a single zero, it will break and memory allocation fails.

### Number literal limits

When it comes to just calling a number:

```bash
npx fs-cli "1000000000000000000"
# Type: BigInteger
# Value: "1000000000000000000"

npx fs-cli "10000000000000000000"
# Failed to parse expression
```

The error message is misleading - "Failed to parse expression" doesn't tell you that you've hit a number limit.

---

## Conclusion

fs-cli is a powerful tool for working with FuncScript expressions from the command line. The key takeaways:

1. **Always quote your expressions** - Use `""` to wrap your FuncScript code
2. **Be aware of type inference** - Numbers and booleans are parsed as their types, not strings
3. **Watch out for number limits** - Large numbers may fail silently or with misleading errors
4. **Understand shell interaction** - fs-cli operates within your shell's constraints

---

> Want to read this in another format? [Read on CS](/cs/my-first-view-on-funcscript-cli)

---

<sup>1</sup> A read–eval–print loop (REPL), also termed an interactive toplevel or language shell, is a simple interactive computer programming environment that takes single user inputs, executes them, and returns the result to the user. [Read–eval–print loop](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)

<sup>2</sup> run is a universal multi-language runner and smart REPL written in Rust. [run](https://run.esubalew.dev/)
