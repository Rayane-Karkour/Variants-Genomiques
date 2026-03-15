import os
import re
import pandas as pd
import numpy as np


DOCS = "../docs/info.txt"
CLINVAR_FILE = "../../data/clinvar.vcf"

KEEP_FIELDS = [
    'CHROM',
    'POS',
    'ID',
    'REF',
    'ALT',
    'CLNVC',
    'ALLELEID',
    'GENEINFO',
    'CLNSIG',
    'CLNREVSTAT',
    'CLNDN',
    'MC',
    'ORIGIN',
    'RS',
]


def parse_info_field(info_str):
    result = {}
    infos = info_str.split(';')
    for item in infos :
        col, val = item.split('=', 1)
        result[col] = val
    return result

def get_info(line):
    match = re.search(r'ID=([^,]+).*Description="([^"]+)"', line)
    if match:
        id_value = match.group(1)
        desc_value = match.group(2)
        with open(DOCS, "a") as f:
            f.write(f"{id_value:<15} : {desc_value}\n")

def parse_vcf(vcf_path, max_rows=None, keep_only=None):
    records = []
    count = 0
    if os.path.exists(DOCS):
        os.remove(DOCS)
    else: 
        open(DOCS, 'w').close()
    with open(vcf_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):  # Skip metadata
                if line.startswith('##INFO'):
                    get_info(line)
                continue
            split_line = re.split(r'[\t]+', line.strip())
            #print(split_line)
            count += 1
            
            #First few column are always the same
            data = {
                'CHROM':  split_line[0],
                'POS':    int(split_line[1]),
                'ID':     split_line[2],
                'REF':    split_line[3],
                'ALT':    split_line[4],
                'QUAL':   split_line[5],
                'FILTER': split_line[6],
            }
            
            info = split_line[7]
            data.update(parse_info_field(info))
            records.append(data)
            #print(data)
            if max_rows != None and count >= max_rows:
                break
    df = pd.DataFrame(records)
    if keep_only:
        df = df[keep_only]
    return df


# df = parse_vcf(CLINVAR_FILE, max_rows=100, keep_only=KEEP_FIELDS)
# print(df.head())