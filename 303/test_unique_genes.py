"""
Test unique_genes.convert_to_unique_genes()
 -Test regular 2-line FASTA file (one header row, one sequence row)
 -Test multi-line FASTA file (one header row, multiple sequence rows)
 -Test that first sequence is ignored in absence of a header
 -Test case variation in gene name
 -Test case variation in sequence
 -Test additional gene name
 -Test use of gzip format as in- or output
"""
import gzip
import os
import pytest
from urllib.request import urlretrieve

import unique_genes

# ################ SETUP

NARI_URL = "https://bites-data.s3.us-east-2.amazonaws.com/narI.fna"

# ################ Support functions
def make_fasta_from_tuple(content):
    """
    Creates a FASTA text from tuples
    """
    return_text = ""
    for header, seq in content:
        return_text += f"{header}\n{seq}\n"
    return return_text


def write_test_file(filename, content, zip=False):
    """
    Writes the contents of a FASTA fie into a physical file
    """
    if not os.path.isfile(filename):
        if not zip:
            with open(filename, "w") as f:
                f.write(make_fasta_from_tuple(content))
        else:
            with gzip.open(filename, "wt") as f:
                f.write(make_fasta_from_tuple(content))


def len_and_first_line(test_filename, tmp):

    input_filename = test_filename

    output_filename = tmp / "output.fasta"

    unique_genes.convert_to_unique_genes(str(input_filename), str(output_filename))
    with open(output_filename, "r") as f:
        all_lines = f.readlines()
        return (
            sum([1 for line in all_lines if line[0] == ">"]),
            all_lines[0].strip().upper(),
        )


