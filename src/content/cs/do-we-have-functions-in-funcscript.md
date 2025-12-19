---
title: Do We Have Functions in FuncScript?
description: Exploring whether FuncScript has functions in the traditional programming sense. A deep dive into lambda expressions, reusable code blocks, and how to think about functions in a JSON-with-superpowers world.
keywords: FuncScript, fs-cli, functions, lambda, JSON, expression language, functional programming, KeyValueCollection, map, Range
og_title: Do We Have Functions in FuncScript?
og_description: Exploring functions and lambda expressions in FuncScript - from simple returns to complex transformations
og_image: /assets/og-cs-do-we-have-functions-in-funcscript.png
date: 2025-12-19
---

<div class="intro-box">
<h2>What is FuncScript?</h2>
<p>
FuncScript<a href="#fn1"><sup>1</sup></a> is a superset of JSON that lets you promote property values into expressions. Instead of static literals, <code>{ x: 1 + 2; }</code> is perfectly legal. You can execute FuncScript using fs-cli<a href="#fn2"><sup>2</sup></a> (the command line interface) or experiment in FuncScript Studio<a href="#fn3"><sup>3</sup></a> (a web-based environment).
</p>
</div>

This article assumes you have basic knowledge of FuncScript. If you're new to it, I recommend starting with the <a href="https://www.funcscript.org/" target="_blank">official documentation</a> or reading my previous article on <a href="/cs/my-first-view-on-funcscript-cli">fs-cli basics</a>.

## _Do functions exist in FuncScript?_

Well, I don't know if there is a "function" in FuncScript in the modern programming language sense.

A function is nothing but a block of code that does something specific. The main ideas are: (1) we can have separated concerns where we do tasks step by step, and (2) we can make code reusable. Instead of hardcoding everything, we can have a block of code dedicated to a specific task.

We don't have a way of creating a function in the format traditional programming languages use, but we can achieve it in a way that looks like JSON. Please remember that FuncScript is nothing but a powerful JSON.

## _Everything in braces is a function_

To make things easier, let's assume FuncScript code is JSON, and the JSON itself is a function. So let's say everything in `{}` is a function where the key is the name of the function and the value is the return value.

To be more specific, if we have a FuncScript code `{a: 10;}`, that means `a` is the name of the function and `10` is what the function `a` returns.

Please note that in reality everything with `{}` is called `KeyValueCollection`, but we must pretend it's not for this exploration.

Here's how we can run this in fs-cli:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{a: 10}'</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="type-label">Value:</span>
<span class="value-label">{
  "a": 10
}</span></code></pre>
</div>
</div>

From here on, I'll show FuncScript code and output separately for clarity. You can run these in fs-cli or FuncScript Studio.

Let's achieve this same thing in Rust to make a connection with traditional programming languages. I'll use `run`<a href="#fn4"><sup>4</sup></a> for simplicity:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">run rust</span>
<span class="output">run universal REPL. Type :help for commands.</span>
rust>>> fn ten() -> i32 { 10 }
rust>>> ten()
10</code></pre>
</div>
</div>

That's essentially what we just did in FuncScript - or even simpler!

To make it cleaner and return only `10` instead of the whole `KeyValueCollection`, we use `eval`:

```javascript
{
  a: 10;
  eval a;
}
```

Output:

```javascript
10;
```

So that's the most basic function in FuncScript.

## _But where are the parentheses?_

You might ask: where is the `()` - the parameter symbol that can either be empty or hold some parameters? Like we see in Rust: `fn ten() -> i32 { 10 }`.

Let's first look at Python - to create a simple "hello" function, then adapt it to FuncScript:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code>python>>> def say_hello(): return 'Hello'
python>>> say_hello()
'Hello'</code></pre>
</div>
</div>

Now let's adapt this in FuncScript - maybe in an even simpler way than Python:

```javascript
{
  say_hello: () => "hello";
  eval say_hello();
}
```

Output:

```javascript
"hello";
```

