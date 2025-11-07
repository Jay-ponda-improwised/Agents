from typing import List, Dict, Any
from rich.table import Table
from utility.Console.Base import MarkdownComponent, MarkdownParentComponent
from utility.Console.Component.TableData.Base import TableData

class TableComponent(MarkdownComponent):
    """
    A component for tables.
    """

    def __init__(self, headers: List[str], rows: List[List[str]], first_column_as_header: bool = True, add_column_number: bool = False):
        super().__init__(
            {
                "headers": headers,
                "rows": rows,
                "first_column_as_header": first_column_as_header,
                "add_column_number": add_column_number
            }
        )
        self.table_data_processor = TableData()

    def bind(self) -> Table:
        table = Table(show_header=True, header_style="bold magenta")
        headers = self.data["headers"]
        rows = self.data["rows"]
        first_column_as_header = self.data["first_column_as_header"]
        add_column_number = self.data["add_column_number"]

        if add_column_number:
            if first_column_as_header:
                table.add_column("No.", style="bold")
            else:
                table.add_column("No.")
        
        should_style_first_header = first_column_as_header and not add_column_number
        styled_headers_data = self.table_data_processor.get_styled_headers(headers, should_style_first_header)
        for styled_header in styled_headers_data:
            table.add_column(styled_header["header"], style=styled_header["style"])

        styled_rows_data = self.table_data_processor.get_styled_rows(rows, first_column_as_header, add_column_number)
        for processed_row in styled_rows_data:
            table.add_row(*processed_row)

        return table

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the component.
        """
        return {
            "id": self._id,
            "type": self.__class__.__name__,
            "headers": self.data["headers"],
            "rows": self.data["rows"],
            "first_column_as_header": self.data["first_column_as_header"],
            "add_column_number": self.data["add_column_number"],
        }

    def update_cell(self, row_index: int, col_index: int, new_value: str):
        """
        Updates a specific cell in the table.
        """
        if row_index < 0 or row_index >= len(self.data["rows"]):
            raise IndexError("Row index out of range.")
        if col_index < 0 or col_index >= len(self.data["rows"][row_index]):
            raise IndexError("Column index out of range.")
        self.data["rows"][row_index][col_index] = new_value
