---
title: My First View on FuncScript CLI
description: A beginner's exploration of fs-cli, the FuncScript command line interface. Lessons learned about quoting, argument handling, and string types when working with this JSON-with-superpowers expression language.
keywords: FuncScript, fs-cli, CLI, command line, JSON, expression language, JavaScript, programming, REPL, npm, npx
og_title: My First View on FuncScript CLI
og_description: Lessons learned from exploring fs-cli - quoting rules, argument handling, and string type quirks
og_image: /assets/og-cs-funcscript-cli.png
date: 2025-06-17
---

<div class="intro-box">
<h2>What is FuncScript?</h2>
<p>
<a href="https://www.funcscript.org/" target="_blank">FuncScript</a> is a superset of JSON that lets you promote property values into expressions. Instead of static literals, <code>{ x: 1 + 2; }</code> is perfectly legal. It keeps JSON's predictability while gaining a concise expression language. The <a href="https://www.funcscript.org/developers/fs-cli/" target="_blank">fs-cli</a> is a lightweight Node.js command line interface that wraps the FuncScript runtime. There's also <a href="https://www.funcdraw.app/" target="_blank">FuncDraw</a>, a UI tool built using FuncScript.
</p>
</div>

This article documents my first experience with `fs-cli`. Note that these observations were made on a specific version of the tool and may not apply to future updates. Think of this as field notes from a curious explorer.

## *What is the lesson I took*

Well most of the issues seem to have a workaround: using `""` is the preferred way of doing FuncScript. Instead of:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli 3 + 'cool'</span></code></pre>
</div>
</div>

I will do:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "3 + 'cool'"</span></code></pre>
</div>
</div>

And also:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "'cool' + 4"</span></code></pre>
</div>
</div>

## *I should not be confused with things in quotes*

When we come to most programming languages, if not all, things in `""` means they are string literals. But here fs-cli expects one argument and if we have more than that, either that is going to be rejected or fs-cli panics.

So if we have `npx fs-cli "4 + 3"`, the `"4 + 3"` is not a string—it's the expression `4 + 3`. Here `" "` is being used to define the expression. It's like entering in Python REPL<sup>1</sup> and executing `4 + 4`:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">python3</span>
<span class="output">Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.</span>
>>> 4 + 3
7
>>></code></pre>
</div>
</div>

As for other languages like Python, string concatenation works naturally:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code>>>> "Hello" + "Hello"
'HelloHello'
>>></code></pre>
</div>
</div>

We can do this in fs-cli but a little bit differently—instead of separately treating the operands, we quote everything in `""`:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "'Hello' + 'Hello'"</span>
<span class="type-label">Type: String</span>
<span class="type-label">Value:</span>
<span class="value-label">"HelloHello"</span></code></pre>
</div>
</div>

The reason we are not doing something like Python is because in fs-cli we are talking with the shell, not only with fs-cli. In Python, in the above example, we are in Python's world where everything is in Python's environment.

If we try to do what we are doing in Python, we fail:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">python3 "3 + 3"</span>
<span class="output">/opt/homebrew/Cellar/python@3.13/3.13.7/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/esubalew/Downloads/testing/3 + 3': [Errno 2] No such file or directory</span></code></pre>
</div>
</div>

What happened is that fs-cli expects expression mostly in `""` or numbers, or some variable. Python expects a file name, so `"3 + 3"` was not a valid file name on my machine, and it failed.

