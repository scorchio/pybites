import pytest

from pair_files import pair_files


@pytest.mark.parametrize(
    "test_description,test_input,expected",
    [
        (
            "Standard input, all match",
            [
                "NCTC8325_S1_L001_R1_001.fastq.gz",
                "NCTC8325_S1_L001_R2_001.fastq.gz",
                "E.coliK12_S2_L001_R1_001.fastq.gz",
                "E.coliK12_S2_L001_R2_001.fastq.gz",
                "C.elegans_S3_L001_R1_001.fastq.gz",
                "C.elegans_S3_L001_R2_001.fastq.gz",
            ],
            [
                (
                    "C.elegans_S3_L001_R1_001.fastq.gz",
                    "C.elegans_S3_L001_R2_001.fastq.gz",
                ),
                (
                    "E.coliK12_S2_L001_R1_001.fastq.gz",
                    "E.coliK12_S2_L001_R2_001.fastq.gz",
                ),
                (
                    "NCTC8325_S1_L001_R1_001.fastq.gz",
                    "NCTC8325_S1_L001_R2_001.fastq.gz",
                ),
            ],
        ),
        (
            "Standard input, order mixed, all match",
            [
                "C.elegans_S3_L001_R2_001.fastq.gz",
                "E.coliK12_S2_L001_R2_001.fastq.gz",
                "NCTC8325_S1_L001_R2_001.fastq.gz",
                "E.coliK12_S2_L001_R1_001.fastq.gz",
                "NCTC8325_S1_L001_R1_001.fastq.gz",
                "C.elegans_S3_L001_R1_001.fastq.gz",
            ],
            [
                (
                    "C.elegans_S3_L001_R1_001.fastq.gz",
                    "C.elegans_S3_L001_R2_001.fastq.gz",
                ),
                (
                    "E.coliK12_S2_L001_R1_001.fastq.gz",
                    "E.coliK12_S2_L001_R2_001.fastq.gz",
                ),
                (
                    "NCTC8325_S1_L001_R1_001.fastq.gz",
                    "NCTC8325_S1_L001_R2_001.fastq.gz",
                ),
            ],
        ),
        (
            "Two non matching pairs",
            [
                "NCTC8325_S1_L001_R1_001.fastq.gz",
                "NCTC8325_S1_L001_R2_001.fastq.gz",
                "E.coli_S2_L001_R1_001.fastq.gz",
                "E.coliK12_S2_L001_R2_001.fastq.gz",
                "C.elegans_S3_L001_R1_001.fastq.gz",
                "C.elegans_S4_L001_R2_001.fastq.gz",
            ],
            [
                (
                    "NCTC8325_S1_L001_R1_001.fastq.gz",
                    "NCTC8325_S1_L001_R2_001.fastq.gz",
                )
            ],
        ),
        (
            "Higher and inconsistent lane numbers",
            [
                "NCTC8325_S1_L002_R1_001.fastq.gz",
                "NCTC8325_S1_L002_R2_001.fastq.gz",
                "C.elegans_S3_L003_R1_001.fastq.gz",
                "C.elegans_S4_L003_R2_001.fastq.gz",
            ],
            [
                (
                    "NCTC8325_S1_L002_R1_001.fastq.gz",
                    "NCTC8325_S1_L002_R2_001.fastq.gz",
                ),
            ],
        ),
        (
            "Extra underscores in filenames",
            [
                "NCTC_8325_S1_L001_R1_001.fastq.gz",
                "NCTC_8325_S1_L001_R2_001.fastq.gz",
                "C._ele_gans_1_S3_L001_R1_001.fastq.gz",
                "C._ele_gans_1_S3_L001_R2_001.fastq.gz",
            ],
            [
                (
                    "C._ele_gans_1_S3_L001_R1_001.fastq.gz",
                    "C._ele_gans_1_S3_L001_R2_001.fastq.gz",
                ),
                (
                    "NCTC_8325_S1_L001_R1_001.fastq.gz",
                    "NCTC_8325_S1_L001_R2_001.fastq.gz",
                ),
            ],
        ),
        (
            "Higher and non matching R numbers",
            [
                "NCTC8325_S1_L001_R1_001.fastq.gz",
                "NCTC8325_S1_L001_R2_001.fastq.gz",
                "E.coliK12_S2_L001_R3_001.fastq.gz",
                "E.coliK12_S2_L001_R4_001.fastq.gz",
                "C.elegans_S3_L001_R1_001.fastq.gz",
                "C.elegans_S3_L001_R3_001.fastq.gz",
            ],
            [
                (
                    "NCTC8325_S1_L001_R1_001.fastq.gz",
                    "NCTC8325_S1_L001_R2_001.fastq.gz",
                )
            ],
        ),
        (
            "Pairs with file paths",
            [
                "folder/NCTC8325_S1_L001_R1_001.fastq.gz",
                "folder/NCTC8325_S1_L001_R2_001.fastq.gz",
                "folder/E.coliK12_S2_L001_R1_001.fastq.gz",
                "folder/E.coliK12_S2_L001_R2_001.fastq.gz",
                "folder/C.elegans_S3_L001_R1_001.fastq.gz",
                "folder/C.elegans_S3_L001_R2_001.fastq.gz",
            ],
            [
                (
                    "folder/C.elegans_S3_L001_R1_001.fastq.gz",
                    "folder/C.elegans_S3_L001_R2_001.fastq.gz",
                ),
                (
                    "folder/E.coliK12_S2_L001_R1_001.fastq.gz",
                    "folder/E.coliK12_S2_L001_R2_001.fastq.gz",
                ),
                (
                    "folder/NCTC8325_S1_L001_R1_001.fastq.gz",
                    "folder/NCTC8325_S1_L001_R2_001.fastq.gz",
                ),
            ],
        ),
        (
            "Pairs with file paths and capitalized file extensions",
            [
                "folder/NCTC8325_S1_L001_R1_001.FASTQ.GZ",
                "folder/NCTC8325_S1_L001_R2_001.FASTQ.GZ",
                "folder/E.coliK12_S2_L001_R1_001.FASTQ.GZ",
                "folder/E.coliK12_S2_L001_R2_001.FASTQ.GZ",
                "folder/C.elegans_S3_L001_R1_001.FASTQ.GZ",
                "folder/C.elegans_S3_L001_R2_001.FASTQ.GZ",
            ],
            [
                (
                    "folder/C.elegans_S3_L001_R1_001.FASTQ.GZ",
                    "folder/C.elegans_S3_L001_R2_001.FASTQ.GZ",
                ),
                (
                    "folder/E.coliK12_S2_L001_R1_001.FASTQ.GZ",
                    "folder/E.coliK12_S2_L001_R2_001.FASTQ.GZ",
                ),
                (
                    "folder/NCTC8325_S1_L001_R1_001.FASTQ.GZ",
                    "folder/NCTC8325_S1_L001_R2_001.FASTQ.GZ",
                ),
            ],
        ),
        (
            "Pairs with file paths and inconsistent capitalization of file extensions between pairs",
            [
                "folder/NCTC8325_S1_L001_R1_001.FASTQ.GZ",
                "folder/NCTC8325_S1_L001_R2_001.FASTQ.GZ",
                "folder/E.coliK12_S2_L001_R1_001.fastq.gz",
                "folder/E.coliK12_S2_L001_R2_001.FASTQ.GZ",
                "folder/C.elegans_S3_L001_R1_001.fastq.GZ",
                "folder/C.elegans_S3_L001_R2_001.FASTQ.gz",
            ],
            [
                (
                    "folder/C.elegans_S3_L001_R1_001.fastq.GZ",
                    "folder/C.elegans_S3_L001_R2_001.FASTQ.gz",
                ),
                (
                    "folder/E.coliK12_S2_L001_R1_001.fastq.gz",
                    "folder/E.coliK12_S2_L001_R2_001.FASTQ.GZ",
                ),
                (
                    "folder/NCTC8325_S1_L001_R1_001.FASTQ.GZ",
                    "folder/NCTC8325_S1_L001_R2_001.FASTQ.GZ",
                ),
            ],
        ),
        (
            "Pairs with with inconsistent capitalization of R1 and R2",
            [
                "NCTC8325_S1_L001_r1_001.fastq.gz",
                "NCTC8325_S1_L001_r2_001.fastq.gz",
                "E.coliK12_S2_l001_R1_001.fastq.gz",
                "E.coliK12_S2_l001_r2_001.fastq.gz",
                "C.elegans_s3_L001_r1_001.fastq.gz",
                "C.elegans_s3_L001_R2_001.fastq.gz",
            ],
            [
                (
                    "C.elegans_s3_L001_r1_001.fastq.gz",
                    "C.elegans_s3_L001_R2_001.fastq.gz",
                ),
                (
                    "E.coliK12_S2_l001_R1_001.fastq.gz",
                    "E.coliK12_S2_l001_r2_001.fastq.gz",
                ),
                (
                    "NCTC8325_S1_L001_r1_001.fastq.gz",
                    "NCTC8325_S1_L001_r2_001.fastq.gz",
                ),
            ],
        ),
        (
            "One Pair mixed with files with other file extensions",
            [
                "NCTC8325_S1_L001_R1_001.fastq.gz",
                "NCTC8325_S1_L001_R1_001.md5.gz",
                "NCTC8325_S1_L001_R2_001.md5.gz",
                "NCTC8325_S1_L001_R2_001.fastq.gz",
                "C.elegans_S3_L001_R1_001.md5.gz",
                "C.elegans_S3_L001_R2_001.md5.gz",
            ],
            [("NCTC8325_S1_L001_R1_001.fastq.gz", "NCTC8325_S1_L001_R2_001.fastq.gz")],
        ),
        (
                "Double file extension",
                [
                    "NCTC8325_S1_L001_R1_001.fastq.gz.fastq.gz",
                    "NCTC8325_S1_L001_R2_001.fastq.gz.fastq.gz",
                ],
            [],
        ),
        (
            "S number missing",
            [
                "NCTC8325_S_L001_R1_001.fastq.gz",
                "NCTC8325_S_L001_R2_001.fastq.gz",
            ],
            [],
        ),
    ],
)
def test_pair_files(test_description, test_input, expected):
    print(f"Test_pair_files {test_description}")
    assert sorted(pair_files(test_input)) == expected