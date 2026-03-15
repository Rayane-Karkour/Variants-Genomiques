import requests
import os
import gzip
import shutil

URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz"
OUTPUT = "data/clinvar.vcf.gz"

def download_clinvar():
    data_folder = "data/"
    gz_file  = os.path.join(data_folder, "clinvar.vcf.gz")
    output_file = os.path.join(data_folder, "clinvar.vcf")

    print("Downloading...")
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(gz_file, "wb") as f:
            for chunk in r.iter_content():
                f.write(chunk)

    print("Unzipping...")
    with gzip.open(gz_file, "rb") as f_in:
        with open(output_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(gz_file)



if __name__ == "__main__":
    download_clinvar()