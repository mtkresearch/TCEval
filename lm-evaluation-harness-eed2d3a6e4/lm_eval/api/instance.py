from dataclasses import dataclass, field
from typing import Literal, Tuple


@dataclass
class Instance:
    request_type: Literal["loglikelihood", "loglikelihood_rolling", "generate_until"]
    doc: dict
    arguments: tuple
    idx: int
    metadata: Tuple[str, int, int] = field(
        default_factory=lambda: (None, None, None)
    )  # TODO: better typehints here
    resps: list = field(default_factory=list)
    filtered_resps: dict = field(default_factory=dict)

    # initialized after init
    task_name: str = None
    doc_id: str = None
    repeats: str = None

    def __post_init__(self) -> None:
        # unpack metadata field
        self.task_name, self.doc_id, self.repeats = self.metadata

    @property
    def args(self):
        """
        Returns (string,) where `string` is the string to calculate loglikelihood over
        """
        return (
            self.arguments if isinstance(self.arguments, tuple) else (self.arguments,)
        )

    @args.setter
    def args(self, new_arguments: tuple) -> None:
        """
        Update the argument of the instance with a new one
        """
        if isinstance(new_arguments, tuple):
            self.arguments = new_arguments
        else:
            raise TypeError(f".... new arguments must be an tuple")
