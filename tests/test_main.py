from fastapi.testclient import TestClient
from src.main import app
from src.models.approval_status import Status
from tests.utils.image_creation import create_high_contrast_image


client = TestClient(app)

def test_happy_path_approval():
    """Happy path - High contrast image should be approved."""

    # Arrange
    test_image = create_high_contrast_image()
    
    # Act
    response = client.post(
        "/creative-approval",
        files={"file": ("test_image.png", test_image.getvalue(), "image/png")},
        data={"metadata": "family,outdoor,advertising"}
    )

    data = response.json()

    # Assert
    assert data["status"] == Status.APPROVED.value
    assert len(data["reasons"]) == 0