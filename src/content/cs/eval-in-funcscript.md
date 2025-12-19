---
title: Eval in FuncScript
description: Understanding the eval keyword in FuncScript - how it helps you focus on results, avoid intermediate variables, and write cleaner expressions both inside and outside braces.
keywords: FuncScript, fs-cli, eval, expression, JSON, functional programming, KeyValueCollection, Reduce, map, Range
og_title: Eval in FuncScript
og_description: Master the eval keyword in FuncScript to focus on results and write cleaner code
og_image: /assets/og-cs-eval-in-funcscript.png
date: 2025-12-20
---

<div class="intro-box">
<h2>What is FuncScript?</h2>
<p>
FuncScript<a href="#fn1"><sup>1</sup></a> is a superset of JSON that lets you promote property values into expressions. Instead of static literals, <code>{ x: 1 + 2; }</code> is perfectly legal. You can execute FuncScript using fs-cli<a href="#fn2"><sup>2</sup></a> (the command line interface) or experiment in FuncScript Studio<a href="#fn3"><sup>3</sup></a> (a web-based environment).
</p>
</div>

This article assumes you have basic knowledge of FuncScript. If you're new to it, I recommend starting with the <a href="https://www.funcscript.org/" target="_blank">official documentation</a> or reading my previous articles: <a href="/cs/my-first-view-on-funcscript-cli">fs-cli basics</a> and <a href="/cs/do-we-have-functions-in-funcscript">functions in FuncScript</a>.

## _What is eval?_

Even though FuncScript code is typically written inside `{}`, it doesn't mean we can't do anything outside braces. Just like Python, Node, or Lua have their own REPL<a href="#fn4"><sup>4</sup></a> environments, FuncScript has fs-cli - which lets us execute simple code without worrying about wrapping everything in a file structure. It's similar to using <a href="https://run.esubalew.dev/" target="_blank">run</a><a href="#fn5"><sup>5</sup></a> to do `4 + 5` in C or C++ without the main function.

So the following is also legal in FuncScript:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '4 + 3'</span>
<span class="type-label">Type: Integer</span>
<span class="type-label">Value:</span>
<span class="value-label">7</span></code></pre>
</div>
</div>

Keep in mind that you need to quote your argument with `""` or `''` for fs-cli, otherwise unexpected things will happen. For more about fs-cli syntax, please read <a href="/cs/my-first-view-on-funcscript-cli">my first view on fs-cli</a>.

---

## _Two ways to run FuncScript_

There are two main ways to run FuncScript: **FuncScript Studio** (a web-based editor) and **fs-cli** (command line interface).

The main difference is the method of input. In fs-cli, everything we call code must be passed as `fs-cli 'arg'` where `arg` is the code. Using quotes is a must (or at least recommended) because things like `fs-cli 4 + 4` will only read the first `4` and miss everything after the first argument.

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="comment"># This is WRONG - fs-cli only sees "4"</span>
<span class="prompt">fs-cli 4 + 4</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">4</span>

<span class="comment"># This is CORRECT</span>
<span class="prompt">fs-cli '4 + 4'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">8</span></code></pre>

</div>
</div>

This means `fs-cli eval 4 + 4` is an invalid expression. The solution is quoting it as `fs-cli 'eval 4 + 4'`.

In FuncScript Studio, `eval 4 + 4` works directly since it's an editor environment. You can access the playground at <a href="https://www.funcscript.org/fsstudio/" target="_blank">funcscript.org/fsstudio</a>.

---

## _Eval with different types_

As long as we follow the same format, we can use eval with any type:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli 'eval "Hello, Esubalew"'</span>
<span class="type-label">Type: String</span>
<span class="value-label">"Hello, Esubalew"</span>

<span class="prompt">fs-cli 'eval [3, 3]'</span>
<span class="type-label">Type: List</span>
<span class="value-label">[3, 3]</span>

<span class="prompt">fs-cli 'eval {}'</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="value-label">{}</span>

<span class="prompt">fs-cli 'eval {age: 10, name: "cool"}'</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="value-label">{
"age": 10,
"name": "cool"
}</span></code></pre>

</div>
</div>

The same applies in FuncScript Studio, except we don't use the outer quotes:

```javascript
eval {age: 10, name: "cool"}
// Output: { "age": 10, "name": "cool" }
```

