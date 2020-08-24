import csv

# See tests for a more comprehensive complementary table
SIMPLE_COMPLEMENTS_STR = """#Reduced table with bases A, G, C, T
 Base	Complementary Base
 A	T
 T	A
 G	C
 C	G
"""


def get_base_mapping(str_table):
    str_table_lines = str_table.split('\n')
    csv_lines = (row.strip() for row in str_table_lines if not row.startswith('#'))
    reader = csv.DictReader(csv_lines, delimiter='\t')
    mapping = {}
    for row in reader:
        mapping[row['Base']] = row['Complementary Base']
    return mapping


# Recommended helper function
def _clean_sequence(sequence, base_mapping):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns all sequences converted to upper case and remove invalid
    characters
    t!t%ttttAACCG --> TTTTTTAACCG
    """
    return ''.join(c for c in sequence.upper() if c in base_mapping.keys())


def reverse(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a reversed string of sequence while removing all characters
    not found in str_table characters
    e.g. t!t%ttttAACCG --> GCCAATTTTTT
    """
    base_mapping = get_base_mapping(str_table)
    return _clean_sequence(sequence[::-1], base_mapping)


def complement(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a string containing complementary bases as defined in
    str_table while removing non input_sequence characters
    e.g. t!t%ttttAACCG --> AAAAAATTGGC
    """
    base_mapping = get_base_mapping(str_table)
    return ''.join(base_mapping[c] for c in _clean_sequence(sequence, base_mapping))


def reverse_complement(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a string containing complementary bases as defined in str_table
    while removing non input_sequence characters
    e.g. t!t%ttttAACCG --> CGGTTAAAAAA
    """
    return complement(sequence, str_table)[::-1]
