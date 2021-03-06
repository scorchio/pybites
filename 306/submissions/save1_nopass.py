import string

from Bio.Seq import Seq


def translate_cds(cds: str, translation_table: str) -> str:
    """
    :param cds: str: DNA coding sequence (CDS)
    :param translation_table: str: translation table as defined in Bio.Seq.Seq.CodonTable.ambiguous_generic_by_name
    :return: str: Protein sequence
    """
    cds_cleaned = cds.encode('ascii', 'ignore').translate(None, string.whitespace)
    return Seq(cds, translation_table, cds=True)