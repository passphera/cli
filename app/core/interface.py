from typing import Any, Union

from typer.rich_utils import Console, Panel, Table, Text, Theme, box

from app.core import config


custom_theme = Theme({
    'success': 'bold green',
    'info': 'bold cyan',
    'highlight': 'bold magenta',
    'warning': 'bold yellow',
    'error': 'bold red',
})


console: Console = Console(theme=custom_theme)


class Interface:
    @staticmethod
    def _create_panel(content: Any, title: str = None, style: str = 'info') -> Panel:
        return Panel.fit(content, title=title, title_align='left', border_style=style, box=box.ROUNDED)

    @classmethod
    def display_user_info(cls, user: dict[str, str]) -> None:
        info = Text()
        info.append('Username: ', style='highlight')
        info.append(user.get('username', 'N/A'))
        info.append("\nEmail: ", style="highlight")
        info.append(user.get('email', 'N/A'))
        console.print(cls._create_panel(info, "User Information"))

    @classmethod
    def display_password(cls, password: Union[dict[str, str], str], text: str = '', context: str = '') -> None:
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
        table.add_column("Context", style="cyan")
        table.add_column("Text", style="green")
        table.add_column("Password", style="yellow")
        if isinstance(password, dict):
            table.add_row(password.get('context', ''), password.get('text', ''), password.get('password', ''))
        else:
            table.add_row(context, text, password)
        console.print(cls._create_panel(table, "Password Information"))

    @classmethod
    def display_passwords(cls, passwords: list[dict[str, str]]):
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
        table.add_column("Context", style="cyan")
        table.add_column("Text", style="green")
        table.add_column("Password", style="yellow")
        for password in passwords:
            table.add_row(password.get('context', ''), password.get('text', ''), password.get('password', ''))
        console.print(cls._create_panel(table, "Stored Passwords"))

    @classmethod
    def display_character_replacement(cls, character: str, replacement: str) -> None:
        text = Text()
        text.append(character, style="cyan")
        text.append(" => ", style="yellow")
        text.append(replacement, style="green")
        console.print(cls._create_panel(text, "Generator Settings"))

    @classmethod
    def display_character_replacements(cls, replacements: dict[str, str]) -> None:
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
        table.add_column("Character", style="cyan")
        table.add_column("Replacement", style="green")

        for character, replacement in replacements.items():
            table.add_row(character, replacement)

        console.print(cls._create_panel(table, "Generator Settings"))

    @classmethod
    def display_message(cls, message: Text | str, title: str = '', style: str = 'info') -> None:
        if isinstance(message, Text):
            console.print(cls._create_panel(message, title=title, style=message.style))
        else:
            console.print(cls._create_panel(Text(message, style=style), title=title, style=style))

    @classmethod
    def display_version(cls) -> None:
        info = Text()
        info.append("Program: ", style="highlight")
        info.append(config.__name__)
        info.append("\nVersion: ", style="highlight")
        info.append(config.__version__)
        info.append("\nAuthor:  ", style="highlight")
        info.append(config.__author__)
        info.append("\nEmail:   ", style="highlight")
        info.append(config.__author_email__)
        console.print(cls._create_panel(info, "Version Information"))


class Messages:
    @staticmethod
    def _style_message(message: str, style: str) -> Text:
        return Text(message, style=style)

    SETTINGS_SYNCED = _style_message(
        "Settings synced successfully. All settings now match the cloud settings.",
        "success")
    COPIED_TO_CLIPBOARD = _style_message(
        "Your password has been copied to your clipboard. Just paste it.",
        "info")
    PASSWORD_REMOVED = _style_message(
        "This password was removed from memory. To restore it, please regenerate it.",
        "warning")
    HISTORY_CLEARED = _style_message(
        "The vault has been cleared. To restore it, you should have a backup or regenerate it.",
        "warning")
    INVALID_REPLACEMENT = _style_message(
        """Invalid replacement. Please choose another replacement.
    Allowed special characters: '!', '@', '$', '^', '-', '_', '=', '+', ',', '.', '/', ':'
    Disallowed special characters: '`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', ''', '"', '|', '\\'""",
        "error")

    @staticmethod
    def sync_vault(local: int, server: int) -> Text:
        message = Text()
        message.append("Database synced successfully\n", style="success")
        message.append(f"{local} local entries synced\n", style="info")
        message.append(f"{server} server entries synced", style="info")
        return message

    @staticmethod
    def context_error(context: str) -> Text:
        return Text(f"There is no password saved with the context '{context}'", style="error")

    @staticmethod
    def error(error: str) -> Text:
        return Text(f"{error}", style="error")
