"""
Need to load all the commands when package is imported in order for sublime to
register all the commands
"""
from .insert_kata import InsertProblemViewCommand, InsertTestFixtureCommand
from .start_kata import StartKataCommand
from .submit_kata import SubmitProblemCommand
