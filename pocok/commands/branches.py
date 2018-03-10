from .abstract_command import AbstractCommand
from ..services.state_utils import StateUtils
from ..services.state import StateHolder
from ..services.console_logger import ColorPrint
from ..services.file_utils import FileUtils


class Branches(AbstractCommand):

    command = "branches"
    args = ["[<name>]"]
    args_descriptions = {"[<name>]": "Name of the project in the catalog."}
    description = "Run: 'pocok branches nginx' to list all available git branches of the 'nginx' project."

    def prepare_states(self):
        StateHolder.name = FileUtils.get_parameter_or_directory_name('<name>')
        StateUtils.prepare("project_repo")

    def resolve_dependencies(self):
        StateUtils.check_variable('repository')

    def execute(self):
        StateHolder.repository.print_branches()
