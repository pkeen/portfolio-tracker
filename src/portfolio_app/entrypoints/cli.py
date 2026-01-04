# src/portfolio_tracker/entrypoints/cli.py
import typer

app = typer.Typer()

@app.command()
def ping():
    print("portfolio-tracker is alive")

if __name__ == "__main__":
    app()
