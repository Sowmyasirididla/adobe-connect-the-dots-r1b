# Connecting the Dots Challenge - Round 1B Solution

## Teammates 
- Didla Sowmya Siri
- Hanshika Misra

## Project Overview

This repository contains my solution for Round 1B of the "Connecting the Dots" Challenge. The goal is to process multiple PDFs along with a persona and job description to:

- Extract hierarchical sections (headings with their texts) from each PDF.
- Rank the sections for relevance to the provided persona and job-to-be-done using offline sentence embeddings.
- Output a JSON file that includes metadata, prioritized sections, and refined subsection texts.

This enables persona-driven document intelligence across a collection of heterogeneous documents.

## Folder Structure

- `/input`  
  Place all input PDFs and the `persona_job.json` file here.

- `/output`  
  The solution writes the final result JSON file here.

- `main.py`  
  The main controller script that orchestrates extraction, ranking, and output generation.

- `pdf_parser.py`  
  Contains modular functions to parse PDFs, extract headings, and capture section text.

- `ranker.py`  
  Implements section ranking based on sentence-transformers embeddings and cosine similarity.

- `requirements.txt`  
  Lists required Python packages.

- `Dockerfile`  
  Defines the environment and builds an offline, CPU-only container to run the solution.

- `README.md`  
  This documentation file.

## How to Build the Docker Image

Run the following command in the root directory of this repository:

docker build --platform linux/amd64 -t yourimagename:round1b .


Replace `yourimagename` with your preferred Docker image name.

## How to Run the Solution

Ensure all input files (PDFs and `persona_job.json`) are placed inside the `input/` folder.

Run the container with:

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none yourimagename:round1b


- All PDFs inside `/app/input` are processed.
- Outputs are saved as JSON files inside `/app/output`.
- The solution does not require internet access at runtime per challenge constraints.

## Input Format

**`persona_job.json`** (example):

{
"persona": "Computer Science Graduate Student",
"job_to_be_done": "Analyze and summarize key Adobe Creative Cloud features and emerging trends in AI and cloud computing."
}

PDF files should be well-structured and placed alongside this JSON file in `input/`.

## Output Format

- Outputs a single JSON file `result.json` to `/output`.
- Includes:
  - Metadata (input docs, persona, job, timestamp)
  - Extracted and ranked sections (document name, page number, section title, importance rank)
  - Subsection analysis with refined text

## Constraints and Compliance

- Runs offline and CPU-only on AMD64 architecture.
- Model size and dependencies kept under 1GB.
- Execution time ≤ 60 seconds for 3–5 documents.
- No internet access during image build or runtime.
- Docker image built with locked dependencies and pre-downloaded embedding model.

## Known Limitations

- Extraction and ranking rely on heuristic and pretrained models and may vary with document complexity.
- No GPU acceleration.
- Summary/refinement is basic extraction; no advanced NLP summarization.

## Contact

For questions or support, please contact via the GitHub repository.

---

Thank you!

