import typer
from rich.console import Console

err_console = Console(stderr=True)

app: typer.Typer = typer.Typer()


@app.command()
def create_habit(
    name: str = typer.Argument(default=..., help="Name of the habit"),
) -> None:
    """
    Command to create a new habit in the database.

    Args:

    """
    print(typer.style(f'Creating new habit "{name}".', fg="blue"))
    # TODO -> Implement the logic to create a new habit in the database
    print(typer.style(f'Habit "{name}" created successfully!', fg="green", bold=True))


@app.command()
def create_habit_category(
    name: str = typer.Argument(default=..., help="Name of the habit category"),
) -> None:
    """
    Command to create a new habit category in the database.

    Args:

    """
    print(typer.style(f'Creating new habit category "{name}".', fg="blue"))
    # TODO -> Implement the logic to create a new habit category in the database
    print(
        typer.style(
            f'Habit category "{name}" created successfully!', fg="green", bold=True
        )
    )


@app.command()
def create_habit_collection(
    name: str = typer.Argument(default=..., help="Name of the habit category"),
) -> None:
    """
    Command to create a new habit category in the database.

    Args:

    """
    print(typer.style(f'Creating new habit category "{name}".', fg="blue"))
    # TODO -> Implement the logic to create a new habit category in the database
    print(
        typer.style(
            f'Habit category "{name}" created successfully!', fg="green", bold=True
        )
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
