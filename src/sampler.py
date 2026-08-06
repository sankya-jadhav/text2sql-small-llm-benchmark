import json
import random
from collections import defaultdict
from pathlib import Path


class StratifiedSampler:
    """
    Creates a reproducible benchmark subset from Spider.

    The sampler groups questions by database and samples
    approximately equal numbers from each database.

    The sampled benchmark is fixed and reused across
    every experiment for fair comparison.
    """

    def __init__(
        self,
        questions,
        sample_size=180,
        random_seed=42
    ):

        self.questions  = questions

        self.sample_size = sample_size

        self.random_seed = random_seed

        random.seed(random_seed)

    def group_by_database(self):

        groups = defaultdict(list)

        for index, question in enumerate(self.questions):

            groups[question["db_id"]].append(index)

        return groups


    def calculate_quota(self):

        groups = self.group_by_database()

        num_databases = len(groups)

        quota = max(
            1,
            self.sample_size // num_databases
        )

        return quota

    def sample(self):

        groups = self.group_by_database()

        quota = self.calculate_quota()

        sampled = []

        remaining = []

        for indices in groups.values():

            random.shuffle(indices)

            sampled.extend(indices[:quota])

            remaining.extend(indices[quota:])

        random.shuffle(remaining)

        while len(sampled) < self.sample_size:

            sampled.append(
                remaining.pop()
            )

        sampled.sort()

        return sampled

    def save(
        self,
        output_file
    ):

        sampled_indices = self.sample()

        benchmark = [

            self.questions[i]

            for i in sampled_indices

        ]

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                benchmark,
                f,
                indent=4
            )

        return benchmark