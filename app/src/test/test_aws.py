from unittest.mock import patch, ANY
from mecklenburg.aws.setup import setup


def test_setup_with_dotenv(monkeypatch):
    with patch("mecklenburg.aws.setup.Path.exists", return_value=True):
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test_key")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test_secret")

        with patch("mecklenburg.aws.setup.boto3.client") as mock_boto_client:
            setup()

            mock_boto_client.assert_called_with(
                "s3",
                aws_access_key_id="test_key",
                aws_secret_access_key="test_secret",
                config=ANY,
            )


def test_setup_without_dotenv():
    with patch("mecklenburg.aws.setup.Path.exists", return_value=False):
        with patch("mecklenburg.aws.setup.boto3.client") as mock_boto_client:
            setup()
            mock_boto_client.assert_called_with("s3")
