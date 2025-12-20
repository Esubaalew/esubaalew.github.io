---
title: "run: Universal Multi-Language Runner & Persistent REPL (Tutorial)"
date: "2025-12-20"
description: "A structured, beginner-friendly tutorial for using run: one CLI to execute snippets, files, and stdin across 25+ languages—plus a persistent, switchable REPL."
keywords: "run, run-kit, universal runner, multi-language runner, polyglot, REPL, persistent REPL, Rust CLI, code runner, execute snippets, stdin piping, language aliases"
author: "Esubalew Chekol"
tags: ["Rust", "Polyglot", "REPL", "run", "Tutorial", "CLI", "Programming"]
og:title: "run: One CLI for 25+ Languages"
og:description: "A clear tutorial for run: execute code in multiple languages with a consistent CLI, a persistent REPL, and flexible syntax."
og:image: "/blog/og-run-universal-multi-language.png"
og:type: "article"
---

> Built in Rust for developers who live in multiple runtimes. `run` gives you a consistent CLI, persistent REPLs, and batteries-included examples for your favorite languages.

---

This post is a **full tutorial** for `run` itself: what it is, why it exists, and how to use it day-to-day.

If you want a **real-world Rust use case** (orchestrating Python/R/JS from a Rust program), read the earlier blog: [Using Run-Kit to Seamlessly Mix Multiple Languages in a Single Rust Codebase](using-run-kit-multi-language-rust.md).

---

## What is run?

`run` is a universal multi-language runner and smart REPL (Read-Eval-Print Loop) written in Rust. It provides a unified interface for executing code across many programming languages without the hassle of managing different command styles per toolchain.

You can use `run` to:

- Execute a **one-liner snippet**
- Run a **file** (language auto-detected from extension)
- Pipe **stdin** into code
- Live inside a **persistent REPL**, switching languages without leaving the session

## Who is this for?

- **Beginners**: start learning without getting stuck on tooling differences.
- **Students**: experiment quickly across languages and paradigms.
- **Developers**: prototype ideas, test algorithms, and switch stacks with minimal friction.
- **DevOps engineers**: test scripts in different runtimes from one CLI.
- **Educators**: teach concepts across languages with consistent commands.

## Why was run created?

Traditional workflows require separate setup and different commands per language:

- **Time-consuming setup**: separate compilers/interpreters/package managers per ecosystem.
- **Inconsistent interfaces**: different flags, defaults, and behaviors.
- **Cognitive overhead**: remembering many CLIs while you just want to test an idea.
- **Higher barrier to entry**: beginners fight setup before writing the first line.

`run` collapses that complexity into one consistent interface: you focus on code, and `run` handles execution.

## Why Rust?

`run` is built with Rust because it’s a great fit for a cross-platform CLI:

- **Performance**: fast startup and low overhead.
- **Reliability**: fewer runtime crashes from memory issues.
- **Cross-platform**: native binaries on Windows, macOS, and Linux.
- **Memory safety**: predictable behavior without a GC.
- **Great distribution story**: Cargo + static-ish binaries work well for CLIs.

---

## Highlights

- **One CLI** across runtimes
- **Persistent REPL** per language session
- **Flexible syntax**: snippet, file, or stdin
- **Aliases**: `py`, `js`, `rs`, `go`, `cpp`, etc.
- **Deterministic mode**: `--lang` when you need zero ambiguity

---

## Quickstart

```bash
# Show build metadata for the current binary
run --version

# Execute a snippet explicitly
run --lang python --code "print('hello, polyglot world!')"

# Let run detect language from the file extension
run examples/go/hello/main.go

# Drop into the interactive REPL (type :help inside)
run

# Pipe stdin (here: JSON) into Node.js
echo '{"name":"Ada"}' | run js --code "const data = JSON.parse(require('fs').readFileSync(0, 'utf8')); console.log(`hi ${data.name}`)"

# Pipe stdin into Python
echo "Hello from stdin" | run python --code "import sys; print(sys.stdin.read().strip().upper())"
```

---

## Installation

All release assets are published on the GitHub Releases page, including macOS builds for both Apple Silicon (`arm64`) and Intel (`x86_64`). Pick the method that fits your platform:

<details>
<summary><strong>Cargo (Rust)</strong></summary>

```bash
cargo install run-kit
```

> Installs the `run` binary from the `run-kit` crate. Updating? Run `cargo install run-kit --force`.

```bash
# Or build from source
git clone https://github.com/Esubaalew/run.git
cd run
cargo install --path .
```

</details>

<details>
<summary><strong>Homebrew (macOS)</strong></summary>

