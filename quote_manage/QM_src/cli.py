import click
import os
import logging
from .database import init_db, get_db
from .models import Quote
import json
import random
from sqlalchemy import func

def create_log_file(log_file_name:str, error_log_file_name:str, var_dir:str):
    """
    The Function to create a log file

    """
    if isinstance(log_file_name, str) == True \
        and isinstance(error_log_file_name, str) == True \
            and isinstance(var_dir, str) == True:
        
        if log_file_name.endswith(".log") == True \
            and error_log_file_name.endswith(".log") == True:

            curr_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(curr_dir)
            var_dir = os.path.join(base_dir, var_dir)

            if not os.path.exists(var_dir):
                os.makedirs(var_dir)
            log_dir = os.path.join(var_dir, "log")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file_path = os.path.join(log_dir, log_file_name)
            if not os.path.exists(log_file_path):
                with open(log_file_path, "w") as f:
                    f.write("")
            
            error_log_file_path = os.path.join(log_dir, error_log_file_name)
            if not os.path.exists(error_log_file_path):
                with open(error_log_file_path, "w") as f:
                    f.write("")

            return log_file_path, error_log_file_path
        else:
            raise ValueError("wrong format, try log files are allowed")

    else:
        raise ValueError("wrong  arguments ,arguments must be strings")


log_file_name = "quote_manager.log"
error_log_file_name = "quote_manager_error.log"
var_dir = "var"

log_file_path, error_log_file_path = create_log_file(log_file_name, error_log_file_name, var_dir)

#set up logging
logging.basicConfig(filename= log_file_path, 
                    level=logging.INFO,
                    format= '%(asctime)s %(levelname)s %(name)s %(message)s')

error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(error_log_file_path)
error_logger.addHandler(error_handler)###

@click.group()
def cli():
    """Quote Manager CLI"""
    pass

@cli.command()
@click.option('--category', prompt='Enter the category', help='The category of the quote',required=True)
@click.option('--quote', prompt='Enter the quote text', help='The text of the quote',required=True)
@click.option('--author', prompt='Enter the author', help='The author of the quote',required=True)

def add(category:str,
                  quote:str,
                  author):
    """
    include the  new quote to the database if the quote and category are provided
    
    """
    try:
        with get_db() as db:
            if quote and category:
                new_quote = Quote(category=category, quote=quote, author = author)
                db.add(new_quote)
                db.commit()

                click.echo({"status": "success, quote added successfully",
                            "quote": quote,
                            "category": category,
                            "author": author
                            })
                logging.info(f"New quote: {quote} added successfully")

            else:
                click.echo("Please provide a quote and a category")
                error_logger.error("Please provide a quote and a category")

    except Exception as e:
        click.echo(f"Error occurred during database operation: {str(e)}")
        error_logger.error(f"Error occurred during database operation: {str(e)}")

@cli.command()
@click.option("--category", default=None, help="Category of the quote")
def list_quotes(category:str):
    """
    provide  5 random quotes in the database 
    
    """
    try:
        with get_db() as db:
            if category:
                quotes = db.query(Quote).filter(Quote.category == category).all()
                quotes = random.choices(quotes, k=5)
            else:
                quotes = db.query(Quote).all()
                # print("quotes", quotes)
                quotes = random.choices(quotes, k=5)

            if quotes:
                for quote in quotes:
                    click.echo({
                        "quote": quote.quote,
                        "author": quote.author,
                        "category": quote.category
                    })
            else:
                click.echo("No quotes found.")
                error_logger.error("No quotes found in the database")
    except Exception as e:
        click.echo(f"Error occurred during database operation: {str(e)}")
        error_logger.error(f"Error occurred during database operation: {str(e)}")

#@cli.command()
#@click.option('--category', help='Filter quotes by category')
#@click.option('--limit', default=5, help='Number of quotes to list (default: 5)')


if __name__ == '__main__':
    cli()