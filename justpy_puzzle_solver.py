"""
WIP : water sort solver solver
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional
from collections import defaultdict

import justpy as jp  # type: ignore


APP_TITLE: str = "water sort puzzle solver"
APP_FAVICON: str = "./jigsaw.ico"

MAX_NB_BOTTLES = 20
MAX_NB_DOSES_PER_BOTTLE = 6

# Type alias for JustPy object
JustPy_Page = Any  # JustPy HTML page
JustPy_Component = Any  # JustPy component on a page
JustPy_Message = Any  # JustPy message in a callback

# Tailwind class for message div component
div_message_classes = "text-xl border m-4 p-2"


@dataclass
class MyColor:
    """This class is used to store one possible color for the puzzle"""

    id: int  # Unique color identifier
    html_color: str  # color name when talking to HTML component
    text_color: str  # color name when talking to the user


# List of all possible colors proposed to the user
ALL_COLORS: list[MyColor] = [
    MyColor(0, "yellow", "Yellow"),
    MyColor(1, "orange", "Orange"),
    MyColor(2, "pink", "Pink"),
    MyColor(3, "deeppink", "Deep pink"),
    MyColor(4, "red", "Red"),
    MyColor(5, "darkorchid", "Light purple"),
    MyColor(6, "magenta", "Magenta"),
    MyColor(7, "purple", "Purple"),
    MyColor(8, "lightgrey", "Light grey"),
    MyColor(9, "grey", "Grey"),
    MyColor(10, "aquamarine", "Light green"),
    MyColor(11, "chartreuse", "Green"),
    MyColor(12, "green", "Dark green"),
    MyColor(13, "cyan", "Light blue"),
    MyColor(14, "cornflowerblue", "Blue"),
    MyColor(15, "blue", "Dark blue"),
    MyColor(16, "chocolate", "Light brown"),
    MyColor(17, "brown", "Brown"),
]


def get_my_color_from_id(id: int) -> MyColor:
    """Return a MyColor instance having a specific id color"""
    for color in ALL_COLORS:
        if color.id == id:
            return color
    return MyColor(id, "black", "Black")


class MyPuzzle:
    """Instance of MyPuzzle holds the current puzzle properties"""

    def __init__(self, page: JustPy_Page) -> None:
        self.page = page
        self.nb_bottles: Optional[
            int
        ] = None  # Number of bottles in the puzzle (including empty ones)
        self.nb_doses: Optional[
            int
        ] = None  # Nomber of different doses (colors) per bottle
        self.div_sizes: Optional[
            JustPy_Component
        ] = None  # Div component with size inputs
        self.div_colors: Optional[
            JustPy_Component
        ] = None  # Div component with color buttons
        self.div_color_message: Optional[
            JustPy_Component
        ] = None  # Div component for color message
        self.div_puzzle: Optional[
            JustPy_Component
        ] = None  # Div component with the puzzle
        self.cur_color: Optional[MyColor] = None  # Current color selected
        self.bottles: list[MyBottle] = []  # Bottle objects in the puzzle
        self.div_puzzle_status_message: Optional[
            JustPy_Component
        ] = None  # Div component for puzzle status message
        self.button_puzzle_solve: Optional[
            JustPy_Component
        ] = None  # Button component for solving the puzzle

    def iter_on_bottles(self) -> Iterator[MyBottle]:
        """Iterator on all bottles in the puzzle"""
        for bottle in self.bottles:
            yield bottle

    def iter_on_bottle_doses(self) -> Iterator[tuple[MyBottle, JustPy_Component]]:
        """Iterator on all bottle/dose in the puzzle"""
        for bottle in self.iter_on_bottles():
            for dose in bottle.doses:
                yield bottle, dose

    def puzzle_status(self) -> tuple[bool, str]:
        """
        Return (True, "") when the puzzle is correct
        Return (False, "Message") when the puzzle is not fullfiled
        """
        if self.nb_doses is not None:
            # Count empty and colored doses
            nb_empty_doses: int = 0
            id_color_counter: dict[int, int] = defaultdict(int)
            for _, dose in self.iter_on_bottle_doses():
                if dose.color is None:
                    nb_empty_doses += 1
                else:
                    id_color_counter[dose.color.id] += 1
            # Check for empty doses
            if nb_empty_doses < self.nb_doses:
                return False, "There is not enough empty doses in this puzzle..."
            # Check for color dose number to be fullfiled
            for id_color, nb in id_color_counter.items():
                if nb % self.nb_doses != 0:
                    missing_dose = self.nb_doses - (nb % self.nb_doses)
                    missing_color = get_my_color_from_id(id_color)
                    return (
                        False,
                        f"{missing_color.text_color} color needs {missing_dose} more doses...",
                    )
            # Check for at least one color
            if len(id_color_counter) == 0:
                return (
                    False,
                    "Select a color and click on bottle to define colors in the puzzle",
                )
            # Check each bottle is correctly fullfiled
            for bottle in self.iter_on_bottles():
                if not bottle.is_correctly_fullfiled():
                    return (
                        False,
                        f"The bottle #{bottle.i_bottle + 1} is not correctly fullfiled",
                    )
            # Else, the puzzle is solvable
            return True, "Puzzle OK"
        else:
            return False, "Nb doses per bottle is not defined"


def button_puzzle_solve_click(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Click on the button for the current puzzle solving"""
    print("SOLVE IT !")