If we want to make it a two-step process, we can remove the `eval` and see the full structure:

```javascript
{
  say_hello: () => "hello";
  result: say_hello();
}
```

Output:

```javascript
{
  say_hello: "[Function]",
  result: "hello",
};
```

## _Functions with parameters_

What if we have parameters, like printing "Hello, name" where `name` is an argument the function receives?

In Python:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code>python>>> name = "Esubalew"
python>>> def say_hello(name): return "hello " + name
python>>> say_hello(name)
'hello Esubalew'</code></pre>
</div>
</div>

Now let's do the exact same thing in FuncScript:

```javascript
{
  name: "Esubalew";
  say_hello: (name) => "Hello " + name;
  eval say_hello();
}
```

Output:

```javascript
"Hello Esubalew";
```

Or if we don't have the argument ready and want to pass it at runtime:

```javascript
{
  say_hello: (name) => "Hello " + name;
  eval say_hello("Augustus");
}
```

Output:

```javascript
"Hello Augustus";
```

## _Complex transformations with functions_

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
```

Output:

```javascript
[
  { old: 1, newer: 0.01 },
  { old: 2, newer: 0.02 },
];
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
```

Output:

```javascript
{
  rate: 0.01,
  numbers: [1, 2],
  multiply: "[Function]",
  multiplied: [
    { old: 1, newer: 0.01 },
    { old: 2, newer: 0.02 },
  ],
};
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
```

Output:

```javascript
0.01;
```

## _Simplifying step by step_

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
```

Output:

```javascript
[
  { old: 1, newer: 0.01 },
  { old: 2, newer: 0.02 },
  { old: 3, newer: 0.03 },
  { old: 4, newer: 0.04 },
  { old: 5, newer: 0.05 },
];
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
```

Output:

```javascript
[
  { old: 1, newer: 0.01 },
  { old: 2, newer: 0.02 },
];
```

Or get rid of naming entirely and go fully inline:

```javascript
{
  eval Range(1, 2) map (n) => {
    old: n;
    newer: n / 100;
  };
}
```

Output:

```javascript
[
  { old: 1, newer: 0.01 },
  { old: 2, newer: 0.02 },
];
```

## _Conclusion_

So, do we have functions in FuncScript? Not in the traditional `function` or `def` keyword sense. But we absolutely have:

- **Lambda expressions**: `(param) => expression`
- **Named bindings**: Store lambdas as reusable values
- **Higher-order functions**: `map`, and other helpers that accept functions
- **Closures**: Lambdas can reference outer bindings like `rate`

FuncScript takes a different approach. Instead of defining functions as separate entities, everything lives inside the JSON-like structure. Your "functions" are just properties that happen to hold lambdas. This makes FuncScript feel less like traditional programming and more like building reactive, self-computing documents.

The beauty is in the simplicity: what starts as `{a: 10}` can evolve into complex transformations while maintaining that familiar JSON shape.

---

<div class="translation-link">
Want to read this in another format? <a href="/blog/do-we-have-functions-in-funcscript">Read on Blog</a>
</div>

<div class="footnote">
<p id="fn1"><sup>1</sup> FuncScript is a superset of JSON that overlaps with much of JavaScript syntax yet introduces its own twists. <a href="https://www.funcscript.org/" target="_blank">FuncScript</a></p>
<p id="fn2"><sup>2</sup> fs-cli is the command line interface for executing FuncScript expressions. <a href="https://www.funcscript.org/developers/fs-cli/" target="_blank">fs-cli</a></p>
<p id="fn3"><sup>3</sup> FuncScript Studio is a web-based environment for experimenting with FuncScript. <a href="https://www.funcscript.org/fsstudio/" target="_blank">FuncScript Studio</a></p>
<p id="fn4"><sup>4</sup> run is a universal multi-language runner and smart REPL written in Rust that lets you execute code in 25+ languages from the command line. <a href="https://run.esubalew.dev/" target="_blank">run</a></p>
</div>
