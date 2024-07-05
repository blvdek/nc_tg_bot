"""Exception for Nextcloud factory."""


class ClassNotFoundError(ValueError):
    """Called when a class is not found by the class factory."""


class FsNodeNotFoundError(ValueError):
    """Raised when a file or directory is not found in the Nextcloud."""