Fs-cli is now more like [run](https://github.com/sigoden/runmulti) (run-kit)<sup>2</sup> but not entirely. For example:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">run "print(4 + 34)"</span>
38</code></pre>
</div>
</div>

Here `run` expects file path (like Python args) or code (much like fs-cli). If we do `run 4 + 4` or even `"3 + 3"` that is wrong because these are neither correct file path nor correct code.

Actually `run` is also REPL which means it can maintain its own environment:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">run py</span>
<span class="output">run universal REPL. Type :help for commands.</span>
python>>> print((lambda x: [i*i for i in x])([1,2,3,4,5]))
[1, 4, 9, 16, 25]
python>>></code></pre>
</div>
</div>

## *Fs-cli is a one argument tool*

fs-cli expects one argument. If we don't respect that, results are going to be unexpected. As I mentioned in the section above, it is recommended that we use quotes when passing that argument.

It first looks like we can ignore quotes if we are passing a valid data type, and this works fine for most of the types. The snippets below show that Integer, Dictionary (`KeyValueCollection`), Float, and Boolean work fine without using quotes. This means `npx fs-cli 3` is the same as `npx fs-cli "3"`:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli 3</span>
<span class="type-label">Type: Integer</span>
<span class="type-label">Value:</span>
<span class="value-label">3</span>

<span class="prompt">npx fs-cli 3.3</span>
<span class="type-label">Type: Float</span>
<span class="type-label">Value:</span>
<span class="value-label">3.3</span>

<span class="prompt">npx fs-cli true</span>
<span class="type-label">Type: Boolean</span>
<span class="type-label">Value:</span>
<span class="value-label">true</span>

<span class="prompt">npx fs-cli "{}"</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="type-label">Value:</span>
<span class="value-label">{}</span>

<span class="prompt">npx fs-cli {}</span>
<span class="type-label">Type: KeyValueCollection</span>
<span class="type-label">Value:</span>
<span class="value-label">{}</span></code></pre>
</div>
</div>

But the issue I discovered is this breaks sometimes or on some Types:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli []</span>
<span class="output">zsh: no matches found: []</span></code></pre>
</div>
</div>

Wrapping this in quotes solved the issue:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "[]"</span>
<span class="type-label">Type: List</span>
<span class="type-label">Value:</span>
<span class="value-label">[]</span></code></pre>
</div>
</div>

<div class="note">
<strong>Takeaway</strong>
So as my title suggests, don't do things unquoted. Or make sure you know which behavior results in the action you executed.
</div>

## *Data type String is wronged* <span class="ethiopic">(ተበድሏል)</span>

Because of the fact that things are naturally expected to be defined in `""`, strings are hard to appear.

`npx fs-cli "3"` is interpreted as Integer and `npx fs-cli "true"` is interpreted as a Boolean and `npx fs-cli "trued"` as Null Type.

But fortunately this is more like a joke than a real issue. If we want to get a string, we need to define a string like `"true"`. We can do that by defining it like `npx fs-cli "'true'"` or we can escape the character we want to use with double quotes. This way we can also make numbers into strings:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "'38934'"</span>
<span class="type-label">Type: String</span>
<span class="type-label">Value:</span>
<span class="value-label">"38934"</span></code></pre>
</div>
</div>

I can even do:

<div class="terminal">
<div class="terminal-header">
<span class="terminal-dot red"></span>
<span class="terminal-dot yellow"></span>
<span class="terminal-dot green"></span>
</div>
<div class="terminal-body">
<pre><code><span class="prompt">npx fs-cli "{ eval f'{{ \"name\": [\"Abebe\", \"Alemu\"] }}'; }"</span>
<span class="type-label">Type: String</span>
<span class="type-label">Value:</span>
<span class="value-label">"{ \"name\":[\"Abebe\", \"Alemu\"] }"</span></code></pre>
</div>
</div>

But the output is a bit scary—the escape character comes in the output.

---

<div class="footnote">
<p><sup>1</sup> A read–eval–print loop (REPL), also termed an interactive toplevel or language shell, is a simple interactive computer programming environment that takes single user inputs, executes them, and returns the result to the user. <a href="https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop" target="_blank">Read–eval–print loop</a></p>
<p><sup>2</sup> run is a universal multi-language runner and smart REPL (Read-Eval-Print Loop) written in Rust. <a href="https://github.com/sigoden/runmulti" target="_blank">run</a></p>
</div>

