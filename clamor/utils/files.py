from base64 import b64encode
from io import IOBase
from typing import Optional, Union

import asks

__all__ = (
    'File',
)


def _get_image_mime_type(image_data: bytes) -> str:
    if image_data.startswith(b'\xFF\xD8') and image_data.rstrip(b'\0').endswith(b'\xFF\xD9'):
        return 'jpeg'
    elif image_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'png'
    elif image_data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'gif'
    elif image_data.startswith(b'RIFF') and image_data[8:12] == b'WEBP':
        return 'webp'
    else:
        raise TypeError('Unsupported image type given')


class File:
    """
    Files that are usable in Discord.

    Discord requires that files be sent in specific ways, so we can't just stuff a random file into
    a request and expect it to be attached. To solve this issue, you can use this class to take
    in a file, or it can download a file from a url. Then it will turn whatever file you put in
    into the kind of file discord expects.

    Attributes
    ----------
    data : bytes
        The file contents in bytes
    file_type : str
        The file extension (png, txt, pdf, etc)
    file_name : str
        The name of the file, excluding the extension
    data_url : str
        The file in the data URI scheme (file type must be set)
    name : str
        The full name of the file (name + extension)
    """

    def __init__(self, data: bytes, file_type: Optional[str] = None, file_name: str = "file"):
        self.data = data
        self.file_type = file_type
        self.file_name = file_name

    @property
    def data_uri(self) -> Optional[str]:
        """Returns the URI scheme for avatars in case this is an image.

        Said scheme has the following format:

        .. code-block::

            data:image/{file_extension};base64,{base64_encoded_image_data}

        Raises
        ------
        TypeError
            Raised in case this is not an image.
        ValueError
            Raised if the image data this class holds is likely corrupt.
        """

        extension = self.file_type
        if extension == 'jpg':
            extension = 'jpeg'

        real_extension = _get_image_mime_type(self.data)
        if extension != real_extension:
            raise ValueError('Likely a corrupt file')

        return "data:image/" + extension + ";base64," + b64encode(self.data).decode('ascii')

    @property
    def name(self):
        return self.file_name + "." + (self.file_type or "")

    @classmethod
    def from_file(cls, file: Union[str, IOBase]):
        """
        Creates a Discord file from local file.

        Generates a File class from a local file. You can provide either the path to the file, or
        the file object itself.

        Parameters
        ----------
        file : str, io.IOBase
            A path to a file, or a file object (Not just any stream!)

        Returns
        -------
        :class:`clamor.utils.files.File`
            A discord usable file object
        """

        if isinstance(file, str):
            with open(file, "rb") as new_file:
                return cls.from_file(new_file)

        if '.' not in file.name:
            name, extension = file.name, None
        else:
            name, extension = file.name.rsplit(".", 1)

        return cls(file.read(), extension, name)

    @classmethod
    async def from_url(cls, target_url: str, file_name: str = None):
        """
        Creates a Discord file from its URL.

        This function will download a file from the provided URL, and return a discord usable file
        based off that. Because files need to have names, this function has several different
        strategies to solve that issue. First, if a file name is provided, it will use that. If the
        provided file name doesn't have an extension it will check the response's Content-Type
        header. If a name is not provided at all, it will use the name from the url path. If the
        path doesn't have an extension it will once again check the Content-Type header. If all
        else fails your computer will in fact explode and you should have provided a file name.

        Parameters
        ----------
        target_url : str
            The place we'll download the file from
        file_name : str or None
            The file name

        Returns
        -------
        :class:`clamor.utils.files.File`
            A discord usable file object
        """

        resp = await asks.get(target_url)
        if not file_name:
            _, file_name = target_url.rsplit('/', 1)

        if '.' not in file_name and "Content-Type" in resp.headers:
            name, extension = file_name, resp.headers['Content-Type'].split('/')[1]
        elif '.' not in file_name:
            name, extension = file_name, None
        else:
            name, extension = file_name.rsplit('.', 1)

        return cls(resp.content, extension, file_name)
