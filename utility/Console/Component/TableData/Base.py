from typing import Any, List, Dict
from utility.Console.Base import ShellowMarkdownChildComponent


class TableData(ShellowMarkdownChildComponent):

    def bind(self) -> Any:
        return super().bind()

    def getFirstColumnAsHeader(
        self,
        data: str,
    ):
        return f"[bold]{data}[/bold]"

    def get_styled_headers(
        self, headers: List[str], first_column_as_header: bool
    ) -> List[Dict[str, str]]:
        styled_headers = []
        for i, header_content in enumerate(headers):
            if first_column_as_header and i == 0:
                styled_headers.append({"header": header_content, "style": "bold"})
            else:
                styled_headers.append({"header": header_content, "style": ""}) # Default unstyled
        return styled_headers

    def get_styled_rows(
        self,
        rows: List[List[str]],
        first_column_as_header: bool,
        add_column_number: bool,
    ) -> List[List[str]]:
        styled_rows = []
        for i, row_data in enumerate(rows):
            row_to_add = [str(i + 1)] + row_data if add_column_number else row_data

            processed_row = []
            for j, cell_content in enumerate(row_to_add):
                if first_column_as_header and j == 0:
                    processed_row.append(self.getFirstColumnAsHeader(cell_content))
                else:
                    processed_row.append(cell_content)
            styled_rows.append(processed_row)
        return styled_rows
