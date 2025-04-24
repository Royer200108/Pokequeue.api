import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

class ABlob:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)
    
    def generate_sas(self, id:int):
        """
        Generate a SAS token for a blob in the Azure Storage container.
        """
        blob_name = f"poke_report_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=AZURE_STORAGE_CONTAINER,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True, delete=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return sas_token
    
    def delete_blob(self, id: int):
        """
        Delete a blob from Azure Storage container.
        
        Args:
            id: The ID used to generate the blob name (poke_report_{id}.csv)
            
        Returns:
            bool: True if deletion was successful, False if blob wasn't found
        Raises:
            Exception: For other Azure-related errors
        """
        blob_name = f"poke_report_{id}.csv"
        try:
            #Crear el cliente del blob
            blob_client = self.blob_service_client.get_blob_client(
                container=AZURE_STORAGE_CONTAINER,
                blob=blob_name
            )
            blob_client.delete_blob()
            return True
        except Exception as e:
            # Specifically handle blob not found error
            if "BlobNotFound" in str(e):
                print(f"Blob {blob_name} not found for deletion.")
                return False
            # Re-raise other exceptions
            print(f"Error deleting blob {blob_name}: {str(e)}")
            raise