"""
Example usage of the MarkdownBoard class.
"""

from utility.MarkdownBoard import MarkdownBoard, TableHeader, TableData

# Create a new MarkdownBoard instance
board = MarkdownBoard()

# Write a main title (H1)
board.writeMainTitle("My Document Title")

# Write a subtitle (H2)
board.writeSubTitle("Introduction")

# Write some text
board.writeText("This is a paragraph with some text.")
board.writeText("This is bold text.", bold=True)
board.writeText("This is italic text.", italic=True)
board.writeText("This is bold and italic text.", bold=True, italic=True)

# Write a code block
python_code = """
def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
"""

board.writeCodeBlock(python_code, "python", "Python Example")

# Take a snapshot of what we have so far
board.TakeSnapshot("First Section")

# Clear the board for reuse
board.RemoveSnapshot()

# Write a topic (H3)
board.writeTopic("Lists Section")

# Write an unordered list
items = ["First item", "Second item", "Third item"]
board.writeList(items)

# Write an ordered list with some bold items
ordered_items = ["Important point", "Regular point", "Another important point"]
bold_flags = [True, False, True]
board.writeList(ordered_items, ordered=True, bold_items=bold_flags)

# Write a subtopic (H4)
board.writeSubTopic("Links and Tables")

# Write a link
board.writeLink("Visit Google", "https://www.google.com")

# Create and write a table
header1 = TableHeader("Name")
header2 = TableHeader("Age")
header3 = TableHeader("City")

data1 = TableData("Alice")
data2 = TableData("30")
data3 = TableData("New York")

data4 = TableData("Bob")
data5 = TableData("25")
data6 = TableData("London")

row1 = board.writeRow([header1, header2, header3])
row2 = board.writeRow([data1, data2, data3])
row3 = board.writeRow([data4, data5, data6])

board.writeTable([row1, row2, row3])

# Take a snapshot of the second section
board.TakeSnapshot("Second Section")