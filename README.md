# CDL @ Hack4SocialGood 2025: Extracting Funding Amounts from State Funding Programs

- Development of a method to automatically extract funding amounts from funding programs.
- The problem can be framed as a Named Entity Recognition (NER) or information extraction task.
- The data basis consists of funding programs that are part of the German federal government's "Förderdatenbank" (funding database). These have been scraped and published [here](https://github.com/CorrelAid/cdl_funding_crawler).
- The background is an attempt to quantify how much the German government spends on promoting democracy. As a first step, a classifier has already been developed to identify democracy funding programs. The next step is the extraction of funding amounts. You can find an article on the project (in German!) [here](https://civic-data.de/transparente_demokratiefoerderung/).

## Data

- The data originates from the website: [www.foerderdatenbank.de](www.foerderdatenbank.de)
- A description of the scraped dataset, as well as the link to the data, can be found [here](https://github.com/CorrelAid/cdl_funding_crawler).
- An example of how the data can be read using Python is available [here](https://github.com/CorrelAid/cdl_funding_crawler/blob/main/index.ipynb)

## Possible Approaches

- NER using the Python package spaCy.
- Fine-tuning language models like BERT.
- In-context learning with generative LLMs.

## Important Considerations
- The method should be evaluated using suitable metrics such as the F1 Score or Accuracy.

## Setup

1. Install [uv](https://docs.astral.sh/uv/#installation)

2. uv sync

### Example Jupyte

## pdf Liste von im Jahr 2023 geförderten Organisationen:
[hier](https://dserver.bundestag.de/btd/20/102/2010233.pdf)
