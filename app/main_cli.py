import typer
from app.commands.charge_status import charge_status

app = typer.Typer()

app.command(name="charge-status")(charge_status)

if __name__ == "__main__":
    app()
