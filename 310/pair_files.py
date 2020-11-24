from collections import defaultdict
import re


def pair_files(filenames):
    """
    Function that pairs filenames

    filenames: list[str] containing filenames
    returns: list[tuple[str, str]] containing filename pairs
    """
    filenames_processed = defaultdict(dict)
    pattern = r'(.*)_S([0-9]{1,2})_L([0-9]{1,3})_R([12])_([0-9]{3})\.fastq\.gz'
    regex = re.compile(pattern, flags=re.IGNORECASE)
    for filename in filenames:
        matches = regex.fullmatch(filename)
        if matches:
            match_indexes = matches.groups()
            non_r_indexes = match_indexes[0], match_indexes[1], match_indexes[2], match_indexes[4]
            r_index = match_indexes[3]
            filenames_processed[non_r_indexes][r_index] = filename
    
    pairs = []
    for r_dict in filenames_processed.values():
        if len(r_dict) != 2 or '1' not in r_dict or '2' not in r_dict:
            continue
        pairs.append((r_dict['1'], r_dict['2']))
    return pairs


# Set up for your convenience during testing
if __name__ == "__main__":
    filenames = [
        "Sample1_S1_L001_R1_001.FASTQ.GZ",
        "Sample1_S1_L001_R2_001.fastq.gz",
        "Sample2_S2_L001_R1_001.fastq.gz",
        "sample2_s2_l001_r2_001.fastq.gz",
    ]
    # ('Sample1_S1_L001_R1_001.FASTQ.GZ', 'Sample1_S1_L001_R2_001.fastq.gz')
    # ('Sample2_S2_L001_R1_001.fastq.gz', 'sample2_s2_l001_r2_001.fastq.gz')

    for pair in pair_files(filenames):
        print(pair)