```bash
brew install --formula https://github.com/Esubaalew/run/releases/latest/download/homebrew-run.rb
```

> This formula is published as a standalone file on each release; it isn’t part of the default Homebrew taps.

</details>

<details>
<summary><strong>Debian / Ubuntu</strong></summary>

```bash
ARCH=${ARCH:-amd64}
DEB_FILE=$(curl -s https://api.github.com/repos/Esubaalew/run/releases/latest \
  | grep -oE "run_[0-9.]+_${ARCH}\\.deb" | head -n 1)
curl -LO "https://github.com/Esubaalew/run/releases/latest/download/${DEB_FILE}"
curl -LO "https://github.com/Esubaalew/run/releases/latest/download/${DEB_FILE}.sha256"
sha256sum --check "${DEB_FILE}.sha256"
sudo apt install "./${DEB_FILE}"
```

</details>

<details>
<summary><strong>Windows (Scoop)</strong></summary>

```powershell
scoop install https://github.com/Esubaalew/run/releases/latest/download/run-scoop.json
```

</details>

<details>
<summary><strong>Install script (macOS / Linux)</strong></summary>

```bash
curl -fsSLO https://raw.githubusercontent.com/Esubaalew/run/master/scripts/install.sh
chmod +x install.sh
./install.sh --add-path           # optional: append ~/.local/bin to PATH
```

</details>

Verify installation:

```bash
run --version
```

---

## How it works

`run` shells out to real toolchains under the hood. Each language engine knows how to:

1. Detect whether the toolchain exists (e.g. `python3`, `node`, `go`, `rustc`).
2. Prepare a temporary workspace (compile for compiled languages, script file for interpreters).
3. Execute snippets, files, or stdin streams and surface stdout/stderr consistently.
4. Manage session state for the interactive REPL.

This keeps the core lightweight while making it easy to support many runtimes.

---

## Supported languages

`run` supports 25+ languages out of the box, spanning scripting, systems, and scientific stacks:

```
# Scripting Languages
Python, JavaScript, Ruby, Bash, Lua, Perl, PHP

# Compiled Languages
Rust, Go, C, C++, Java, C#, Swift, Kotlin, Crystal, Zig, Nim

# Typed & Functional Languages
TypeScript, Haskell, Elixir, Julia

# Specialized Languages
R (Statistical computing)
Dart (Mobile development)
```

### Complete Language Aliases Reference

Every language in `run` has multiple aliases for convenience (badges intentionally omitted):

| Alias                                 | Language / runtime                   |
| ------------------------------------- | ------------------------------------ |
| `python`, `py`, `py3`, `python3`      | Python                               |
| `javascript`, `js`, `node`, `nodejs`  | JavaScript (Node.js)                 |
| `typescript`, `ts`, `ts-node`, `deno` | TypeScript (Deno/Node compatibility) |
| `rust`, `rs`                          | Rust                                 |
| `go`, `golang`                        | Go                                   |
| `c`, `gcc`, `clang`                   | C                                    |
| `cpp`, `c++`, `cxx`, `g++`            | C++                                  |
| `java`                                | Java                                 |
| `csharp`, `cs`, `dotnet`              | C# (.NET)                            |
| `ruby`, `rb`, `irb`                   | Ruby                                 |
| `bash`, `sh`, `shell`, `zsh`          | Shell                                |
| `lua`, `luajit`                       | Lua                                  |
| `perl`, `pl`                          | Perl                                 |
| `php`, `php-cli`                      | PHP                                  |
| `groovy`, `grv`, `groovysh`           | Groovy                               |
| `haskell`, `hs`, `ghci`               | Haskell                              |
| `elixir`, `ex`, `exs`, `iex`          | Elixir                               |
| `julia`, `jl`                         | Julia                                |
| `r`, `rscript`, `cran`                | R                                    |
| `dart`, `dartlang`, `flutter`         | Dart                                 |
| `swift`, `swiftlang`                  | Swift                                |
| `kotlin`, `kt`, `kts`                 | Kotlin                               |
| `crystal`, `cr`, `crystal-lang`       | Crystal                              |
| `zig`, `ziglang`                      | Zig                                  |
| `nim`, `nimlang`                      | Nim                                  |

---

# Command Variations - Flexible Syntax

`run` supports multiple command formats to fit your workflow. You can be explicit with `--lang` or let `run` auto-detect the language.

1. Full syntax with `--lang` and `--code`

```bash
run --lang rust --code "fn main() { println!(\"hello from rust\"); }"
```

