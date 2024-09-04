import pytest,os
from click.testing import CliRunner
from QM_src.cli import cli
from QM_src.database import init_db, get_db
from QM_src.models import Quote

@pytest.fixture(scope="function")
def runner():
    return CliRunner()

@pytest.fixture(scope="function")
def test_db():
    init_db()
    db = next(get_db())
    yield db
    db.close()

def test_add_quote(runner, test_db):
    result = runner.invoke(cli, ['add'], input='Test quote\nTest author\n')
    assert result.exit_code == 0
    assert 'Added quote' in result.output

    quotes = test_db.query(Quote).all()
    assert len(quotes) == 1
    assert quotes[0].text == 'Test quote'
    assert quotes[0].author == 'Test author'

def test_list_quotes(runner, test_db):
    test_db.add(Quote(text='Test quote', author='Test author'))
    test_db.commit()

    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'Test quote' in result.output
    assert 'Test author' in result.output