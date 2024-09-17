"""
This script collects questions from a website.

Usage:
    python collect_questions.py --url <url> --output_path <output_path> --first_page_index <first_page_index> --last_page_index <last_page_index>

Options:
    --url                  URL of the website [default: https://domande-ap.mur.gov.it/api/v1/domanda/list]
    --output_path          Path to save the questions [default: questions.jsonl]
    --first_page_index     Index of the first page to scrape [default: 0]
    --last_page_index      Index of the last page to scrape [default: 10]

Example:
    python collect_questions.py --url https://www.example.com --output_path questions.jsonl --first_page_index 0 --last_page_index 10

"""

import argparse
import json
import re
import requests

import tqdm
from loguru import logger


BASE_URL = "https://domande-ap.mur.gov.it/api/v1/domanda/list"
BASE_URL_ARGS = "?page={page_index}&page-size=20"

"""
Example of a POST request to the website:

curl 'https://domande-ap.mur.gov.it/api/v1/domanda/list?page=2&page-size=20' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'DNT: 1' \
  -H 'Referer: https://domande-ap.mur.gov.it/domande' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="127", "Not)A;Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"'
"""

"""
Example of a response from the website:
{
  "content": [
    {
      "id": 2020,
      "argomento": "biologia",
      "nro": 41,
      "domanda": "<b><p><span><span>Quale delle seguenti affermazioni sui lipidi è VERA?</span></span></p></b>",
      "risposte": [
        {
          "id": "e",
          "text": "<p><span>Immagazzinano l'informazione genetica</span></p>"
        },
        {
          "id": "b",
          "text": "<p><span>Degradano i prodotti di scarto della cellula</span></p>"
        },
        {
          "id": "a",
          "text": "<p><span>Fungono da riserva energetica</span></p>"
        },
        {
          "id": "c",
          "text": "<p><span>Hanno funzione catalitica</span></p>"
        },
        {
          "id": "d",
          "text": "<p><span>Producono immunoglobuline</span></p>"
        }
      ]
    },
    { ... },
    {
      "id": 1984,
      "argomento": "biologia",
      "nro": 60,
      "domanda": "<b><p><span><span>Quale delle seguenti affermazioni sul simporto è corretta?</span></span></p></b>",
      "risposte": [
        {
          "id": "b",
          "text": "<p><span>Non richiede dispendio energetico</span></p>"
        },
        {
          "id": "d",
          "text": "<p><span>È un tipo di trasporto passivo</span></p>"
        },
        {
          "id": "c",
          "text": "<p><span>Permette il passaggio simultaneo ma in direzione opposta di due sostanze differenti</span></p>"
        },
        {
          "id": "e",
          "text": "<p><span>Consente il passaggio di una sola sostanza in un'unica direzione</span></p>"
        },
        {
          "id": "a",
          "text": "<p><span>Permette il passaggio simultaneo di due sostanze nella stessa direzione</span></p>"
        }
      ]
    }
  ],
  "pageable": {
    "pageNumber": 2,
    "pageSize": 20,
    "sort": [
      {
        "direction": "ASC",
        "property": "argomento",
        "ignoreCase": false,
        "nullHandling": "NATIVE",
        "ascending": true,
        "descending": false
      },
      {
        "direction": "ASC",
        "property": "nro",
        "ignoreCase": false,
        "nullHandling": "NATIVE",
        "ascending": true,
        "descending": false
      }
    ],
    "offset": 40,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 175,
  "totalElements": 3500,
  "last": false,
  "size": 20,
  "number": 2,
  "sort": [
    {
      "direction": "ASC",
      "property": "argomento",
      "ignoreCase": false,
      "nullHandling": "NATIVE",
      "ascending": true,
      "descending": false
    },
    {
      "direction": "ASC",
      "property": "nro",
      "ignoreCase": false,
      "nullHandling": "NATIVE",
      "ascending": true,
      "descending": false
    }
  ],
  "numberOfElements": 20,
  "first": false,
  "empty": false
}
"""


