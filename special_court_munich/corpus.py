class CorpusStats:
    """Values for quantifying data extraction success."""

    @staticmethod
    def inc_val(val: int) -> int:
        """Increment the value of the given integer by one.

        Parameters:
            val (int): Input value.

        Returns:
            int: Incremented value of the given integer.
        """
        return val + 1

    def __init__(self):
        self.parsed_docs = 0
        self.valid_docs = 0
        self.parsed_docs_repr = ""
        self.parsed_proceedings = 0
        self.missing_proceedings_estimate = 0
        self.valid_proceedings = 0
        self.valid_registration_no = 0
        self.parsed_proceedings_repr = ""
        self.persons = 0

    def has_been_inc(self) -> bool:
        """Check if at least one instance attribute has been incremented.

        Returns:
            bool: True, iff at least one instance attribute has been incremented.
        """
        return (
            self.parsed_docs != 0
            or self.valid_docs != 0
            or self.parsed_proceedings != 0
            or self.valid_proceedings != 0
            or self.valid_registration_no != 0
            or self.persons != 0
        )

    def update_repr_calculations(self) -> None:
        """Updates the representation strings."""
        if self.parsed_docs > 0:
            self.parsed_docs_repr = (
                f"valid docs: {self.valid_docs}/{self.parsed_docs} "
                f"({round((self.valid_docs / self.parsed_docs) * 100, 2)}%)"
            )
        if self.parsed_proceedings > 0:
            self.parsed_proceedings_repr = (
                f"valid proceedigs: {self.valid_proceedings}/{self.parsed_proceedings} "
                f"({round((self.valid_proceedings / self.parsed_proceedings) * 100, 2)}%), "
                f"registration_no: {self.valid_registration_no}/{self.parsed_proceedings} "
                f"({round((self.valid_registration_no / self.parsed_proceedings) * 100, 2)}%)"
            )

    def get_repr_dict(self) -> dict:
        """Returns this object as a dictionary, transforming class attributes and their values to key-value pairs.

        Returns:
            dict: this class object as a dictionary representation.
        """
        self.update_repr_calculations()
        return self.__dict__

    def inc_val_missing_proceedings(self) -> None:
        self.missing_proceedings_estimate = CorpusStats.inc_val(
            self.missing_proceedings_estimate
        )

    def inc_val_parsed_docs(self) -> None:
        """Increment the number of parsed documents."""
        self.parsed_docs = CorpusStats.inc_val(self.parsed_docs)

    def inc_val_valid_docs(self) -> None:
        """Increment the number of valid documents."""
        self.valid_docs = CorpusStats.inc_val(self.valid_docs)

    def inc_val_parsed_proceedings(self) -> None:
        """Increment the number of parsed processes."""
        self.parsed_proceedings = CorpusStats.inc_val(self.parsed_proceedings)

    def inc_val_valid_proceedings(self) -> None:
        """Increment the number of valid processes."""
        self.valid_proceedings = CorpusStats.inc_val(self.valid_proceedings)

    def inc_val_valid_registration_no(self) -> None:
        """Increment the number of valid process ids."""
        self.valid_registration_no = CorpusStats.inc_val(self.valid_registration_no)

    def inc_val_persons(self) -> None:
        """Increment the number of people indicted."""
        self.persons = CorpusStats.inc_val(self.persons)
