"""
Water sort solver solver
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional
from collections import defaultdict

import justpy as jp  # type: ignore

# Puzzle solver classes
from puzzle import Puzzle
from bottle import Bottle
from puzzle_solver import PuzzleSolver, PuzzleChain

APP_TITLE: str = "water sort puzzle solver"
APP_FAVICON: str = "./jigsaw.ico"

MIN_NB_BOTTLES, MAX_NB_BOTTLES = 3, 20
MIN_NB_DOSES_PER_BOTTLE, MAX_NB_DOSES_PER_BOTTLE = 2, 6

# Type alias for JustPy object
JustPy_Page = Any  # JustPy HTML page
JustPy_Component = Any  # JustPy component on a page
JustPy_Message = Any  # JustPy message in a callback

# Tailwind class for message div component
div_message_classes = "text-xl border m-4 p-2"


@dataclass
class MyColor:
    """This class is used to store one possible puzzle color"""

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

        # Puzzle sizes
        # ------------
        # Number of bottles in the puzzle (including empty ones)
        self.nb_bottles: Optional[int] = None
        # Number of different doses (colors) per bottle
        self.nb_doses: Optional[int] = None
        # Div component with size inputs
        self.div_sizes: Optional[JustPy_Component] = None

        # Colors section
        # --------------
        # Div component with color buttons
        self.div_colors: Optional[JustPy_Component] = None
        # Div component for color message
        self.div_color_message: Optional[JustPy_Component] = None
        # Current color selected
        self.cur_color: Optional[MyColor] = None

        # Puzzle section
        # --------------
        # Div component with the puzzle
        self.div_my_puzzle: Optional[JustPy_Component] = None
        # Bottle objects in the puzzle
        self.bottles: list[MyBottle] = []
        # Div component for puzzle status message
        self.div_my_puzzle_status_message: Optional[JustPy_Component] = None

        # Puzzle solve section
        # --------------------
        # Button component for solving the puzzle
        self.button_my_puzzle_solve: Optional[JustPy_Component] = None

        # Explore solution section
        # ------------------------
        # Puzzle solver
        self.my_puzzle_solver: Optional[MyPuzzleSolver] = None
        # Div component to explore solution steps
        self.div_explore_solution: Optional[JustPy_Component] = None
        # Button to previous step
        self.button_explore_solution_previous: Optional[JustPy_Component] = None
        # Div component for current step
        self.div_explore_solution_message: Optional[JustPy_Component] = None
        # Button to next step
        self.button_explore_solution_next: Optional[JustPy_Component] = None

    def iter_on_bottles(self) -> Iterator[MyBottle]:
        """Iterator on all bottles in the puzzle"""
        for bottle in self.bottles:
            yield bottle

    def iter_on_bottle_doses(self) -> Iterator[tuple[MyBottle, JustPy_Component]]:
        """Iterator on all bottle/dose in the puzzle"""
        for bottle in self.iter_on_bottles():
            for dose in bottle.doses:
                yield bottle, dose

    def my_puzzle_status(self) -> tuple[bool, str]:
        """
        Return (True, "") when the puzzle is correct
        Return (False, "Message") when the puzzle is not fullfiled
        """
        if self.nb_doses is None:
            return False, "Nb doses per bottle not defined"

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


class MyPuzzleSolver:
    """Instance of MyPuzzleSolver does the puzzle solving"""

    def __init__(self, my_puzzle: MyPuzzle) -> None:
        self.my_puzzle: MyPuzzle = my_puzzle
        puzzle: Puzzle = self._create_puzzle(my_puzzle)
        solver: PuzzleSolver = PuzzleSolver(puzzle)
        solution: Optional[PuzzleChain] = solver.solve(
            nb_chains_without_empty_bottle=4,  # More human looklike solution...
            verbose_cycle=0,
        )
        self.solution_steps: Optional[list[PuzzleChain]] = None
        if solution is not None:
            self.solution_steps = solution.get_puzzle_chain_as_list()
        self.i_current_step = 0

    def _create_puzzle(self, my_puzzle: MyPuzzle) -> Puzzle:
        """Create the puzzle object from my_puzzle construction"""
        puzzle = Puzzle()
        if my_puzzle.nb_doses is not None:
            # TODO : Next line breaks the multi-session capability (need to refactor the Bottle module)
            Bottle.MAX_DOSES = my_puzzle.nb_doses
        for my_bottle in my_puzzle.iter_on_bottles():
            my_doses: list[Any] = []
            for my_dose in my_bottle.doses:
                if my_dose.color is None:
                    break
                else:
                    my_doses.append(my_dose.color.id)
            bottle = Bottle(my_doses)
            puzzle.add_bottle(bottle)
        return puzzle


def do_show_puzzle(my_puzzle: MyPuzzle, puzzle: Puzzle) -> None:
    """Show the puzzle"""
    for my_bottle, bottle in zip(my_puzzle.iter_on_bottles(), puzzle.iter_bottles()):
        for my_dose, id_color in zip(my_bottle.doses, bottle.doses):
            if id_color is None:
                do_update_bottle_dose_button_color(my_dose, None)
            else:
                my_color = get_my_color_from_id(id_color)
                do_update_bottle_dose_button_color(my_dose, my_color)


def do_show_solution_step(my_puzzle: MyPuzzle) -> None:
    """Show the current solution step"""
    if my_puzzle.my_puzzle_solver is None:
        return
    my_puzzle_solver: MyPuzzleSolver = my_puzzle.my_puzzle_solver
    i_current_step: int = my_puzzle_solver.i_current_step
    if my_puzzle_solver.solution_steps is None:
        return
    solution_steps: list[PuzzleChain] = my_puzzle_solver.solution_steps
    nb_steps: int = len(solution_steps)
    if i_current_step < 0:
        i_current_step = 0
    elif i_current_step >= nb_steps:
        i_current_step = nb_steps - 1
    step: PuzzleChain = solution_steps[i_current_step]

    if (
        my_puzzle.button_explore_solution_previous is not None
        and my_puzzle.div_explore_solution_message is not None
        and my_puzzle.button_explore_solution_next is not None
    ):

        if i_current_step == 0:
            # Show initial puzzle
            my_puzzle.button_explore_solution_previous.show = False
            my_puzzle.div_explore_solution_message.text = (
                f"The solution is {nb_steps - 1} steps long"
            )
            my_puzzle.button_explore_solution_next.show = True
        elif i_current_step == nb_steps - 1:
            # Show final step
            my_puzzle.button_explore_solution_previous.show = True
            my_puzzle.div_explore_solution_message.text = (
                f"{step.message} and it's done !"
            )
            my_puzzle.button_explore_solution_next.show = False
        else:
            # Show intermediate step
            my_puzzle.button_explore_solution_previous.show = True
            my_puzzle.div_explore_solution_message.text = (
                f"Step {i_current_step}/{nb_steps - 1} : {step.message}"
            )
            my_puzzle.button_explore_solution_next.show = True

        do_show_puzzle(my_puzzle, step.puzzle)


def button_explore_solution_previous_click(
    self: JustPy_Component, msg: JustPy_Message
) -> None:
    my_puzzle: MyPuzzle = msg.page.my_puzzle
    if my_puzzle.my_puzzle_solver is not None:
        my_puzzle.my_puzzle_solver.i_current_step -= 1
        do_show_solution_step(my_puzzle)


def button_explore_solution_next_click(
    self: JustPy_Component, msg: JustPy_Message
) -> None:
    my_puzzle: MyPuzzle = msg.page.my_puzzle
    if my_puzzle.my_puzzle_solver is not None:
        my_puzzle.my_puzzle_solver.i_current_step += 1
        do_show_solution_step(my_puzzle)


def button_my_puzzle_solve_click(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Click on the button for the current puzzle solving"""
    my_puzzle: MyPuzzle = msg.page.my_puzzle
    if (
        my_puzzle.my_puzzle_solver is None  # Avoid multiple reentrance
        and my_puzzle.button_my_puzzle_solve is not None
        and my_puzzle.div_my_puzzle_status_message is not None
    ):
        my_puzzle.button_my_puzzle_solve.show = False
        do_change_show_div_colors(my_puzzle, False)
        my_puzzle.my_puzzle_solver = MyPuzzleSolver(my_puzzle)
        if my_puzzle.my_puzzle_solver.solution_steps is None:
            my_puzzle.div_my_puzzle_status_message.text = "NO SOLUTION FOUND !"
        else:
            # Init explore solution
            my_puzzle.div_my_puzzle_status_message.show = False
            if my_puzzle.div_explore_solution is not None:
                my_puzzle.div_explore_solution.show = True
                do_show_solution_step(my_puzzle)


