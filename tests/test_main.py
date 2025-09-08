from fastapi.testclient import TestClient
from src.main import app
from src.models.approval_status import ApprovalStatus, Status
from tests.utils.image_creation import create_high_contrast_image, create_test_image


client = TestClient(app)

def test_high_contrast_approved():
    """High contrast image should be approved."""

    # Arrange
    test_image = create_high_contrast_image()
    
    # Act
    response = client.post(
        "/creative-approval",
        files={"file": ("test_image.png", test_image, "image/png")},
        data={"metadata": "family,outdoor,advertising"}
    )

    approval_status = ApprovalStatus.model_validate_json(response.text)

    # Assert
    assert approval_status.status == Status.APPROVED
    assert approval_status.reasons == []

def test_low_contrast_rejection():
    """Low contrast image should be rejected."""

    # Arrange
    test_image = create_test_image()
    
    # Act
    response = client.post(
        "/creative-approval",
        files={"file": ("test_image.png", test_image, "image/png")},
        data={"metadata": "family,outdoor,advertising"}
    )

    approval_status = ApprovalStatus.model_validate_json(response.text)

    # Assert
    assert approval_status.status == Status.REJECTED
    assert "Image has insufficient contrast for quality standards" in approval_status.reasons

def test_wrong_file_type_error():
    """Happy path - High contrast image should be approved."""

    # Arrange
    test_image = create_test_image()
    
    # Act
    response = client.post(
        "/creative-approval",
        files={"file": ("test_file.txt", test_image, "text/plain")},
        data={"metadata": "family,outdoor,advertising"}
    )

    data = response.json()

    # Assert
    assert response.status_code == 422
    assert data["detail"] == "test_file.txt has an invalid file format. Allowed formats are .png, .jpeg, .jpg, .gif"