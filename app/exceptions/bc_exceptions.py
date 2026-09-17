class BusinessCentralAPIError(Exception):
    """Custom exception for Business Central API errors."""

    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(self.message)