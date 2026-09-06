import inspect
from importlib.metadata import version

from dotenv import find_dotenv, load_dotenv


print(version("python-dotenv"))
print(inspect.signature(find_dotenv))
print(inspect.signature(load_dotenv))