def do_update_puzzle_status_message(puzzle: MyPuzzle) -> None:
    """Update the puzzle status message"""
    if puzzle.div_puzzle_status_message is not None:
        ok, message = puzzle.puzzle_status()
        if ok:
            puzzle.div_puzzle_status_message.text = ""
            if puzzle.button_puzzle_solve is not None:
                puzzle.button_puzzle_solve.show = True
        else:
            puzzle.div_puzzle_status_message.text = message
            if puzzle.button_puzzle_solve is not None:
                puzzle.button_puzzle_solve.show = False


def do_update_bottle_dose_button(self: JustPy_Component) -> None:
    """Update the button component of a bottle dose"""
    if self.color is None and self.puzzle.cur_color is not None:
        self.color = self.puzzle.cur_color
        self.style = f"background-color: {self.puzzle.cur_color.html_color}"
    else:
        self.color = None
        self.style = "color: white"
        self.set_class("bg-black")

    do_update_puzzle_status_message(self.puzzle)


def button_bottle_dose_click(self: JustPy_Component, msg: JustPy_Message):
    """Callback on a dose button in the puzzle"""
    do_update_bottle_dose_button(self)


class MyBottle(jp.Div):
    """JustPy custom component for one bottle in the puzzle"""

    def __init__(self, puzzle: MyPuzzle, i_bottle: int, **kwargs) -> None:
        root = self

        super().__init__(
            text=f"Bottle #{i_bottle + 1}",
            classes="flex flex-col-reverse  m-2",
            **kwargs,
        )
        self.i_bottle: int = i_bottle
        self.puzzle: MyPuzzle = puzzle
        puzzle.bottles.append(self)
        self.doses: list[JustPy_Component] = []

        # Create dose buttons
        button_classes = "w-16 bg-black hover:bg-white text-white font-bold"
        if puzzle.nb_doses is not None:
            for i in range(puzzle.nb_doses):
                b = jp.Button(
                    text=f"{i + 1}",
                    a=root,
                    classes=button_classes,
                    click=button_bottle_dose_click,
                )
                b.puzzle = puzzle
                self.doses.append(b)
                b.i_dose = i
                b.color = None

    def is_correctly_fullfiled(self) -> bool:
        """Return True if there is no empty dose below a colored dose"""
        dose_can_be_colored: bool = True
        for dose in self.doses:
            if dose.color is None:
                dose_can_be_colored = False
            elif not dose_can_be_colored:
                return False
        return True


