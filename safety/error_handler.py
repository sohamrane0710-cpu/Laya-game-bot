
class ErrorHandler:
    """
    Defines bounded recovery behavior for the first agent.
    """

    def __init__(self, logger, max_consecutive_errors=3):
        self.logger = logger
        self.max_consecutive_errors = (
            max_consecutive_errors
        )
        self.consecutive_errors = 0

    def report_success(self):
        self.consecutive_errors = 0

    def recover(self, error, context=None):
        self.consecutive_errors += 1

        self.logger.error(
            "Agent operation failed",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            consecutive_errors=self.consecutive_errors,
        )

        if (
            self.consecutive_errors
            >= self.max_consecutive_errors
        ):
            self.logger.error(
                "Stopping after repeated failures"
            )
            return False

        return True
