---
title: "Eval in FuncScript"
date: "2025-12-20"
description: "Understanding the eval keyword in FuncScript - how it helps you focus on results, avoid intermediate variables, and write cleaner expressions both inside and outside braces."
keywords: "FuncScript, fs-cli, eval, expression, JSON, functional programming, KeyValueCollection, Reduce, map, Range"
author: "Esubalew Chekol"
tags: ["FuncScript", "eval", "Tutorial", "Programming", "JSON"]
og:title: "Eval in FuncScript"
og:description: "Master the eval keyword in FuncScript to focus on results and write cleaner code"
og:image: "/blog/og-eval-in-funcscript.png"
og:type: "article"
---

> FuncScript is a superset of JSON that lets you promote property values into expressions. The `eval` keyword helps you focus on results and write cleaner code by avoiding intermediate variables.

---

## What is FuncScript?

[FuncScript](https://www.funcscript.org/)<sup>1</sup> is a superset of JSON that lets you promote property values into expressions. Instead of static literals, `{ x: 1 + 2; }` is perfectly legal. You can execute FuncScript using [fs-cli](https://www.funcscript.org/developers/fs-cli/)<sup>2</sup> (the command line interface) or experiment in [FuncScript Studio](https://www.funcscript.org/fsstudio/)<sup>3</sup> (a web-based environment).

This article assumes you have basic knowledge of FuncScript. If you're new to it, I recommend starting with the [official documentation](https://www.funcscript.org/) or reading my previous articles: [fs-cli basics](/blog/my-first-view-on-funcscript-cli) and [functions in FuncScript](/blog/do-we-have-functions-in-funcscript).

---

## What is eval?

Even though FuncScript code is typically written inside `{}`, it doesn't mean we can't do anything outside braces. If we have a REPL<sup>4</sup>-type environment like Python, Node, or Lua, we can execute simple code without worrying about wrapping everything in a file structure. It's similar to using [run](https://run.esubalew.dev/)<sup>5</sup> to do `4 + 5` in C or C++ without the main function.

So the following is also legal in FuncScript:

```bash
fs-cli '4 + 3'
# Type: Integer
# Value: 7
```

Keep in mind that you need to quote your argument with `""` or `''` for fs-cli, otherwise unexpected things will happen. For more about fs-cli syntax, please read [my first view on fs-cli](/blog/my-first-view-on-funcscript-cli).

---

## Two ways to run FuncScript

There are two main ways to run FuncScript: **FuncScript Studio** (a web-based editor) and **fs-cli** (command line interface).

The main difference is the method of input. In fs-cli, everything we call code must be passed as `fs-cli 'arg'` where `arg` is the code. Using quotes is a must (or at least recommended) because things like `fs-cli 4 + 4` will only read the first `4` and miss everything after the first argument.

```bash
# This is WRONG - fs-cli only sees "4"
fs-cli 4 + 4
# Type: Integer
# Value: 4

# This is CORRECT
fs-cli '4 + 4'
# Type: Integer
# Value: 8
```

This means `fs-cli eval 4 + 4` is an invalid expression. The solution is quoting it as `fs-cli 'eval 4 + 4'`.

In FuncScript Studio, `eval 4 + 4` works directly since it's an editor environment. You can access the playground at [funcscript.org/fsstudio](https://www.funcscript.org/fsstudio/).

---

## Eval with different types

As long as we follow the same format, we can use eval with any type:

```bash
fs-cli 'eval "Hello, Esubalew"'
# Type: String
# Value: "Hello, Esubalew"

fs-cli 'eval [3, 3]'
# Type: List
# Value: [3, 3]

fs-cli 'eval {}'
# Type: KeyValueCollection
# Value: {}

fs-cli 'eval {age: 10, name: "cool"}'
# Type: KeyValueCollection
# Value: { "age": 10, "name": "cool" }
```

The same applies in FuncScript Studio, except we don't use the outer quotes:

```javascript
eval {age: 10, name: "cool"}
// Output: { "age": 10, "name": "cool" }
```

---

## Eval with expressions inside braces

We can use eval inside `{}` to combine values:

```bash
fs-cli '{name: "Esubalew"; full: "Hello, " + name;}'
# Type: KeyValueCollection
# Value: { "name": "Esubalew", "full": "Hello, Esubalew" }

fs-cli '{a: 10; b: 20; sum: a + b;}'
# Type: KeyValueCollection
# Value: { "a": 10, "b": 20, "sum": 30 }
```

But what if we want to avoid the intermediate `sum` key and just evaluate to the sum directly?

---

## The problem with missing keys

Can we do something like this?

```javascript
fs-cli '{a: 10; b: 20; a + b}'
```

Will this result in `30`? **No, it will not.** The `{}` object violates the key: value syntax because `a + b` is without a key.

```bash
fs-cli '{a: 10; b: 20; a + b}'
# Failed to parse expression
```

This is where **eval** becomes powerful. By taking eval inside `{}`, we can return the result directly:

```bash
fs-cli '{a: 10; b: 20; eval a + b;}'
# Type: Integer
# Value: 30
```

---

## Focusing on results with eval

Consider this example where we want to transform a list:

```javascript
{
  doubled: [1, 2] map (number) => number * 2;
}
// Output: { "doubled": [2, 4] }
```

But what if we just want the result without the `doubled` key?

```javascript
{
  eval [1, 2] map (number) => number * 2;
}
// Output: [2, 4]
```

We can also access specific elements:

```bash
fs-cli '{number: [1, 2] map (n) => n * 2; eval number[0]}'
# Type: Integer
# Value: 2
```

---

## A practical example

Let's revisit an example from my [previous article](/blog/do-we-have-functions-in-funcscript):

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
```

This returns everything including intermediate steps:

```javascript
{
  rate: 0.01,
  numbers: [1, 2],
  multiply: "[Function]",
  multiplied: [{ old: 1, newer: 0.01 }, { old: 2, newer: 0.02 }],
}
```

Instead of showing all the intermediate variables like `rate` and the function, we can focus on the result:

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

We can go even further and focus on a very specific result:

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

## When eval has no effect

Please note that using eval on a value that's already a direct return is useless:

```bash
fs-cli 'range(1, 10)'
# Type: List
# Value: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fs-cli 'range(1, 10)[0]'
# Type: Integer
# Value: 1

fs-cli 'eval range(1, 10)[0]'
# Type: Integer
# Value: 1
```

Here adding eval is of no effect. Think of it like doing `eval 1` which just returns `1`.

---

## Eval with functions

If we have a function (what I call a "key function" - learn more at [my functions article](/blog/do-we-have-functions-in-funcscript)) that returns a multiplied value:

```javascript
{
  multi: (x) => x * 2;
}
// Output: { "multi": "[Function]" }
```

We can use it by expanding:

```javascript
{
  multi: (x) => x * 2;
  play: multi(2);
}
// Output: { "multi": "[Function]", "play": 4 }
```

But what if we just want a function that returns a number? This time eval is very important:

```bash
fs-cli '{multi: (x) => x * 2; eval multi(2)}'
# Type: Integer
# Value: 4
```

---

## Eval with Reduce

Let's use eval with `Reduce`, a powerful built-in function. Reduce takes these parameters:

- `list` - the list to reduce
- `lambda` - a function that takes `(currentState, currentValue)` and returns the new state
- `initialValue` - the starting value

Let's sum numbers from 1 to 10:

```javascript
{
  numbers: range(1, 10);
  sum: Reduce(numbers, (stateNow, number) => stateNow + number, 0);
}
// Output: { "numbers": [1, 2, ...10], "sum": 55 }
```

We can simplify by passing the range directly:

```javascript
{
  sum: Reduce(range(1, 10), (stateNow, number) => stateNow + number, 0);
}
// Output: { "sum": 55 }
```

Using eval, we can return just the number without a key:

```javascript
{
  sum: Reduce(range(1, 10), (stateNow, number) => stateNow + number, 0);
  eval sum;
}
// Output: 55
```

We can also remove the `sum:` key entirely:

```javascript
{
  eval Reduce(range(1, 10), (stateNow, number) => stateNow + number, 0);
}
// Output: 55
```

And since we don't have key-value pairs anymore, we can even get rid of `{}`:

```bash
fs-cli 'eval Reduce(range(1,10), (s, n) => s + n, 0)'
# Type: Integer
# Value: 55
```

---

## Conclusion

The `eval` keyword in FuncScript is a powerful tool for:

1. **Focusing on results** - Skip intermediate variables and return exactly what you need
2. **Cleaner output** - Avoid KeyValueCollection wrappers when you just want a value
3. **Flexible expressions** - Use both inside and outside `{}` depending on your context
4. **Working with functions** - Extract return values from lambda expressions

> Remember: eval is most useful when you're inside `{}` and want to avoid intermediate keys. Outside braces, it's often redundant since expressions already evaluate directly.

---

> Want to read this in another format? [Read on CS](/cs/eval-in-funcscript)

---

<sup>1</sup> FuncScript is a superset of JSON that overlaps with much of JavaScript syntax yet introduces its own twists. [FuncScript](https://www.funcscript.org/)

<sup>2</sup> fs-cli is the command line interface for executing FuncScript expressions. [fs-cli](https://www.funcscript.org/developers/fs-cli/)

<sup>3</sup> FuncScript Studio is a web-based environment for experimenting with FuncScript. [FuncScript Studio](https://www.funcscript.org/fsstudio/)

<sup>4</sup> A read–eval–print loop (REPL), also termed an interactive toplevel or language shell, is a simple interactive computer programming environment that takes single user inputs, executes them, and returns the result to the user. [Read–eval–print loop](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)

<sup>5</sup> run is a universal multi-language runner and smart REPL written in Rust that lets you execute code in 25+ languages from the command line. [run](https://run.esubalew.dev/)
