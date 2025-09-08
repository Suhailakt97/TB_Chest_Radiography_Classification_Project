import os
import urllib.request as request
import shutil
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestinConfig
from pathlib import Path



class DataIngestion:
    def __init__(self, config: DataIngestinConfig):
        self.config = config

    def download_data(self):
            
        local_source = "artifacts/data_ingestion/TB_Chest_Radiography_Database"
        
        if os.path.exists(local_source):
            # Copy from local source
            if not os.path.exists(self.config.local_data_file):
                if os.path.isfile(local_source):
                    # If it's a single file
                    shutil.copy2(local_source, self.config.local_data_file)
                else:
                    # If it's a directory, copy the contents
                    os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
                    shutil.copytree(local_source, self.config.local_data_file)
                logger.info(f"File copied from local source: {local_source}")
            else:
                logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
        else:
            # Fallback to original download method
            if not os.path.exists(self.config.local_data_file):
                filename, header = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logger.info(f"File : {filename} downloaded with following info: \n{header}")
            else:
                logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
        

    def extract_zip_file(self):
        """
        Since your data is not a zip file, this method will verify the dataset structure
        Function returns None
        """
        # Create the unzip directory for consistency with the pipeline
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        
        # Verify the TB dataset structure
        if os.path.exists(self.config.local_data_file):
            normal_path = os.path.join(self.config.local_data_file, "normal")
            tuberculosis_path = os.path.join(self.config.local_data_file, "tuberculosis")
            
            if os.path.exists(normal_path) and os.path.exists(tuberculosis_path):
                normal_count = len(os.listdir(normal_path))
                tb_count = len(os.listdir(tuberculosis_path))