import kagglehub
import os
present_dir = os.getcwd()

# Download latest version
path = kagglehub.dataset_download("puneet6060/intel-image-classification", output_dir=present_dir+"/dataset")

print("Path to dataset files:", path)