from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from pathlib import Path
from typing import Callable
from abc import ABC, abstractmethod

LOGO_PATH = r"api/email_service/static/job-search.png"


class SendEmail(ABC):
    """
    The base class for sending emails
    """
    def __init__(self, html_form: Callable):
        self.html_form = html_form
        self.data = dict()
        self.paths = [LOGO_PATH]
        self.body = ""

    @property
    def email_data(self) -> dict[any]:
        """
        The function via property returns information about the data of a given object
        """
        return self.data

    @email_data.setter
    def email_data(self, new_value: dict[any]):
        """
        The function via property updates the data in the dict of the given object
        """
        self.data.update(new_value)

    @property
    def file_paths(self) -> list[any]:
        """
        The function via property returns file paths
        """
        return self.paths

    @file_paths.setter
    def file_paths(self, new_value: list[str] | str):
        """
        The function via property adds paths to the variable
        """
        if isinstance(new_value, str):
            self.paths.append(new_value)
        elif isinstance(new_value, list):
            self.paths.extend(new_value)

    @abstractmethod
    def send_email(self) -> EmailMessage:
        """
        Send email. Add additional parameters if required
        """
        return self._get_obj()

    @abstractmethod
    def _get_obj(self):
        """
        Returns an email object with appropriate parameters
        """
        pass

    @abstractmethod
    def get_body(self):
        """
        It adds all the necessary data to the self.body variable
        """
        pass

    @staticmethod
    def _add_header_with_file(path: str) -> MIMEImage:
        """
        The function returns a header object that can be sent via email
        """
        with open(path, mode='rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', f"<{Path(path).name}>")
            return image
