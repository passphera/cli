import time

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress


MARKDOWN = """
# This is an h1
## This is an h2
### This is an h3
#### This is an h4
##### This is an h5
###### This is an h6

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item

- This is an unordered list item
- Yet another list item

python code
```python
h = list()
h.append(1)
```
java code
```java
class MainClass{
    public static void main(String[] args) {
        System.out.println(args[0]);
    }
}
```
"""


console = Console()


def main():
    # print(typer.style(f"Hello {name}!", "green"))
    # print(f"Hello {typer.style(name, 'green')}!")
    # print(f"Hello [bold italic underline green]{name}[/bold italic underline green] :house: :sunglasses: :warning-emoji: :red_heart-emoji: :red_heart-text:")
    # print("Visit my [blue blink][link=https://www.willmcgugan.com]blog[/link][/blue blink]!")
    md = Markdown(MARKDOWN)
    tree = Tree("[bold cyan]P")
    e1 = tree.add("C1-P")
    e2 = tree.add("C2-P")
    e1.add("CC1-C1-P")
    e1.add("CC2-C1-P").add("CCC1-CC2-C1-P")
    e1.add("CC3-C1-P")
    e2.add("CC1-C1-P")
    e2.add("CC2-C1-P")
    console.print(md)
    console.print(Panel("Hello [red]World!", title="Welcome Message", subtitle="First message"))
    # console.print(Panel.fit("Hello [red]World[/bold] Again!"))
    console.print(tree)
    with Progress() as progress:

        task1 = progress.add_task("[red]Downloading...", total=1000)
        task2 = progress.add_task("[green]Processing...", total=1000)
        task3 = progress.add_task("[cyan]Cooking...", total=1000)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.9)
            time.sleep(0.02)
    name: str = Prompt.ask("What is your name?")
    age: int = int(Prompt.ask("How old are you?"))
    if age < 18:
        if Confirm.ask("Are you sure you wish to continue?", default=False) is True:
            sex: str = Prompt.ask("What is your sex?", choices=["Male", "Female"], default="Male")
            degree: str = Prompt.ask("What is your degree?", choices=["License", "Master", "Phd"])
            table = Table("firstname", "age", "sex", "degree", show_header=True, header_style="bold cyan")
            table.add_row(name, str(age), sex, degree)
            console.print(table)
        else:
            console.print("You are too young.")
    else:
        sex: str = Prompt.ask("What is your sex?", choices=["Male", "Female"], default="Male")
        degree: str = Prompt.ask("What is your degree?", choices=["License", "Master", "Phd"])
        table = Table("firstname", "age", "sex", "degree", show_header=True, header_style="bold cyan")
        table.add_row(name, str(age), sex, degree)
        console.print(table)
    console.print("Goodbye")


if __name__ == "__main__":
    typer.run(main)