2. Shorthand flags (`-l` for `--lang`, `-c` for `--code`)

```bash
run -l rust -c "fn main() { println!(\"hello from rust\"); }"
```

3. Omit `--code` (auto-detected)

```bash
run --code "fn main() { println!(\"hello from rust\"); }"
```

4. Just the code

```bash
run "fn main() { println!(\"hello from rust\"); }"
```

5. Language first, then code

```bash
run rust "fn main() { println!(\"hello from rust\"); }"
```

---

# Command-Line Flags Reference

```bash
# Language specification
--lang, -l          Specify the programming language
run --lang python "print('hello')"
run -l python "print('hello')"

# Code input
--code, -c          Provide code as a string
run --code "print('hello')"
run -c "print('hello')"

# Combined usage
run -l python -c "print('hello')"
run --lang python --code "print('hello')"
```

---

## When to Use --lang (Important)

Auto-detection is convenient, but **ambiguous syntax** can exist across languages. Use `--lang` when you want deterministic behavior.

```bash
# Ambiguous - may choose a different language than you intended
run "print('hello')"
```

```bash
# Explicit - always correct
run --lang python "print('hello')"
```

**Recommendation:** Always use `--lang` when:

- The syntax is shared across multiple languages
- You’re writing scripts/automation and need deterministic behavior
- You want reproducible commands in docs and CI

---

# Main Function Flexibility

For compiled languages (Rust, Go, C, C++, Java, etc.), `run` is smart about “main”:

- Write complete programs with `main`
- Or write snippet-style code (where supported) and let `run` wrap it

Go example (inside REPL):

```bash
$ run go
run universal REPL. Type :help for commands.

go>>> package main
import "fmt"
func main() {
    fmt.Println("Hello, world!")
}
Hello, world!
```

---

## Examples

If you’re browsing the `run` repo, real programs typically live under an `examples/` tree—each language often includes a small `hello` and a slightly richer scenario so you can validate your toolchain quickly.

```bash
run examples/rust/hello.rs
run examples/typescript/progress.ts
run examples/python/counter.py
```

---

## REPL

The REPL supports built-in commands for managing your session:

| Command                    | Purpose                                      |
| -------------------------- | -------------------------------------------- |
| `:help`                    | Show available meta commands                 |
| `:languages`               | Show detected engines and status             |
| `:lang <id>` or `:<alias>` | Switch the active language (`:py`, `:go`, …) |
| `:detect on/off/toggle`    | Control snippet language auto-detection      |
| `:load path/to/file`       | Execute a file inside the current session    |
| `:reset`                   | Clear the accumulated session state          |
| `:exit` / `:quit`          | Leave the REPL                               |

### Interactive REPL - Line by Line or Paste All

You can type line-by-line or paste a whole program.

Python example (paste program):

```bash
$ run python
python>>> def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### Variable Persistence & Language Switching

Variables persist **within the same language session**. When you switch languages, state does not carry over (each language has an isolated session).

```text
$ run go
go>>> x := 10
go>>> x
10

go>>> :py
switched to python

python>>> y = 10
python>>> y
10
```

### REPL Commands

```text
:help              → Show help and available commands
:languages         → List all supported languages
:clear             → Clear the screen
:exit or :quit     → Exit the REPL
:lang <language>   → Switch to a different language
Ctrl+D             → Exit the REPL
```

---

## Stdin Piping Examples

`run` supports piping input from stdin to your code snippets across languages.

### Node.js (JSON Processing)

```bash
echo '{"name":"Ada"}' | run js --code "const data = JSON.parse(require('fs').readFileSync(0, 'utf8')); console.log(`hi ${data.name}`)"
```

### Python (Uppercase Conversion)

```bash
echo "Hello from stdin" | run python --code "import sys; print(sys.stdin.read().strip().upper())"
```

### Go (Greeting)

```bash
echo "world" | run go --code 'import "fmt"; import "bufio"; import "os"; scanner := bufio.NewScanner(os.Stdin); scanner.Scan(); fmt.Printf("Hello, %s!\\n", scanner.Text())'
```

---

## Language-Specific Notes

For detailed usage, quirks, and best practices for each language, see the docs: [run.esubalew.et](https://run.esubalew.et/).

Practical tips that save time:

- **C/C++ here-docs**: prefer quoted here-doc delimiters (`<<'EOF'`) so the shell doesn’t expand `%d`, `\n`, `$vars`, and glob patterns.
- **TypeScript (Deno)**: prefer explicit module specifiers (like `node:fs`).
- **Groovy / shells**: quote here-docs to prevent `$` interpolation by the shell.

---
