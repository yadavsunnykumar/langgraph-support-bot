"""Custom exception classes for clearer error handling."""


class SupportBotError(Exception):
    """Base exception for all support bot errors."""
    pass


class ClassificationError(SupportBotError):
    """Raised when intent classification fails."""
    pass


class AgentError(SupportBotError):
    """Raised when a specialist agent fails."""
    pass


class ConfigurationError(SupportBotError):
    """Raised when required config is missing or invalid."""
    pass