from app import app, db
import click
@app.cli.command("init")
def init():
    db.create_all()
    click.echo("Database created successfully!")
if __name__ == "__main__":
    from flask.cli import main
    main()