def collect_questions(url, first_page_index=0, last_page_index=10):
    questions = []

    for page_index in tqdm.tqdm(
        range(first_page_index, last_page_index + 1),
        desc="Loading pages",
    ):
        # Create the URL for the current page
        current_url = url + BASE_URL_ARGS.format(page_index=page_index)

        # Send a GET request to the website
        response = requests.get(current_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON data
            data = response.json()

            # Extract the questions from the response
            questions.extend(data["content"])
        else:
            logger.error(f"Failed to load page {page_index}")

    return questions


def clean_text(text):
    text = text.strip()

    # Replace <sup> x </sup> with ^x
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text)

    # Replace <sub> x </sub> with _x
    text = re.sub(r"<sub>(.*?)</sub>", r"_\1", text)

    # Replace &nbsp; with a space
    text = re.sub(r"&nbsp;", " ", text)

    # Replace <br> with a newline
    text = re.sub(r"<br>", "\n", text)

    # Replace &lt; with < and &gt; with >
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)

    # Replace &amp; with &
    text = re.sub(r"&amp;", "&", text)

    # Replace &quot; with "
    text = re.sub(r"&quot;", '"', text)

    # Replace &apos; with '
    text = re.sub(r"&apos;", "'", text)

    # Replace &euro; with €
    text = re.sub(r"&euro;", "€", text)

    # Replace &deg; with °
    text = re.sub(r"&deg;", "°", text)

    # Replace &times; with ×
    text = re.sub(r"&times;", "×", text)

    # Replace &divide; with ÷
    text = re.sub(r"&divide;", "÷", text)

    # Replace &le; with ≤
    text = re.sub(r"&le;", "≤", text)

    # Replace &ge; with ≥
    text = re.sub(r"&ge;", "≥", text)

    # Replace &ne; with ≠
    text = re.sub(r"&ne;", "≠", text)

    # Replace &plusmn; with ±
    text = re.sub(r"&plusmn;", "±", text)

    # Replace &radic; with √
    text = re.sub(r"&radic;", "√", text)

    # Replace &infin; with ∞
    text = re.sub(r"&infin;", "∞", text)

    # Replace &int; with ∫
    text = re.sub(r"&int;", "∫", text)

    # Replace &sum; with ∑
    text = re.sub(r"&sum;", "∑", text)

    # Replace &alpha; with α
    text = re.sub(r"&alpha;", "α", text)

    # Replace &beta; with β
    text = re.sub(r"&beta;", "β", text)

    # Replace &gamma; with γ
    text = re.sub(r"&gamma;", "γ", text)

    # Replace &delta; with δ
    text = re.sub(r"&delta;", "δ", text)

    # Replace &epsilon; with ε
    text = re.sub(r"&epsilon;", "ε", text)

    # Replace &theta; with θ
    text = re.sub(r"&theta;", "θ", text)

    # Replace &lambda; with λ
    text = re.sub(r"&lambda;", "λ", text)

    # Replace &mu; with μ
    text = re.sub(r"&mu;", "μ", text)

    # Replace &sigma; with σ
    text = re.sub(r"&sigma;", "σ", text)

    # Replace &omega; with ω
    text = re.sub(r"&omega;", "ω", text)

    # Replace &pi; with π
    text = re.sub(r"&pi;", "π", text)

    # Replace &phi; with φ
    text = re.sub(r"&phi;", "φ", text)

    # Replace &psi; with ψ
    text = re.sub(r"&psi;", "ψ", text)

    # Replace &chi; with χ
    text = re.sub(r"&chi;", "χ", text)

    # Replace &tau; with τ
    text = re.sub(r"&tau;", "τ", text)

    # Replace &rho; with ρ
    text = re.sub(r"&rho;", "ρ", text)

    # Replace &xi; with ξ
    text = re.sub(r"&xi;", "ξ", text)

    # Replace &zeta; with ζ
    text = re.sub(r"&zeta;", "ζ", text)

    # Replace &eta; with η
    text = re.sub(r"&eta;", "η", text)

    # Replace &kappa; with κ
    text = re.sub(r"&kappa;", "κ", text)

    # Replace the double newline with a single newline
    text = re.sub(r" *\n+ *", "\n", text)

    return text.strip()


def process_questions(questions):
    processed_questions = {}

    for question in questions:
        # Extract the question details
        question_id = question["id"]
        topic = question["argomento"]
        text = question["domanda"]
        answers = question["risposte"]

        # Check if the questions and answers are not empty
        if not text or not answers:
            logger.warning(
                f"Skipping question {question_id} with empty text or answers"
            )
            continue

        # Check if the question and answers contain an img tag
        if "<img" in text:
            logger.warning(f"Skipping question {question_id} with image in text")
            continue

        for answer in answers:
            if "<img" in answer["text"]:
                logger.warning(f"Skipping question {question_id} with image in answers")
                continue

        # Clean the text of the question and answers
        text = clean_text(text)
        answers = [
            {"id": answer["id"], "text": clean_text(answer["text"])}
            for answer in answers
        ]

        # Remove any HTML tags from the question and answers
        text = re.sub(r"<[^>]*>", "", text)
        answers = [
            {"id": answer["id"], "text": re.sub(r"<[^>]*>", "", answer["text"])}
            for answer in answers
        ]

        # Extract the correct answer
        correct_answer_index = None
        for i, answer in enumerate(answers):
            if answer["id"] == "a":
                correct_answer_index = i
                break

        # Keep only the text of each answer
        answers = [answer["text"] for answer in answers]

        # Add the question to the processed questions dictionary
        processed_questions[question_id] = {
            "id": question_id,
            "topic": topic,
            "text": text,
            "answers": answers,
            "label": correct_answer_index,
        }

    num_total_questions = len(questions)
    num_processed_questions = len(processed_questions)
    logger.info(
        f"Processed {num_processed_questions} out of {num_total_questions} questions"
    )

    return processed_questions


def save_questions(questions, output_file):
    sorted_ids = sorted(questions.keys())

    with open(output_file, "w") as f:
        for question_id in sorted_ids:
            question = questions[question_id]
            line = json.dumps(question, ensure_ascii=False)
            f.write(line + "\n")

    logger.info(f"Saved {len(sorted_ids)} questions to {output_file}")


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Add an argument for the website URL
    parser.add_argument(
        "--url",
        type=str,
        default=BASE_URL,
        help="URL of the website",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="questions.jsonl",
        help="Path to save the questions",
    )
    parser.add_argument(
        "--first_page_index",
        type=int,
        default=0,
        help="Index of the first page to scrape",
    )
    parser.add_argument(
        "--last_page_index",
        type=int,
        default=10,
        help="Index of the last page to scrape",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Collect questions from the website
    questions = collect_questions(args.url, args.first_page_index, args.last_page_index)

    # Process the questions
    processed_questions = process_questions(questions)

    # Save the questions to a file
    save_questions(processed_questions, args.output_path)