def do_update_my_puzzle_status_message(my_puzzle: MyPuzzle) -> None:
    """Update the puzzle status message"""
    if my_puzzle.div_my_puzzle_status_message is not None:
        ok, message = my_puzzle.my_puzzle_status()
        if ok:
            my_puzzle.div_my_puzzle_status_message.text = ""
            if my_puzzle.button_my_puzzle_solve is not None:
                my_puzzle.button_my_puzzle_solve.show = True
        else:
            my_puzzle.div_my_puzzle_status_message.text = message
            if my_puzzle.button_my_puzzle_solve is not None:
                my_puzzle.button_my_puzzle_solve.show = False


def do_update_bottle_dose_button_color(
    self: JustPy_Component, color: Optional[MyColor]
) -> None:
    self.color = color
    if color is not None:
        self.style = f"background-color: {color.html_color}"
    else:
        self.style = "color: white"
        self.set_class("bg-black")


def button_bottle_dose_click(self: JustPy_Component, msg: JustPy_Message):
    """Callback on a dose button in the puzzle"""
    if self.color is None and self.my_puzzle.cur_color is not None:
        do_update_bottle_dose_button_color(self, self.my_puzzle.cur_color)
    else:
        do_update_bottle_dose_button_color(self, None)

    do_update_my_puzzle_status_message(self.my_puzzle)


