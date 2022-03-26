class CorpusStats:
    @staticmethod
    def inc_val(x: int) -> int:
        return x + 1

    def __init__(self):
        """Values for quantifying data extraction success."""
        self.parsed_docs = 0
        self.valid_docs = 0
        self.parsed_docs_repr = ""
        self.parsed_processes = 0
        self.valid_process = 0
        self.valid_process_id = 0
        self.parsed_processes_repr = ""
        self.people = 0
        self.person_add_data = 0
        self.parsed_people_repr = ""

    def update_repr_calculations(self):
        if self.parsed_docs > 0:
            self.parsed_docs_repr = (
                f"valid docs: {self.valid_docs}/{self.parsed_docs} "
                f"({round((self.valid_docs/self.parsed_docs)*100,2)}%)"
            )
        if self.parsed_processes > 0:
            self.parsed_processes_repr = (
                f"valid processes: {self.valid_process}/{self.parsed_processes} "
                f"({round((self.valid_process/self.parsed_processes)*100,2)}%), "
                f"id: {self.valid_process_id}/{self.valid_process} "
                f"({round((self.valid_process_id/self.valid_process)*100,2)}%)"
            )
        if self.people > 0:
            self.parsed_people_repr = (
                f"additional data (/people): {self.person_add_data}/{self.people} "
                f"({round((self.person_add_data/self.people)*100,2)}%)"
            )

    def get_repr_dict(self) -> dict:
        self.update_repr_calculations()
        return self.__dict__

    def inc_val_parsed_docs(self):
        self.parsed_docs = CorpusStats.inc_val(self.parsed_docs)

    def inc_val_valid_docs(self):
        self.valid_docs = CorpusStats.inc_val(self.valid_docs)

    def inc_parsed_processes(self):
        self.parsed_processes = CorpusStats.inc_val(self.parsed_processes)

    def inc_val_valid_process(self):
        self.valid_process = CorpusStats.inc_val(self.valid_process)

    def inc_val_valid_process_id(self):
        self.valid_process_id = CorpusStats.inc_val(self.valid_process_id)

    def inc_val_people(self):
        self.people = CorpusStats.inc_val(self.people)

    def inc_val_person_add_data(self):
        self.person_add_data = CorpusStats.inc_val(self.person_add_data)
