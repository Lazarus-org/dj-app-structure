import os
from typing import Dict, List
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A custom Django management command to create a predefined folder structure inside a specified app.

    This command removes default files created by the `startapp` command and creates a custom
    folder structure tailored for a more organized Django application.
    """

    help = "Create a custom folder structure inside an app"

    def add_arguments(self, parser) -> None:
        """
        Define the command-line arguments for this command.

        Args:
            parser (argparse.ArgumentParser): The argument parser to which arguments are added.
        """
        parser.add_argument(
            "app_name", type=str, help="The name of the app to create the structure in"
        )

    def handle(self, *args: str, **kwargs: str) -> None:
        """
        Handle the execution of the command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        app_name: str = kwargs["app_name"]
        base_dir: str = os.path.join(os.getcwd(), app_name)

        # Check if the app directory exists
        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR(f"App '{app_name}' does not exist"))
            return

        # Remove default files created by the `startapp` command
        self.remove_default_files(base_dir)

        # Define the custom folder structure
        structure: Dict[str, List[str]] = {
            "admin": [],
            "api": [
                "exceptions",
                "filters",
                "orderings",
                "paginations",
                "permissions",
                "schema",
                "routers",
                "serializers",
                "throttlings",
                "views",
            ],
            "models": ["helper"],
            "repository": ["manager", "queryset"],
            "signals": [],
            "tests": ["models", "api", "admin"],
            "validators": [],
        }

        # Create the folder structure
        self.create_folder_structure(base_dir, structure)

        # Special case for models/helper/enums
        enums_path: str = os.path.join(base_dir, "models", "helper", "enums")
        self.create_folder_with_init(enums_path)

        self.stdout.write(self.style.SUCCESS(f"Structure created for app '{app_name}'"))

    def remove_default_files(self, base_dir: str) -> None:
        """
        Remove default files created by the `startapp` command.

        Args:
            base_dir (str): The base directory of the app.
        """
        default_files: List[str] = ["models.py", "admin.py", "tests.py", "views.py"]
        for filename in default_files:
            file_path: str = os.path.join(base_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                self.stdout.write(self.style.WARNING(f"Removed {file_path}"))

    def create_folder_structure(self, base_dir: str, structure: Dict[str, List[str]]) -> None:
        """
        Create the folder structure based on the provided dictionary.

        Args:
            base_dir (str): The base directory of the app.
            structure (Dict[str, List[str]]): A dictionary representing the folder structure.
        """
        for folder, subfolders in structure.items():
            folder_path: str = os.path.join(base_dir, folder)
            self.create_folder_with_init(folder_path)
            for subfolder in subfolders:
                subfolder_path: str = os.path.join(folder_path, subfolder)
                self.create_folder_with_init(subfolder_path)

    def create_folder_with_init(self, path: str) -> None:
        """
        Create a folder and an empty `__init__.py` file if it doesn't already exist.

        Args:
            path (str): The path of the folder to create.
        """
        if not os.path.exists(path):
            os.makedirs(path)
            init_path: str = os.path.join(path, "__init__.py")
            with open(init_path, "w"):
                pass
            self.stdout.write(self.style.SUCCESS(f"Created {path}"))