def do_change_show_div_sizes(puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the input sizes"""
    if puzzle.div_sizes is not None:
        puzzle.div_sizes.show = show  # type: ignore


def do_change_show_div_colors(puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the color selection"""
    if puzzle.div_colors is not None:
        puzzle.div_colors.show = show  # type: ignore
        puzzle.div_color_message.show = show  # type: ignore


def do_change_show_div_puzzle(puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the puzzle"""
    if puzzle.div_puzzle is not None:
        puzzle.div_puzzle.show = show  # type: ignore


def color_click(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Click on a color button"""
    msg.page.puzzle.cur_color = self.color
    self.div_color_message.text = f"'{self.text}' color selected... Click on puzzle bottle doses 1 to {msg.page.puzzle.nb_doses} below..."
    self.div_color_message.style = f"color: {self.color.html_color}"


async def check_do_change_show_puzzle(msg: JustPy_Message) -> None:
    """Check during callback if size is defined.
    When defined, an empty puzzle is contructed and colors and puzzle is visible"""
    if msg.page.puzzle.nb_bottles is not None and msg.page.puzzle.nb_doses is not None:
        await puzzle_div_construction(msg.page.puzzle)
        do_change_show_div_sizes(msg.page.puzzle, False)
        do_change_show_div_colors(msg.page.puzzle, True)
        do_change_show_div_puzzle(msg.page.puzzle, True)


async def nb_bottles_change(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Callback on change the number of bottles"""
    if 1 <= self.value <= MAX_NB_BOTTLES:
        msg.page.puzzle.nb_bottles = self.value
        await check_do_change_show_puzzle(msg)
    else:
        self.div_message.text = f"Number of bottles is in range 1 to {MAX_NB_BOTTLES} !"


async def nb_doses_change(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Callback on change the number of doses per bottle"""
    if 1 <= self.value <= MAX_NB_DOSES_PER_BOTTLE:
        msg.page.puzzle.nb_doses = self.value
        await check_do_change_show_puzzle(msg)
    else:
        self.div_message.text = (
            f"Number of doses per bottle is in range 1 to {MAX_NB_DOSES_PER_BOTTLE} !"
        )


async def puzzle_div_construction(puzzle: MyPuzzle) -> None:
    """Construct the puzzle once its size is known"""
    div_root = puzzle.div_puzzle
    div_bottles = jp.Div(classes="flex m-2 flex-wrap", a=div_root)
    if puzzle.nb_bottles is not None:
        for i_bottle in range(puzzle.nb_bottles):
            MyBottle(
                puzzle=puzzle,
                i_bottle=i_bottle,
                a=div_bottles,
            )
        div_puzzle_status_message = jp.Div(
            text="... and click on bottle dose to set/unset the color",
            classes=div_message_classes,
            a=div_root,
        )
        puzzle.div_puzzle_status_message = div_puzzle_status_message
        button_puzzle_solve = jp.Button(
            text="Solve it !",
            a=div_puzzle_status_message,
            classes="w-32 mr-2 mb-2 bg-green-400 hover:bg-green-600 font-bold py-2 px-4 rounded-full",
            click=button_puzzle_solve_click,
        )
        button_puzzle_solve.show = False
        puzzle.button_puzzle_solve = button_puzzle_solve
        await puzzle.page.update()


def puzzle_solver_construction() -> JustPy_Page:
    """Puzzle construction for justpy"""
    wp = jp.WebPage()
    wp.puzzle = MyPuzzle(wp)
    wp.title = APP_TITLE
    wp.favicon = APP_FAVICON

    # input number of bottles and bottle size (visible at the begining and hidden once defined)
    div_sizes = jp.Div(a=wp)
    wp.puzzle.div_sizes = div_sizes
    do_change_show_div_sizes(wp.puzzle, True)

    div_sizes_message = jp.Div(
        text="First, define the puzzle size with the total number of bottles (including empty ones) "
        "and the number of different possible doses (or colors) per bottle...",
        classes=div_message_classes,
        a=div_sizes,
    )
    div_sizes = jp.Div(classes="flex m-4 flex-wrap", a=div_sizes)
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    # Total number of bottles
    input_nb_bottles = jp.Input(
        type="number", a=div_sizes, classes=input_classes, placeholder="Nb bottles"
    )
    input_nb_bottles.on("change", nb_bottles_change)
    input_nb_bottles.div_message = div_sizes_message

    # Nb doses per bottle
    input_nb_doses = jp.Input(
        type="number",
        a=div_sizes,
        classes=input_classes,
        placeholder="Nb doses per bottle",
    )
    input_nb_doses.on("change", nb_doses_change)
    input_nb_doses.div_message = div_sizes_message

    # create the color div selector
    div_colors = jp.Div(classes="flex m-4 flex-wrap", a=wp)
    wp.puzzle.div_colors = div_colors

    button_color_classes = (
        "w-32 mr-2 mb-2 bg-black hover:bg-white font-bold py-2 px-4 rounded-full"
    )
    div_color_message = jp.Div(
        text="Click one of the above buttons to select a color...",
        classes=div_message_classes,
        a=wp,
    )
    wp.puzzle.div_color_message = div_color_message

    # color selector is hidden until size is defined
    do_change_show_div_colors(wp.puzzle, False)

    # create a button for each possible colors
    for color in ALL_COLORS:
        b = jp.Button(
            text=f"{color.text_color}",
            a=div_colors,
            classes=button_color_classes,
            click=color_click,
        )
        b.style = f"color: {color.html_color}"
        b.color = color
        b.div_color_message = div_color_message

    jp.Hr(a=wp)  # Add horizontal like to page

    # create the puzzle div (hidden until size is defined)
    div_puzzle = jp.Div(a=wp)
    wp.puzzle.div_puzzle = div_puzzle
    do_change_show_div_puzzle(wp.puzzle, False)

    return wp


# This starts de HTML server
jp.justpy(puzzle_solver_construction, host="0.0.0.0", port=80)
