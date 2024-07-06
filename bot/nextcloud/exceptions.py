"""Exception for Nextcloud services."""


class FsNodeNotFoundError(ValueError):
    """Raised when a file or directory is not found in the Nextcloud."""
