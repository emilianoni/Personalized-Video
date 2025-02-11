from minio import Minio
from minio.error import S3Error
import json

# Load config.json
with open("./config.json") as config_file:
    config = json.load(config_file)

def download_file_from_minio(
    object_name, 
    file_path,
    endpoint = config["endpoint"], 
    access_key = config["access_key"], 
    secret_key = config["secret_key"], 
    bucket_name = config["bucket_name"]
):
    """
    Mendownload file dari bucket Minio.
    
    Args:
        endpoint (str): Hostname Minio server
        access_key (str): Access key Minio
        secret_key (str): Secret key Minio
        bucket_name (str): Nama bucket
        object_name (str): Nama file di dalam bucket
        file_path (str): Path lokal untuk menyimpan file
        secure (bool, optional): Gunakan HTTPS. Default True.
    """
    try:
        # Buat client Minio
        client = Minio(
            endpoint.replace('https://', '').replace('http://', ''),  # Remove protocol
            access_key=access_key,
            secret_key=secret_key,
            secure=True if 'https://' in endpoint else False
        )
        
        # Periksa apakah bucket ada
        if not client.bucket_exists(bucket_name):
            raise ValueError(f"Bucket {bucket_name} tidak ditemukan")
        
        # Download file
        client.fget_object(
            bucket_name, 
            object_name, 
            file_path
        )
        
        print(f"File {object_name} berhasil didownload ke {file_path}")
    
    except S3Error as e:
        print(f"Error S3: {e}")
    except Exception as e:
        print(f"Error umum: {e}")

# # Contoh penggunaan
# model_build = "arif"
# model_name = "modeltfvgg16.h5"
# # Download model file from minio
# download_file_from_minio(
#     object_name=f"deepfake/{model_build}/{model_name}",
#     file_path=f"../deepfake inference/model/{model_build}/{model_name}"
# )