# Medschool-Test, or *"Test di Medicina"*

<p align="center">
  <img src="assets/images/test-medicina.jpg" />
</p>

## Is your LLM able to pass a National Entrance Exam for the Italian Medical School?

This the GitHub repo for our Huggingface dataset designed for evaluating Language Model (LLM) on a broad range of questions from the **national entrance exams for the Italian medical school**.
The dataset includes multiple-choice questions from various subjects such as biology, chemistry, physics, mathematics, world knowledge, and more.
Each question is accompanied by five answer choices, with one correct answer.

The dataset is available on Huggingface! You can find it [here](https://huggingface.co/datasets/room-b007/test-medicina).

## Features

- **Multiple topics**: Questions cover a wide range of subjects, including biology, chemistry, physics, mathematics, world knowledge (with a focus on Italian culture), and more.

- **"Multiple-choice" and "Cloze-style" formats**: Each question has five answer choices, with one correct answer. This dataset is designed to evaluate LLMs on both multiple-choice and cloze-style questions. More specifically, each question is presented in the following formats:

  - **Multiple-choice**: The question is followed by five answer choices, with one correct answer. The evaluation metrics is based on the model's ability to select the correct answer when presented with the question and answer choices.

  - **Cloze-style**: The question is NOT followed by answer choices. The evaluation metric is based on the model's ability to generate the correct answer when presented with the question only.

- **Large-scale**: The dataset contains over 3K high-quality questions, making it suitable for the evaluation of LLMs.

- **Italian (and English coming soon)**: The dataset is currently available in Italian, with an English version coming soon.


## Evaluation

The dataset is designed to evaluate LLMs on a wide range of questions from medical school entrance exams. The evaluation metrics are based on the model's ability to select the correct answer when presented with the question and answer choices (multiple-choice format) or generate the correct answer when presented with the question only (cloze-style format).

### Leaderboard
> [!NOTE]
> Coming soon!

### Scoring

For each question, the model obtains a score ranging from -0.4 to 1.5, based on the following criteria:
- **Correct Answer**: If the model selects the correct answer, it receives a score of 1.5.
- **Incorrect Answer**: If the model selects an incorrect answer, it receives a score of -0.4.
- **No Answer**: If the model does not select any answer, it receives a score of 0.0.

The final score is calculated as the weighted average of the scores obtained on all questions, where the weight of each question depends on the topic of the question, as follows:
| Subject            | Score | Weight   |
|--------------------|-------|----------|
| Biology            | 23/60 | 0.3833   |
| Chemistry          | 15/60 | 0.25     |
| Math & Physics     | 13/60 | 0.2167   |
| World Knowledge    | 4/60  | 0.0667   |
| Logic & Reasoning  | 5/60  | 0.0833   |

This is the same scoring system used for the official Italian medical school entrance exams.

### Evaluation Script

The evaluation is based on the `lm-evaluation-harness` library, which provides a simple and flexible way to evaluate LLMs on a wide range of tasks and datasets. The tasks are defined in `tasks/medschool-test`.

#### Requirements and Installation
We recommend using Conda to create a new environment and install the required libraries. You can create a new Conda environment using the following command:

```bash
conda create -n medschool-test python=3.10
conda activate medschool-test
```

> [!NOTE]
> Using Conda is optional but highly recommended to avoid conflicts with existing libraries.

To run the evaluation, you need to install the `lm-evaluation-harness` library and the `transformers` library. You can install them using the following command:

```bash
pip install --upgrade -r requirements.txt
```

#### Running the Evaluation Script

To run the evaluation, you can use the following command:

```bash
# Model to evaluate: meta-llama/Meta-Llama-3.1-8B-Instruct (in bfloat16)
MODEL_ARGS="pretrained=meta-llama/Meta-Llama-3.1-8B-Instruct,dtype=bfloat16"

# Evaluate the model on both multiple-choice and cloze-style formats
TASKS="medschool_test_it_mc,medschool_test_it_cloze"

# Create the output directory if it does not exist
OUTPUT_DIR="outputs/"
mkdir -p $OUTPUT_DIR

# Run the evaluation with the lm-evaluation-harness library
accelerate launch -m lm_eval \
  --model hf \
  --model_args $MODEL_ARGS \
  --tasks $TASKS \
  --batch_size auto \
  --log_samples \
  --output_path $OUTPUT_DIR \
  --include tasks/medschool-test/

```

This command evaluates the model `meta-llama/Meta-Llama-3.1-8B-Instruct` on the Italian version of the dataset in both multiple-choice and cloze-style formats. The evaluation results are saved in the `outputs/` directory.

Please, refer to the examples in `examples/evaluation` or [lm-evaluation-harness](https://github.com/eleutherai/lm-evaluation-harness) repository for more details on how to use the library.

> [!NOTE]
> The scores provided by the evaluation script are between -0.4 and 1.5 per each category/domain. To get the final score, you need to calculate the weighted average of the scores obtained across the categories, where the weight of each question depends on the topic of the question (as described in the "Scoring" section above).
>
> For example, if the model obtains the following scores:
> - Biology: 1.0571
> - Chemistry: 0.7598
> - Knowledge: 1.0518
> - Reasoning: 0.2005
> - Math & Physics: 0.4302
>
> The final score is calculated as follows:
> ```
> average_per_question = (1.0571 * 0.3833) + (0.7598 * 0.25) + (1.0518 * 0.0667) + (0.2005 * 0.0833) + (0.4302 * 0.2167) = 0.7752
> overall_score = average_per_question * 60 = 46.51
> ```


## Data

### Source

The dataset is collected from the official Italian website of the Ministry of Education, University and Research ([MIUR](https://www.miur.gov.it/)), which hosts a large collection of past entrance exams for medical school in Italy. The dataset includes questions from various subjects, such as biology, chemistry, physics, mathematics, world knowledge, and more. You can find the original dataset [here](https://domande-ap.mur.gov.it/domande).

### Composition

The dataset contains over 3K questions, making it suitable for training and evaluating LLMs. The following table shows the number of questions in the dataset for each subject:

| Subject       | Number of questions |
|---------------|---------------------|
| Biology       | 1,180               |
| Chemistry     | 1,009               |
| Math & Physics       | 655               |
| World knowledge | 245             |
| Logic & Reasoning   | 212                  |
| **Total**         | **3,301**               |


### Size comparison with other benchmarks

The dataset contains over 3K questions, making it suitable for training and evaluating LLMs. The following table shows the size of the dataset compared to other benchmarks:

| **Dataset**              | **Number of questions** |
|--------------------------|------------------------|
| Medical School Entrance Exams | ~3,300             |
| ARC-Challenge (test)     | ~1,170                  |
| ARC-Easy (test)          | ~2,380                  |
| BoolQ (validation)       | ~3,270                  |
| CommonSenseQA (validation)     | ~1,220            |
| GSM8K (test)             | ~1,320                  |
| MMLU (test)              | ~14,000                 |
| PIQA (validation)        | ~1,850                  |
| SciQ (test)              | ~1,000                  |
| TruthfulQA (test)        | ~820                    |
| WinoGrande (test)        | ~1,767                  |

### Format

The dataset is provided in JSONL format, with each line representing a single question in the following format:

```json
{
  "id": 1691,
  "topic": "biologia",
  "text": "Come sono definite le cellule staminali che sono in grado di differenziarsi in tutti i tipi di cellule presenti nel corpo umano, ma non possono dare origine ad un organismo completo?",
  "answers": [
    "Cellule Staminali Multipotenti",
    "Cellule Staminali Pluripotenti",
    "Cellule Staminali Totipotenti",
    "Cellule Staminali Unipotenti",
    "Cellule Staminali Oligopotenti"
  ],
  "label": 1
}
```

where:
- `id` (int): The unique identifier of the question.
- `topic` (str): The subject of the question.
- `text` (str): The text of the question.
- `answers` (list): A list of five answer choices, with one correct answer.
- `label` (int): The index of the correct answer in the `answers` list (0-indexed).


### Examples

#### Biology

```json
{
  "id": 1691,
  "topic": "biologia",
  "text": "Come sono definite le cellule staminali che sono in grado di differenziarsi in tutti i tipi di cellule presenti nel corpo umano, ma non possono dare origine ad un organismo completo?",
  "answers": [
    "Cellule Staminali Multipotenti",
    "Cellule Staminali Pluripotenti",
    "Cellule Staminali Totipotenti",
    "Cellule Staminali Unipotenti",
    "Cellule Staminali Oligopotenti"
  ],
  "label": 1
}
```

#### Chemistry

```json
{
  "id": 19,
  "topic": "chimica",
  "text": "Rispetto alla classificazione che si trova nella tavola periodica il fluoro fa parte del: ",
  "answers": [
    "gruppo dei gas nobili",
    "gruppo degli alogeni",
    "gruppo dei lantanidi",
    "secondo gruppo",
    "quarto periodo"
  ],
  "label": 1
}
```

#### Math & Physics

```json
{
  "id": 1203,
  "topic": "fisica-matematica",
  "text": "Quali sono le coordinate del centro della circonferenza di equazione x^2 + y^2 + 2x – 6y + 5 = 0?",
  "answers": [
    "(2 ; –6)",
    "(–2 ; 6)",
    "(1 ; 3)",
    "(–1 ; 3)",
    "(2 ; 3)"
  ],
  "label": 3
}
```

#### World Knowledge

```json
{
  "id": 11,
  "topic": "competenze-conoscenze",
  "text": "Quale dei seguenti è il primo romanzo di Italo Calvino, pubblicato nel 1947?",
  "answers": [
    "Se una notte d'inverno un viaggiatore",
    "Il barone rampante",
    "Palomar",
    "Le cosmicomiche",
    "Il sentiero dei nidi di ragno"
  ],
  "label": 4
}
```

#### Logic & Reasoning

```json
{
  "id": 2539,
  "topic": "logica",
  "text": "Tutti i pasticcieri praticano il kendo; Gianluca pratica il kendo. Quale delle seguenti affermazioni aggiuntive consentirebbe di dedurre con certezza che Gianluca è un pasticciere?",
  "answers": [
    "Tra le persone che praticano kendo vi sono dei pasticcieri",
    "Alcune persone che praticano kendo si chiamano Gianluca",
    "Alcune persone che praticano kendo sono pasticcieri",
    "Non è certo che ogni persona che pratica kendo sia anche un pasticciere",
    "Ogni persona che pratica kendo è anche un pasticciere"
  ],
  "label": 4
}
```


### Reproducibility
We provide the code to reproduce our dataset in the `src/data/collection` directory. The code is written in Python and uses the `beautifulsoup4` library to scrape the questions from the official MIUR website. You can run the code to collect the latest questions from the website and generate the dataset in JSONL format.

You can run the code using the following command:

```bash
python src/data/collection/collect_questions.py \
    --output_path data/questions/medical_school_questions.jsonl \
    --last_page_index 174
```

This command collects the questions from the official MIUR website and saves them in the `data/questions/medical_school_questions.jsonl` file. You can specify the number of pages to scrape using the `--last_page_index` argument (where each page contains 20 questions and the last page is 174).


## Citation
> [!NOTE]
> We are currently writing a report on the dataset and will provide the citation information soon.


## License

This dataset is released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). Feel free to use it for research, commercial, or personal purposes.