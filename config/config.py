"""Central test configuration for the automation suite."""


class Config:
    """Stores reusable application and credential values."""

    BASE_URL = "https://www.saucedemo.com/"
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    INVALID_USERNAME = "locked_out_user"
    INVALID_PASSWORD = "wrong_password"
    EXPLICIT_WAIT = 10
