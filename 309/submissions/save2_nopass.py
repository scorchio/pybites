from __future__ import annotations

import string

EOL_PUNCTUATION = ".!?"


class Document:
    def __init__(self) -> None:
        self.lines = []

    def add_line(self, line: str, index: int = None) -> Document:
        """Add a new line to the document.

        Args:
            line (str): The line,
                expected to end with some kind of punctuation.
            index (int, optional): The place where to add the line into the document.
                If None, the line is added at the end. Defaults to None.

        Returns:
            Document: The changed document with the new line.
        """
        if not index:
            index = len(self.lines)
        self.lines.insert(index, line)
        return self

    def swap_lines(self, index_one: int, index_two: int) -> Document:
        """Swap two lines.

        Args:
            index_one (int): The first line.
            index_two (int): The second line.

        Returns:
            Document: The changed document with the swapped lines.
        """
        temp_line = self.lines[index_one]
        self.lines[index_two] = self.lines[index_one]
        self.lines[index_one] = temp_line
        return self

    def merge_lines(self, indices: list) -> Document:
        """Merge several lines into a single line.

        If indices are not in a row, the merged line is added at the first index.

        Args:
            indices (list): The lines to be merged.

        Returns:
            Document: The changed document with the merged lines.
        """
        destination_idx = indices[0]
        new_line = ''.join([self.lines[idx] for idx in indices])
        for idx, line_idx in reversed(enumerate(indices)):
            if idx == 0:
                self.lines[line_idx] = new_line
            else:
                del self.lines[line_idx]
        return self

    def add_punctuation(self, punctuation: str, index: int) -> Document:
        """Add punctuation to the end of a sentence.

        Overwrites existing punctuation.

        Args:
            punctuation (str): The punctuation. One of EOL_PUNCTUATION.
            index (int): The line to change.

        Returns:
            Document: The document with the changed line.
        """
        self.lines[index] = self.lines[index][:-1] + punctuation
        return self

    def word_count(self) -> int:
        """Return the total number of words in the document."""
        raise NotImplementedError("You have to fill this method with life.")

    @property
    def words(self) -> list:
        """Return a list of unique words, sorted and case insensitive."""
        raise NotImplementedError("You have to fill this method with life.")

    def _remove_puctuation(line: str) -> str:
        """Remove punctuation from a line."""
        # you can use this function as helper method for
        # Document.word_count() and Document.words
        # or you can totally ignore it
        pass

    def __len__(self):
        """Return the length of the document (i.e. line count)."""
        return len(self.lines)

    def __str__(self):
        """Return the content of the document as string."""
        return ''.join(self.lines)


if __name__ == "__main__":
    # this part is only execute when you run the file and is ignored by the tests
    # you can use this section for debugging and testing
    d = (
        Document()
        .add_line("My first sentence.")
        .add_line("My second sentence.")
        .add_line("Introduction", 0)
        .merge_lines([1, 2])
    )

    print(d)
    print(len(d))
    print(d.word_count())
    print(d.words)