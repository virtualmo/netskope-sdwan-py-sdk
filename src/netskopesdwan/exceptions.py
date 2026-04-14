class SDWANError(Exception):
    """Base exception for the SDK."""


class ConfigurationError(SDWANError):
    """Raised when client configuration is invalid."""


class ResolutionError(SDWANError):
    """Raised when tenant or base URL resolution fails."""


class AuthenticationError(SDWANError):
    """Raised when API authentication fails."""


class PermissionDeniedError(SDWANError):
    """Raised when the caller lacks required permissions."""


class NotFoundError(SDWANError):
    """Raised when a resource cannot be found."""


class ValidationError(SDWANError):
    """Raised when the API rejects request data."""


class RateLimitError(SDWANError):
    """Raised when the API rate limit is exceeded."""


class APIResponseError(SDWANError):
    """Raised when the API returns an unexpected error response."""
