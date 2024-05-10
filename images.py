from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

account_url = "https://<this info is specific for my account so it is sensitive>.blob.core.windows.net"
default_credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url, credential=default_credential)


def upload_image(image, image_path):
    blob_client = blob_service_client.get_blob_client(
        container=image_path, blob=image_path
    )

    blob_client.upload_blob(image)
