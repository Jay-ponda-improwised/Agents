# Component Documentation

## MainTitle

An H1 title.

```python
board = VirtualMarkdownBoard()
board.main_title("This is a Main Title")
board.take_snapshot("MainTitle Demo")
```

**Output:**

```
╭─ MainTitle Demo ───────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  This is a Main Title                                                                  │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## SubTitle

An H2 title.

```python
board = VirtualMarkdownBoard()
board.sub_title("This is a Sub Title")
board.take_snapshot("SubTitle Demo")
```

**Output:**

```
╭─ SubTitle Demo ────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  This is a Sub Title                                                                   │
│  ────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## Topic

An H3 title.

```python
board = VirtualMarkdownBoard()
board.topic("This is a Topic")
board.take_snapshot("Topic Demo")
```

**Output:**

```
╭─ Topic Demo ───────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ● This is a Topic                                                                     │
│  ────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## SubTopic

An H4 title.

```python
board = VirtualMarkdownBoard()
board.sub_topic("This is a Sub Topic")
board.take_snapshot("SubTopic Demo")
```

**Output:**

```
╭─ SubTopic Demo ────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ➡ This is a Sub Topic                                                                 │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## TextBlock

A block of text.

```python
board = VirtualMarkdownBoard()
board.text("This is a simple text block.")
board.take_snapshot("TextBlock Demo")
```

**Output:**

```
╭─ TextBlock Demo ───────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  This is a simple text block.                                                          │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

### TextBlock with Point

```python
board = VirtualMarkdownBoard()
board.text("This is a text block with a point.", point=True)
board.take_snapshot("TextBlock Point Demo")
```

**Output:**

```
╭─ TextBlock Point Demo ─────────────────────────────────────────────────────────────────╮
│                                                                                        │
│                                                                                        │
│   • This is a text block with a point.                                                 │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

### Adding Empty Lines

You can add empty lines using the `text` method with an empty string:

```python
board = VirtualMarkdownBoard()
board.text("")
board.text("This is a line after an empty line.")
board.take_snapshot("Empty Line Demo")
```

**Output:**

```
╭─ Empty Line Demo ──────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│                                                                                        │
│  This is a line after an empty line.                                                   │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## CodeBlock

A block of code.

```python
board = VirtualMarkdownBoard()
code = 'print("Hello, World!")'
board.code_block(code, language='python', title='Python Code')
board.take_snapshot("CodeBlock Demo")
```

**Output:**

```
╭─ CodeBlock Demo ───────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ╭─ Python Code ────────────────────────────────────────────────────────────────────╮  │
│  │   1 print("Hello, World!")                                                       │  │
│  ╰──────────────────────────────────────────────────────────────────────────────────╯  │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## TableComponent

A table.

```python
board = VirtualMarkdownBoard()
headers = ["Name", "Age", "City"]
rows = [["Alice", "30", "New York"], ["Bob", "25", "London"]]board.table(headers, rows)
board.take_snapshot("Table Demo")
```

**Output:**

```
╭─ Table Demo ───────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ┏━━━━━━━┳━━━━━┳━━━━━━━━━━┓                                                            │
│  ┃ Name  ┃ Age ┃ City     ┃                                                            │
│  ┡━━━━━━━╇━━━━━╇━━━━━━━━━━┩                                                            │
│  │ Alice │ 30  │ New York │                                                            │
│  │ Bob   │ 25  │ London   │                                                            │
│  └───────┴─────┴──────────┘                                                            │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## ListComponent

An ordered or unordered list.

### Unordered List

```python
board = VirtualMarkdownBoard()
board.list(["Item 1", "Item 2", "Item 3"])
board.take_snapshot("Unordered List Demo")
```

**Output:**

```
╭─ Unordered List Demo ──────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ➤ Item 1                                                                              │
│  ➤ Item 2                                                                              │
│  ➤ Item 3                                                                              │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

### Ordered List

```python
board = VirtualMarkdownBoard()
board.list(["Item 1", "Item 2", "Item 3"], ordered=True)
board.take_snapshot("Ordered List Demo")
```

**Output:**

```
╭─ Ordered List Demo ────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  1. Item 1                                                                             │
│  2. Item 2                                                                             │
│  3. Item 3                                                                             │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

### Nested List (Automatic)

```python
board = VirtualMarkdownBoard()
board.list(["Item 1", ["Nested 1", "Nested 2"], "Item 3"], ordered=True)
board.take_snapshot("Nested List Demo")
```

**Output:**

```
╭─ Nested List Demo ─────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  1. Item 1                                                                             │
│    1. Nested 1                                                                         │
│    2. Nested 2                                                                         │
│  3. Item 3                                                                             │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

### List with Mixed Data Types

```python
board = VirtualMarkdownBoard()
board.list(["String item", 123, 45.67, True], ordered=False)
board.take_snapshot("Mixed Data List Demo")
```

**Output:**

```
╭─ Mixed Data List Demo ─────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ➤ String item                                                                         │
│  ➤ 123                                                                                 │
│  ➤ 45.67                                                                               │
│  ➤ True                                                                                │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

## LineComponent

A horizontal line.

```python
board = VirtualMarkdownBoard()
board.line(style="red", character="=")
board.take_snapshot("Line Demo")
```

**Output:**

```
╭─ Line Demo ────────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ====================================================================================  │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

