import os
import json
from datetime import datetime
import pdf_parser
import ranker

def load_persona_job(input_dir):
    pj_path = os.path.join(input_dir, "persona_job.json")
    if not os.path.isfile(pj_path):
        raise FileNotFoundError(f"persona_job.json not found in {input_dir}")
    with open(pj_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    persona = data.get("persona", "")
    job_to_be_done = data.get("job_to_be_done", "")
    return persona, job_to_be_done

def main():
    input_dir = "./input"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    # Load persona and job description
    persona, job_to_be_done = load_persona_job(input_dir)

    # List all PDFs in input directory (exclude other files)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    all_sections = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"Extracting sections from {pdf_file}...")
        sections = pdf_parser.extract_sections(pdf_path)
        # Add document info to each section
        for sec in sections:
            sec["document"] = pdf_file
        all_sections.extend(sections)

    if not all_sections:
        print("No sections extracted from input PDFs.")
    else:
        print(f"Extracted a total of {len(all_sections)} sections from {len(pdf_files)} PDFs.")

    # Rank sections by relevance to persona and job
    print("Ranking sections by relevance...")
    ranked_sections = ranker.rank_sections(all_sections, persona, job_to_be_done)
    print(f"Ranking complete. Preparing output...")

    # Prepare output JSON data
    extracted_sections = []
    sub_section_analysis = []

    for sec in ranked_sections:
        extracted_sections.append({
            "document": sec["document"],
            "page_number": sec["page"],
            "section_title": sec["title"],
            "importance_rank": sec.get("importance_rank", 0.0)
        })
        sub_section_analysis.append({
            "document": sec["document"],
            "page_number": sec["page"],
            "refined_text": sec.get("text", "")
        })

    output_json = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": extracted_sections,
        "sub_section_analysis": sub_section_analysis
    }

    # Write the output JSON to output folder
    output_path = os.path.join(output_dir, "result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(pdf_files)} PDFs. Results saved to {output_path}.")

if __name__ == "__main__":
    main()
