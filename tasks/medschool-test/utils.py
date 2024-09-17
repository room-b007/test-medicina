import datasets
import numpy as np

QUERY_PREFIX = {
    "cloze": {
        "en": "Question: {input}",
        "it": "Domanda: {input}",
    },
    "multiple_choice": {
        "en": "Question: {input}\n{choices}",
        "it": "Domanda: {input}\n{choices}",
    },
}

ANSWER_PREFIX = {
    "cloze": {
        "en": "Answer: ",
        "it": "Risposta: ",
    },
    "multiple_choice": {
        "en": "Answer: ",
        "it": "Risposta: ",
    },
}


def process_results(doc, results):
    """
    Process the results of a model on a dataset.

    Args:
        doc: The document from the dataset.
        results: The results of the model on the dataset.

    """
    gold = doc["gold"]

    loglikelihoods, _ = zip(*results)
    probabilities = np.exp(loglikelihoods) / np.sum(np.exp(loglikelihoods))
    prediction = np.argmax(probabilities)

    choice_len = [len(c) for c in doc["choices"]]
    normalized_probabilities = probabilities / np.array(choice_len)
    normalized_prediction = np.argmax(normalized_probabilities)

    if prediction == 5:  # index 5 is the "Prefer not to answer" choice
        score = 0.0
    elif prediction == gold:
        score = 1.5
    else:
        score = -0.4

    if normalized_prediction == 5:  # index 5 is the "Prefer not to answer" choice
        normalized_score = 0.0
    elif normalized_prediction == gold:
        normalized_score = 1.5
    else:
        normalized_score = -0.4

    return {
        "acc": score,
        "acc_norm": normalized_score,
    }


def process_docs(
    dataset: datasets.Dataset,
    language: str,
    template: str,
    prefer_not_to_answer: str,
    topic: str = None,
) -> datasets.Dataset:
    """
    Prepare the dataset and builds the prompt using the source and target languages.

    Args:
        dataset: The dataset to process.
        language: The language of the dataset.
        template: The template to use for the prompt (cloze or multiple_choice).
        prefer_not_to_answer: The answer to use when the model prefers not to answer.

    Returns:
        The processed dataset.
    """

    def _process_doc(doc):
        input = doc["text"]
        choices = doc["answers"] + [prefer_not_to_answer]

        input = input.strip()
        choices = [choice.strip() for choice in choices]

        if template == "multiple_choice":
            labels = ["A", "B", "C", "D", "E", "F"]
            multiple_choices = [
                f"{label}. {choice}" for choice, label in zip(choices, labels)
            ]

            query = QUERY_PREFIX[template][language].format(
                input=input,
                choices="\n".join(multiple_choices),
            )

            query += "\n" + ANSWER_PREFIX[template][language]
            choices = labels

        elif template == "cloze":
            query = QUERY_PREFIX[template][language].format(input=input)
            query += "\n" + ANSWER_PREFIX[template][language]

        else:
            raise ValueError(f"Invalid template: {template}")

        return {
            "id": doc["id"],
            "query": query,
            "choices": choices,
            "gold": doc["label"],
        }

    if topic is not None:
        dataset = dataset.filter(lambda x: x["topic"] == topic)

    return dataset.map(_process_doc)


# Custom methods to use the dataset for cloze-style evaluation.
def process_docs_it_cloze(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(dataset, "it", "cloze", "Preferisco non rispondere")


def process_docs_it_cloze_bio(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(dataset, "it", "cloze", "Preferisco non rispondere", "biologia")


def process_docs_it_cloze_chem(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(dataset, "it", "cloze", "Preferisco non rispondere", "chimica")


def process_docs_it_cloze_math(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset, "it", "cloze", "Preferisco non rispondere", "fisica-matematica"
    )


def process_docs_it_cloze_know(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset, "it", "cloze", "Preferisco non rispondere", "competenze-conoscenze"
    )


def process_docs_it_cloze_log(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(dataset, "it", "cloze", "Preferisco non rispondere", "logica")


# Custom methods to use the ARC-Challenge dataset with the choices directly in the prompt a-la MMLU.
def process_docs_it_mc(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(dataset, "it", "multiple_choice", "Preferisco non rispondere")


def process_docs_it_mc_bio(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset, "it", "multiple_choice", "Preferisco non rispondere", "biologia"
    )


def process_docs_it_mc_chem(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset, "it", "multiple_choice", "Preferisco non rispondere", "chimica"
    )


def process_docs_it_mc_math(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset,
        "it",
        "multiple_choice",
        "Preferisco non rispondere",
        "fisica-matematica",
    )


def process_docs_it_mc_know(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset,
        "it",
        "multiple_choice",
        "Preferisco non rispondere",
        "competenze-conoscenze",
    )


def process_docs_it_mc_log(dataset: datasets.Dataset) -> datasets.Dataset:
    return process_docs(
        dataset, "it", "multiple_choice", "Preferisco non rispondere", "logica"
    )


def compute_aggregate_score(*args):
    print(args)
    return {
        "overall_score": 0.0,
    }
