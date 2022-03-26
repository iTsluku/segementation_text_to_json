class CorpusStats:
    """Values for quantifying data extraction success."""

    @staticmethod
    def inc_val(x: int) -> int:
        """Incremented the value of the given integer by one.

        Returns:
            int: incremented value of the given integer.
        """
        return x + 1

    def __init__(self):
        self.parsed_docs = 0
        self.valid_docs = 0
        self.parsed_docs_repr = ""
        self.parsed_processes = 0
        self.valid_processes = 0
        self.valid_process_ids = 0
        self.parsed_processes_repr = ""
        self.people = 0
        self.people_add_data = 0
        self.parsed_people_repr = ""

    def update_repr_calculations(self) -> None:
        """Updates the representation strings."""
        if self.parsed_docs > 0:
            self.parsed_docs_repr = (
                f"valid docs: {self.valid_docs}/{self.parsed_docs} "
                f"({round((self.valid_docs / self.parsed_docs) * 100, 2)}%)"
            )
        if self.parsed_processes > 0:
            self.parsed_processes_repr = (
                f"valid processes: {self.valid_processes}/{self.parsed_processes} "
                f"({round((self.valid_processes / self.parsed_processes) * 100, 2)}%), "
                f"id: {self.valid_process_ids}/{self.valid_processes} "
                f"({round((self.valid_process_ids / self.valid_processes) * 100, 2)}%)"
            )
        if self.people > 0:
            self.parsed_people_repr = (
                f"additional data (/people): {self.people_add_data}/{self.people} "
                f"({round((self.people_add_data / self.people) * 100, 2)}%)"
            )

    def get_repr_dict(self) -> dict:
        """Returns this object as a dictionary, transforming class attributes and their values to key-value pairs.

        Returns:
            dict: this class object as a dictionary representation.
        """
        self.update_repr_calculations()
        return self.__dict__

    def inc_val_parsed_docs(self) -> None:
        """Increment the number of parsed documents."""
        self.parsed_docs = CorpusStats.inc_val(self.parsed_docs)

    def inc_val_valid_docs(self) -> None:
        """Increment the number of valid documents."""
        self.valid_docs = CorpusStats.inc_val(self.valid_docs)

    def inc_parsed_processes(self) -> None:
        """Increment the number of parsed processes."""
        self.parsed_processes = CorpusStats.inc_val(self.parsed_processes)

    def inc_val_valid_processes(self) -> None:
        """Increment the number of valid processes."""
        self.valid_processes = CorpusStats.inc_val(self.valid_processes)

    def inc_val_valid_process_ids(self) -> None:
        """Increment the number of valid process ids."""
        self.valid_process_ids = CorpusStats.inc_val(self.valid_process_ids)

    def inc_val_people(self) -> None:
        """Increment the number of people indicted."""
        self.people = CorpusStats.inc_val(self.people)

    def inc_val_people_add_data(self) -> None:
        """Increment the number of people from whom additional data could be extracted."""
        self.people_add_data = CorpusStats.inc_val(self.people_add_data)
