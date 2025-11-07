from utility.Console.VirtualMarkdownBoard import VirtualMarkdownBoard
from utility.Console.Component.Table.Base import TableComponent
from typing import cast

def main():
    board = VirtualMarkdownBoard()

    # Add a main title
    board.write_main_title("Virtual Markdown Board Example")

    # Add a subtitle
    board.write_sub_title("Demonstrating Component Functionality")

    # Add some text
    text_id = board.write_text("This is a sample paragraph demonstrating how to add text to the virtual board. You can use **bold** and *italic* directly in the text.")

    # Add a bold and italic text using Markdown syntax
    board.write_text("This text is **bold** and *italic* using Markdown syntax.")

    # Add a code block
    code_id = board.write_code_block(
        """def hello_world():\n    print(\"Hello, World!\")""",
        language="python",
        title="Python Example"
    )

    # Add a default table
    table_id = board.write_table(
        headers=["Name", "Age", "Occupation"],
        rows=[
            ["Alice", "30", "Engineer"],
            ["Bob", "25", "Designer"],
            ["Charlie", "35", "Doctor"],
        ],
    )

    # Add a table with numbered rows
    board.write_table(
        headers=["Task", "Status"],
        rows=[
            ["Implement feature A", "Done"],
            ["Fix bug B", "In Progress"],
            ["Write documentation", "To Do"],
        ],
        add_column_number=True,
    )

    # Add a table without the first column as header
    board.write_table(
        headers=["Product", "Price", "In Stock"],
        rows=[
            ["Laptop", "$1200", "Yes"],
            ["Mouse", "$25", "Yes"],
            ["Keyboard", "$75", "No"],
        ],
        first_column_as_header=False,
    )

    # Take a snapshot to see the initial board
    print("\n--- Initial Board ---")
    board.take_snapshot()

    # Demonstrate replacing a component
    print("\n--- Board After Component Replacement ---")
    board.write_text("This is the NEW text, replacing the original paragraph. It is now **bold**.", component_id=text_id)
    board.take_snapshot("After Text Replacement")

    # Demonstrate updating a table cell
    print("\n--- Board After Table Cell Update ---")
    table_component: TableComponent = cast(TableComponent, board.get_component(table_id))
    # Update Charlie's age. Row index 2, column index 1.
    table_component.update_cell(2, 1, "36")  # Update Charlie's age
    board.take_snapshot("After Table Cell Update")

    # Clear the board
    board.remove_snapshot()
    print("\nBoard cleared.")


if __name__ == "__main__":
    main()