---

## _Eval with expressions inside braces_

We can use eval inside `{}` to combine values:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{name: "Esubalew"; full: "Hello, " + name;}'</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="value-label">{
  "name": "Esubalew",
  "full": "Hello, Esubalew"
}</span>

<span class="prompt">fs-cli '{a: 10; b: 20; sum: a + b;}'</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="value-label">{
"a": 10,
"b": 20,
"sum": 30
}</span></code></pre>

</div>
</div>

But what if we want to avoid the intermediate `sum` key and just evaluate to the sum directly?

---

## _The problem with missing keys_

Can we do something like this?

```javascript
fs-cli '{a: 10; b: 20; a + b}'
```

Will this result in `30`? **No, it will not.** The `{}` object violates the key: value syntax because `a + b` is without a key.

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{a: 10; b: 20; a + b}'</span>
<span class="error">Failed to parse expression</span></code></pre>
</div>
</div>

This is where **eval** becomes powerful. By taking eval inside `{}`, we can return the result directly:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{a: 10; b: 20; eval a + b;}'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">30</span></code></pre>
</div>
</div>

---

## _Focusing on results with eval_

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

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{number: [1, 2] map (n) => n * 2; eval number[0]}'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">2</span></code></pre>
</div>
</div>

---

## _A practical example_

Let's revisit an example from my <a href="/cs/do-we-have-functions-in-funcscript">previous article</a>:

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
};
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

## _When eval has no effect_

Please note that using eval on a value that's already a direct return is useless:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli 'range(1, 10)'</span>
<span class="type-label">Type: List</span>
<span class="value-label">[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]</span>

<span class="prompt">fs-cli 'range(1, 10)[0]'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">1</span>

<span class="prompt">fs-cli 'eval range(1, 10)[0]'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">1</span></code></pre>

</div>
</div>

Here adding eval is of no effect. Think of it like doing `eval 1` which just returns `1`.

---

## _Eval with functions_

If we have a function (what I call a "key function" - learn more at <a href="/cs/do-we-have-functions-in-funcscript">my functions article</a>) that returns a multiplied value:

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

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli '{multi: (x) => x * 2; eval multi(2)}'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">4</span></code></pre>
</div>
</div>

---

## _Eval with Reduce_

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

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">fs-cli 'eval Reduce(range(1,10), (s, n) => s + n, 0)'</span>
<span class="type-label">Type: Integer</span>
<span class="value-label">55</span></code></pre>
</div>
</div>

---

## _Conclusion_

The `eval` keyword in FuncScript is a powerful tool for:

1. **Focusing on results** - Skip intermediate variables and return exactly what you need
2. **Cleaner output** - Avoid KeyValueCollection wrappers when you just want a value
3. **Flexible expressions** - Use both inside and outside `{}` depending on your context
4. **Working with functions** - Extract return values from lambda expressions

Remember: eval is most useful when you're inside `{}` and want to avoid intermediate keys. Outside braces, it's often redundant since expressions already evaluate directly.

---

<div class="translation-link">
Want to read this in another format? <a href="/blog/eval-in-funcscript">Read on Blog</a>
</div>

<div class="footnote">
<p id="fn1"><sup>1</sup> FuncScript is a superset of JSON that overlaps with much of JavaScript syntax yet introduces its own twists. <a href="https://www.funcscript.org/" target="_blank">FuncScript</a></p>
<p id="fn2"><sup>2</sup> fs-cli is the command line interface for executing FuncScript expressions. <a href="https://www.funcscript.org/developers/fs-cli/" target="_blank">fs-cli</a></p>
<p id="fn3"><sup>3</sup> FuncScript Studio is a web-based environment for experimenting with FuncScript. <a href="https://www.funcscript.org/fsstudio/" target="_blank">FuncScript Studio</a></p>
<p id="fn4"><sup>4</sup> A read–eval–print loop (REPL), also termed an interactive toplevel or language shell, is a simple interactive computer programming environment that takes single user inputs, executes them, and returns the result to the user. <a href="https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop" target="_blank">Read–eval–print loop</a></p>
<p id="fn5"><sup>5</sup> run is a universal multi-language runner and smart REPL written in Rust that lets you execute code in 25+ languages from the command line. <a href="https://run.esubalew.dev/" target="_blank">run</a></p>
</div>
