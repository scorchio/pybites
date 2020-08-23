import os
from collections import Counter
from urllib.request import urlretrieve

# Translation Table:
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG11
# Each column represents one entry. Codon = {Base1}{Base2}{Base3}
# All Base 'T's need to be converted to 'U's to convert DNA to RNA
TRANSL_TABLE_11 = """
    AAs  = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
  Starts = ---M------**--*----M------------MMMM---------------M------------
  Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
  Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
  Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG
"""

TABLE_HEADER = "|  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |"
TABLE_DIVIDER = "---------------------------------------------------------------------------------------------------------"
TABLE_ROW = "|  {codon1}:  {aa1}   {freq1:>4.1f}  {count1:>5}  |  {codon2}:  {aa2}   {freq2:>4.1f}  {count2:>5}  |  {codon3}:  {aa3}   {freq3:>4.1f}  {count3:>5}  |  {codon4}:  {aa4}   {freq4:>4.1f}  {count4:>5}  |"

# Converted from http://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Staphylococcus_aureus_Newman_uid58839/NC_009641.ffn  # noqa E501
URL = "https://bites-data.s3.us-east-2.amazonaws.com/NC_009641.txt"

# Order of bases in the table
BASE_ORDER = ["U", "C", "A", "G"]


def _preload_sequences(url=URL):
    """
    Provided helper function
    Returns coding sequences, one sequence each line
    """
    filename = os.path.join(os.getenv("TMP", "/tmp"), "NC_009641.txt")
    if not os.path.isfile(filename):
        urlretrieve(url, filename)
    with open(filename, "r") as f:
        return f.readlines()


def extract_translation_table(translation_table_str):
    lines = translation_table_str.strip().splitlines()
    aa = lines[0].split(' = ')[1]
    base1 = lines[2].split(' = ')[1].replace('T', 'U')
    base2 = lines[3].split(' = ')[1].replace('T', 'U')
    base3 = lines[4].split(' = ')[1].replace('T', 'U')

    table = []
    for idx in range(len(base1)):
        table.append((f'{base1[idx]}{base2[idx]}{base3[idx]}', aa[idx]))
    return table


def get_codons(sequences):
    codons = []
    for sequence_line in sequences:
        for idx in range(len(sequence_line) // 3):
            codons.append(sequence_line[idx * 3:idx * 3 + 3])
    return codons


def generate_codon_usage_table(translation_table, codons):
    codon_counter = Counter(codons)
    total_codon_count = sum(codon_counter.values())

    output = []
    output.append(TABLE_HEADER)
    output.append(TABLE_DIVIDER)
    for idx in range(0, len(translation_table), 16):
        for idx2 in range(4):
            codon1, aa1 = translation_table[idx + idx2]
            freq1, count1 = codon_counter[codon1] / total_codon_count * 1000, codon_counter[codon1]
            codon2, aa2 = translation_table[idx + idx2 + 4]
            freq2, count2 = codon_counter[codon2] / total_codon_count * 1000, codon_counter[codon2]
            codon3, aa3 = translation_table[idx + idx2 + 8]
            freq3, count3 = codon_counter[codon3] / total_codon_count * 1000, codon_counter[codon3]
            codon4, aa4 = translation_table[idx + idx2 + 12]
            freq4, count4 = codon_counter[codon4] / total_codon_count * 1000, codon_counter[codon4]
            output.append(TABLE_ROW.format(
                codon1=codon1, aa1=aa1, freq1=freq1, count1=count1,
                codon2=codon2, aa2=aa2, freq2=freq2, count2=count2,
                codon3=codon3, aa3=aa3, freq3=freq3, count3=count3,
                codon4=codon4, aa4=aa4, freq4=freq4, count4=count4,
            ))
        output.append(TABLE_DIVIDER)
    return '\n'.join(output)



def return_codon_usage_table(
    sequences=_preload_sequences(), translation_table_str=TRANSL_TABLE_11
):
    """
    Receives a list of gene sequences and a translation table string
    Returns a string with all bases and their frequencies in a table
    with the following fields:
    codon_triplet: amino_acid_letter frequency_per_1000 absolute_occurrences

    Skip invalid coding sequences:
       --> must consist entirely of codons (3-base triplet)
    """
    translation_table = extract_translation_table(translation_table_str)
    codons = get_codons(sequences)
    return generate_codon_usage_table(translation_table, codons)


if __name__ == "__main__":
    print(return_codon_usage_table())