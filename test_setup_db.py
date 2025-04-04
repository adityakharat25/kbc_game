import pytest
from unittest.mock import patch, MagicMock
import MySQLdb
from kbc_game import setup_db
 # Replace with your actual script filename (without .py)

@patch("MySQLdb.connect")
def test_setup_database_success(mock_connect):
    # Mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Call the function
    setup_db.setup_database()

    # Assert connection called with correct parameters
    mock_connect.assert_called_once_with(
        host=setup_db.DB_HOST,
        user=setup_db.DB_USER,
        password=setup_db.DB_PASSWORD,
        db=setup_db.TEST_DB_NAME
    )

    # Check if expected SQL commands were executed
    mock_cursor.execute.assert_any_call(f"CREATE DATABASE IF NOT EXISTS {setup_db.TEST_DB_NAME};")
    mock_cursor.execute.assert_any_call(f"USE {setup_db.TEST_DB_NAME};")
    assert mock_cursor.execute.called
    assert mock_conn.commit.called
    assert mock_cursor.close.called
    assert mock_conn.close.called

@patch("MySQLdb.connect", side_effect=MySQLdb.Error("Connection failed"))
def test_setup_database_failure(mock_connect, capsys):
    setup_db.setup_database()
    captured = capsys.readouterr()
    assert "Error" in captured.out