class MyBottle(jp.Div):
    """JustPy custom component for one bottle in the puzzle"""

    def __init__(self, my_puzzle: MyPuzzle, i_bottle: int, **kwargs) -> None:
        root = self

        super().__init__(
            text=f"Bottle #{i_bottle + 1}",
            classes="flex flex-col-reverse  m-2",
            **kwargs,
        )
        self.i_bottle: int = i_bottle
        self.my_puzzle: MyPuzzle = my_puzzle
        my_puzzle.bottles.append(self)
        self.doses: list[JustPy_Component] = []

        # Create dose buttons
        button_classes = "w-16 bg-black hover:bg-white text-white font-bold"
        if my_puzzle.nb_doses is not None:
            for i in range(my_puzzle.nb_doses):
                b = jp.Button(
                    text=f"{i + 1}",
                    a=root,
                    classes=button_classes,
                    click=button_bottle_dose_click,
                )
                b.my_puzzle = my_puzzle
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


def do_change_show_div_sizes(my_puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the input sizes"""
    if my_puzzle.div_sizes is not None:
        my_puzzle.div_sizes.show = show


def do_change_show_div_colors(my_puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the color selection"""
    if my_puzzle.div_colors is not None and my_puzzle.div_color_message is not None:
        my_puzzle.div_colors.show = show
        my_puzzle.div_color_message.show = show


def do_change_show_div_my_puzzle(my_puzzle: MyPuzzle, show: bool) -> None:
    """Change the visibility of the div containing the puzzle"""
    if my_puzzle.div_my_puzzle is not None:
        my_puzzle.div_my_puzzle.show = show


def color_click(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Click on a color button"""
    msg.page.my_puzzle.cur_color = self.color
    self.div_color_message.text = f"'{self.text}' color selected... Click on puzzle bottle doses 1 to {msg.page.my_puzzle.nb_doses} below..."
    self.div_color_message.style = f"color: {self.color.html_color}"


async def check_do_change_show_my_puzzle(msg: JustPy_Message) -> None:
    """Check during callback if size is defined.
    When defined, an empty puzzle is contructed and colors and puzzle is visible"""
    if (
        msg.page.my_puzzle.nb_bottles is not None
        and msg.page.my_puzzle.nb_doses is not None
    ):
        await my_puzzle_div_construction(msg.page.my_puzzle)
        do_change_show_div_sizes(msg.page.my_puzzle, False)
        do_change_show_div_colors(msg.page.my_puzzle, True)
        do_change_show_div_my_puzzle(msg.page.my_puzzle, True)


async def nb_bottles_change(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Callback on change the number of bottles"""
    if MIN_NB_BOTTLES <= self.value <= MAX_NB_BOTTLES:
        msg.page.my_puzzle.nb_bottles = self.value
        await check_do_change_show_my_puzzle(msg)
    else:
        self.div_message.text = (
            f"Number of bottles is in range {MIN_NB_BOTTLES} to {MAX_NB_BOTTLES} !"
        )


async def nb_doses_change(self: JustPy_Component, msg: JustPy_Message) -> None:
    """Callback on change the number of doses per bottle"""
    if MIN_NB_DOSES_PER_BOTTLE <= self.value <= MAX_NB_DOSES_PER_BOTTLE:
        msg.page.my_puzzle.nb_doses = self.value
        await check_do_change_show_my_puzzle(msg)
    else:
        self.div_message.text = f"Number of doses per bottle is in range {MIN_NB_DOSES_PER_BOTTLE} to {MAX_NB_DOSES_PER_BOTTLE} !"


async def my_puzzle_div_construction(my_puzzle: MyPuzzle) -> None:
    """Construct the puzzle once its size is known"""
    div_root = my_puzzle.div_my_puzzle

    # Puzzle section
    div_bottles = jp.Div(classes="flex m-2 flex-wrap", a=div_root)
    if my_puzzle.nb_bottles is not None:
        for i_bottle in range(my_puzzle.nb_bottles):
            MyBottle(
                my_puzzle=my_puzzle,
                i_bottle=i_bottle,
                a=div_bottles,
            )
        div_my_puzzle_status_message = jp.Div(
            text="... and click on bottle dose to set/unset the color",
            classes=div_message_classes,
            a=div_root,
        )
        my_puzzle.div_my_puzzle_status_message = div_my_puzzle_status_message

        # Puzzle solve section
        button_my_puzzle_solve = jp.Button(
            text="Solve it !",
            a=div_my_puzzle_status_message,
            classes="w-32 mr-2 mb-2 bg-green-400 hover:bg-green-600 font-bold py-2 px-4 rounded-full",
            click=button_my_puzzle_solve_click,
        )
        button_my_puzzle_solve.show = False
        my_puzzle.button_my_puzzle_solve = button_my_puzzle_solve

        # Explore solution section
        div_explore_solution = jp.Div(classes="inline-flex items-baseline", a=div_root)
        my_puzzle.div_explore_solution = div_explore_solution
        button_explore_classes = "w-64 h-12 mr-2 mb-2 bg-green-400 hover:bg-green-600 font-bold py-2 px-4 rounded-full"
        button_explore_solution_previous = jp.Button(
            text="Previous step",
            a=div_explore_solution,
            classes=button_explore_classes,
            click=button_explore_solution_previous_click,
        )
        my_puzzle.button_explore_solution_previous = button_explore_solution_previous
        div_explore_solution_message = jp.Div(
            text="Current step",
            classes=div_message_classes,
            a=div_explore_solution,
        )
        my_puzzle.div_explore_solution_message = div_explore_solution_message
        button_explore_solution_next = jp.Button(
            text="Next step",
            a=div_explore_solution,
            classes=button_explore_classes,
            click=button_explore_solution_next_click,
        )
        my_puzzle.button_explore_solution_next = button_explore_solution_next

        div_explore_solution.show = False

        await my_puzzle.page.update()


def my_puzzle_solver_construction() -> JustPy_Page:
    """Puzzle construction for justpy"""
    wp = jp.WebPage()
    wp.my_puzzle = MyPuzzle(wp)
    wp.title = APP_TITLE
    wp.favicon = APP_FAVICON

    # input number of bottles and bottle size (visible at the begining and hidden once defined)
    div_sizes = jp.Div(a=wp)
    wp.my_puzzle.div_sizes = div_sizes
    do_change_show_div_sizes(wp.my_puzzle, True)

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
    wp.my_puzzle.div_colors = div_colors

    button_color_classes = (
        "w-32 mr-2 mb-2 bg-black hover:bg-white font-bold py-2 px-4 rounded-full"
    )
    div_color_message = jp.Div(
        text="Click one of the above buttons to select a color...",
        classes=div_message_classes,
        a=wp,
    )
    wp.my_puzzle.div_color_message = div_color_message

    # color selector is hidden until size is defined
    do_change_show_div_colors(wp.my_puzzle, False)

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
    div_my_puzzle = jp.Div(a=wp)
    wp.my_puzzle.div_my_puzzle = div_my_puzzle
    do_change_show_div_my_puzzle(wp.my_puzzle, False)

    return wp


# This starts de HTML server
jp.justpy(my_puzzle_solver_construction, host="0.0.0.0", port=80)
