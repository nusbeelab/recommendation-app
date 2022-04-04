from typing import Literal, Optional


def get_response(button: Optional[Literal["L", "R"]], left_option: bool):
    if button == None:
        return None
    if button == "L":
        return left_option
    if button == "R":
        return not left_option
    raise ValueError("Value of button must be 'L' or 'R' or None")