# Pytest fixtures ###############################
@pytest.fixture(scope="session")
def fasta_dir(tmpdir_factory):
    simple_fasta = [
        (">gene [locus_tag=AA11]", "AAAAAA"),
        (">gene [locus_tag=BB22]", "AAAAAA"),
        (">gene [locus_tag=CC33]", "AAAAAA"),
        (">gene [locus_tag=DD44]", "GAAAAC"),
    ]

    tmp_d = tmpdir_factory.mktemp("fastas")

    # Regular 2-line FASTA file (1 line header, one line sequence)
    write_test_file(tmp_d.join("simple_test.fasta"), simple_fasta)
    write_test_file(tmp_d.join("simple_test.fasta.gz"), simple_fasta, zip=True)

    # FASTA File where the sequence is spread over more than one line
    simple_multi_fasta = simple_fasta.copy()
    simple_multi_fasta[0] = (">gene [locus_tag=AA11]", "AAA\nAAA")
    write_test_file(tmp_d.join("simple_multi_fasta.fasta"), simple_multi_fasta)

    # FASTA File with first header missing
    missing_header = simple_fasta.copy()
    missing_header[0] = ("gene [locus_tag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("first_header_missing.fasta"), missing_header)

    # FASTA with same gene but upper/lower case variation
    name_case_variation = simple_fasta.copy()
    name_case_variation[0] = (">gEnE [locus_tag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("gene_case_variation.fasta"), name_case_variation)

    # FASTA with upper and lower case variation in sequence
    seq_case_variation = simple_fasta.copy()
    seq_case_variation[0] = (">gene [locus_tag=AA11]", "AaAaAa")
    write_test_file(tmp_d.join("seq_case_variation.fasta"), seq_case_variation)

    # FASTA file with more than one gene
    two_different_genes = simple_fasta.copy()
    two_different_genes[0] = (">gene2 [locus_tag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("two_gene_names.fasta"), two_different_genes)

    if not os.path.isfile(tmp_d.join("narI.fasta")):
        urlretrieve(url=NARI_URL, filename=tmp_d.join("narI.fasta"))

    return tmp_d


# End of setup ####################################

# Tests ###########################################


def test_regular_2line_fasta(fasta_dir, tmp_path):
    """
    Use a short FASTA file to test output
    """
    assert len_and_first_line(fasta_dir / "simple_test.fasta", tmp_path) == (
        2,
        ">gene [locus_tags=AA11,BB22,CC33]".upper(),
    )


def test_multiline_fasta(fasta_dir, tmp_path):
    """
    Test multi line FASTA file
    """
    assert len_and_first_line(fasta_dir / "simple_multi_fasta.fasta", tmp_path) == (
        2,
        ">gene [locus_tags=AA11,BB22,CC33]".upper(),
    )


def test_name_case_variation(fasta_dir, tmp_path):
    """
    Test if case variation in name is ignored
    """
    assert len_and_first_line(fasta_dir / "gene_case_variation.fasta", tmp_path) == (
        2,
        ">gene [locus_tags=AA11,BB22,CC33]".upper(),
    )


def test_seq_case_variation(fasta_dir, tmp_path):
    """ "
    Test if case variation in sequence is ignored
    """
    assert len_and_first_line(fasta_dir / "seq_case_variation.fasta", tmp_path) == (
        2,
        ">gene [locus_tags=AA11,BB22,CC33]".upper(),
    )


def test_header_missing(fasta_dir, tmp_path):
    """
    Test FASTA with missing header
    """
    assert len_and_first_line(fasta_dir / "first_header_missing.fasta", tmp_path) == (
        2,
        ">gene [locus_tags=BB22,CC33]".upper(),
    )


def test_longer_input(fasta_dir, tmp_path):
    """
    Test longer FASTA input
    """
    assert len_and_first_line(fasta_dir / "narI.fasta", tmp_path) == (
        58,
        ">narI [locus_tags=DP59_RS09945,Y036_RS19960,SY87_RS00665,SZ30_RS00830,AQ846_RS16685,BGI48_RS00955,BGI50_RS21770,AQ742_RS29760,AQ783_RS24625,AQ804_RS17165,AQ819_RS14565,AQ838_RS36260,AQ837_RS28155,AQ839_RS29335,AQ840_RS14260,AQ901_RS19340,AQ905_RS27755,AQ904_RS01210,AQ919_RS04570,AQ921_RS32415,AQ959_RS26455,AQ961_RS26945,AQ963_RS02165,AQ962_RS21790,A4G86_RS14410,A4G85_RS24330,C1W34_RS04280,C1W99_RS25750,C1W93_RS23700,C1W91_RS24560,C1W95_RS24580,C1X01_RS24900,C1W80_RS25855,C1X03_RS25160,E5U26_RS07600,EFY35_RS18945,EFY95_RS29240,EFD88_RS17870,EFK35_RS16190,EF032_RS29310,EFL73_RS24765,EFL71_RS25075,EFI57_RS16310,EF093_RS23065,EF100_RS24940,EFO39_RS23210,EFJ73_RS27440,EFP41_RS21775,EFP09_RS21615,EFV50_RS19610,EFR16_RS21235,EFV41_RS22340,EFR78_RS08490,EFP72_RS21575,EFQ68_RS18800,EFR72_RS14280,EFP85_RS19655,EFR74_RS21345,EFV67_RS18600,EFT84_RS09500,EFB38_RS29535,EFY02_RS19395,EFU30_RS23720,EFV27_RS03070,EFX36_RS26565,EFX96_RS20275,EFV42_RS20900,EFU80_RS21905,EFY12_RS16940]".upper(),
    )


def test_ambigious_gene_name(fasta_dir, tmp_path):
    """
    Test with more than one gene name present in FASTA file
    """
    with pytest.raises(NameError) as excinfo:
        unique_genes.convert_to_unique_genes(
            str(fasta_dir / "two_gene_names.fasta"), str(tmp_path / "output.fasta")
        )
    assert "Gene names differ between entries: 'gene2' vs. 'gene'" in str(excinfo.value)


def test_gzipped_fastas(fasta_dir, tmp_path):
    """
    Test how function handles gzipped FASTA files
    """

    # gz INPUT > fna OUTPUT
    assert len_and_first_line(fasta_dir / "simple_test.fasta.gz", tmp_path) == (
        2,
        ">gene [locus_tags=AA11,BB22,CC33]".upper(),
    )

    # fna INPUT > gz OUTPUT
    unique_genes.convert_to_unique_genes(
        str(fasta_dir / "simple_test.fasta"), str(tmp_path / "output.fasta.gz")
    )
    with gzip.open(str(tmp_path / "output.fasta.gz"), "rt") as f:
        assert (
            f.readlines()[0].strip().upper()
            == ">gene [locus_tags=AA11,BB22,CC33]".upper()
        )

    # gz INPUT > gz OUTPUT
    unique_genes.convert_to_unique_genes(
        str(fasta_dir / "simple_test.fasta.gz"), str(tmp_path / "output2.fasta.gz")
    )
    with gzip.open(str(tmp_path / "output2.fasta.gz"), "rt") as f:
        assert (
            f.readlines()[0].strip().upper()
            == ">gene [locus_tags=AA11,BB22,CC33]".upper()
        )