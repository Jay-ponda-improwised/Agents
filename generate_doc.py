import os
from utility.Console.VirtualMarkdownBoard import VirtualMarkdownBoard
from utility.Console.Component.List.Base import ListComponent
from utility.Console.Component.TextBlock.Base import TextBlock
from utility.Console.Component.Line.Base import LineComponent

def capture_output(func):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        func()
    return f.getvalue()

def generate_docs():
    with open("doc.md", "w") as f:
        f.write("# Component Documentation\n\n")

        # MainTitle
        f.write("## MainTitle\n\n")
        f.write("An H1 title.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.main_title("This is a Main Title")\n')
        f.write('board.take_snapshot("MainTitle Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def main_title_demo():
            board = VirtualMarkdownBoard()
            board.main_title("This is a Main Title")
            board.take_snapshot("MainTitle Demo")
        output = capture_output(main_title_demo)
        f.write(output)
        f.write("```\n\n")

        # SubTitle
        f.write("## SubTitle\n\n")
        f.write("An H2 title.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.sub_title("This is a Sub Title")\n')
        f.write('board.take_snapshot("SubTitle Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def sub_title_demo():
            board = VirtualMarkdownBoard()
            board.sub_title("This is a Sub Title")
            board.take_snapshot("SubTitle Demo")
        output = capture_output(sub_title_demo)
        f.write(output)
        f.write("```\n\n")

        # Topic
        f.write("## Topic\n\n")
        f.write("An H3 title.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.topic("This is a Topic")\n')
        f.write('board.take_snapshot("Topic Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def topic_demo():
            board = VirtualMarkdownBoard()
            board.topic("This is a Topic")
            board.take_snapshot("Topic Demo")
        output = capture_output(topic_demo)
        f.write(output)
        f.write("```\n\n")

        # SubTopic
        f.write("## SubTopic\n\n")
        f.write("An H4 title.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.sub_topic("This is a Sub Topic")\n')
        f.write('board.take_snapshot("SubTopic Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def sub_topic_demo():
            board = VirtualMarkdownBoard()
            board.sub_topic("This is a Sub Topic")
            board.take_snapshot("SubTopic Demo")
        output = capture_output(sub_topic_demo)
        f.write(output)
        f.write("```\n\n")

        # TextBlock
        f.write("## TextBlock\n\n")
        f.write("A block of text.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.text("This is a simple text block.")\n')
        f.write('board.take_snapshot("TextBlock Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def text_block_demo():
            board = VirtualMarkdownBoard()
            board.text("This is a simple text block.")
            board.take_snapshot("TextBlock Demo")
        output = capture_output(text_block_demo)
        f.write(output)
        f.write("```\n\n")

        f.write("### TextBlock with Point\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.text("This is a text block with a point.", point=True)\n')
        f.write('board.take_snapshot("TextBlock Point Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def text_block_point_demo():
            board = VirtualMarkdownBoard()
            board.text("This is a text block with a point.", point=True)
            board.take_snapshot("TextBlock Point Demo")
        output = capture_output(text_block_point_demo)
        f.write(output)
        f.write("```\n\n")

        # CodeBlock
        f.write("## CodeBlock\n\n")
        f.write("A block of code.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write("code = 'print(\"Hello, World!\")'\n")
        f.write("board.code_block(code, language='python', title='Python Code')\n")
        f.write('board.take_snapshot("CodeBlock Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def code_block_demo():
            board = VirtualMarkdownBoard()
            code = 'print("Hello, World!")'
            board.code_block(code, language='python', title='Python Code')
            board.take_snapshot("CodeBlock Demo")
        output = capture_output(code_block_demo)
        f.write(output)
        f.write("```\n\n")

        # TableComponent
        f.write("## TableComponent\n\n")
        f.write("A table.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('headers = ["Name", "Age", "City"]\n')
        f.write('rows = [["Alice", "30", "New York"], ["Bob", "25", "London"]]')
        f.write("board.table(headers, rows)\n")
        f.write('board.take_snapshot("Table Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def table_demo():
            board = VirtualMarkdownBoard()
            headers = ["Name", "Age", "City"]
            rows = [["Alice", "30", "New York"], ["Bob", "25", "London"]]
            board.table(headers, rows)
            board.take_snapshot("Table Demo")
        output = capture_output(table_demo)
        f.write(output)
        f.write("```\n\n")

        # ListComponent
        f.write("## ListComponent\n\n")
        f.write("An ordered or unordered list.\n\n")
        f.write("### Unordered List\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.list(["Item 1", "Item 2", "Item 3"])\n')
        f.write('board.take_snapshot("Unordered List Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def unordered_list_demo():
            board = VirtualMarkdownBoard()
            board.list(["Item 1", "Item 2", "Item 3"])
            board.take_snapshot("Unordered List Demo")
        output = capture_output(unordered_list_demo)
        f.write(output)
        f.write("```\n\n")

        f.write("### Ordered List\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.list(["Item 1", "Item 2", "Item 3"], ordered=True)\n')
        f.write('board.take_snapshot("Ordered List Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def ordered_list_demo():
            board = VirtualMarkdownBoard()
            board.list(["Item 1", "Item 2", "Item 3"], ordered=True)
            board.take_snapshot("Ordered List Demo")
        output = capture_output(ordered_list_demo)
        f.write(output)
        f.write("```\n\n")

        f.write("### Nested List (Automatic)\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.list(["Item 1", ["Nested 1", "Nested 2"], "Item 3"], ordered=True)\n')
        f.write('board.take_snapshot("Nested List Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def nested_list_demo():
            board = VirtualMarkdownBoard()
            board.list(["Item 1", ["Nested 1", "Nested 2"], "Item 3"], ordered=True)
            board.take_snapshot("Nested List Demo")
        output = capture_output(nested_list_demo)
        f.write(output)
        f.write("```\n\n")

        f.write("### List with Mixed Data Types\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.list(["String item", 123, 45.67, True], ordered=False)\n')
        f.write('board.take_snapshot("Mixed Data List Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def mixed_data_list_demo():
            board = VirtualMarkdownBoard()
            board.list(["String item", 123, 45.67, True], ordered=False)
            board.take_snapshot("Mixed Data List Demo")
        output = capture_output(mixed_data_list_demo)
        f.write(output)
        f.write("```\n\n")

        # LineComponent
        f.write("## LineComponent\n\n")
        f.write("A horizontal line.\n\n")
        f.write("```python\n")
        f.write("board = VirtualMarkdownBoard()\n")
        f.write('board.line(style="red", character="=")\n')
        f.write('board.take_snapshot("Line Demo")\n')
        f.write("```\n\n")
        f.write("**Output:**\n\n")
        f.write("```\n")
        def line_demo():
            board = VirtualMarkdownBoard()
            board.line(style="red", character="=")
            board.take_snapshot("Line Demo")
        output = capture_output(line_demo)
        f.write(output)
        f.write("```\n\n")


if __name__ == "__main__":
    generate_docs()
