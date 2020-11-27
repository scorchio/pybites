from collections import defaultdict
from copy import deepcopy
import gzip
from io import StringIO
from Bio import SeqIO, SeqRecord


def convert_to_unique_genes(filename_in, filename_out):
    """
    Takes a standard FASTA file or gzipped FASTA file,
    de-duplicates the file, sorts by number of occurrences and
    outputs the result in a standard FASTA file

    filename_in: str Filename of FASTA file containing duplicated genes
    filename_out: str Filename of FASTA file to output reduced file

    returns None
    """
    read_method = gzip.open if '.gz' in filename_in else open
    read_flags = "rt" if '.gz' in filename_in else "r"
    with read_method(filename_in, read_flags) as handle:
        records = list(SeqIO.parse(handle, "fasta"))
    
    new_records = get_converted_records(records)

    stringio_out_handle = StringIO()
    SeqIO.write(new_records, stringio_out_handle, "fasta")

    write_method = gzip.open if '.gz' in filename_out else open 
    write_flags = "wt" if '.gz' in filename_out else "w"
    with write_method(filename_out, write_flags) as handle:
        handle.write(stringio_out_handle.getvalue())


def get_converted_records(records):
    records_dict = defaultdict(list)
    for record in records:
        records_dict[record.seq.upper()].append(record)
    new_records = []
    records_unordered = [(seq, records) for seq, records in records_dict.items()]
    records_ordered = sorted(records_unordered, key=lambda seq_records: len(seq_records[1]), reverse=True)
    expected_gene_name = None
    for seq, records in records_ordered:
        locus_tags = [_strip_description_to_locus_tag(record.name, record.description) for record in records]
        tags_joined = ','.join(locus_tags)
        proto_record = deepcopy(records[0])
        proto_record.id = proto_record.id.lower()
        proto_record.name = proto_record.name.lower()
        if not expected_gene_name:
            expected_gene_name = proto_record.name
        elif proto_record.name != expected_gene_name:
            raise NameError(f"Gene names differ between entries: '{expected_gene_name}' vs. '{proto_record.name}'")
        proto_record.description = f'{proto_record.name} [locus_tags={tags_joined}]'
        new_records.append(proto_record)
    return new_records


def _strip_description_to_locus_tag(name, description):
    return (
        description
            .lower()
            .replace(f'{name.lower()} ', '')
            .replace('[locus_tag=', '')
            .replace('[locus_tags=', '')
            .replace(']', '')
            .upper()
    )
