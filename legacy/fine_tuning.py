import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def prepare_dataset():
    # This is a placeholder function. In a real-world scenario, you would
    # prepare your dataset of UX research interview transcripts here.
    dataset = [
        {"messages": [
            {"role": "system", "content": "You are a UX research expert."},
            {"role": "user", "content": "Analyze this UX research interview transcript: [Transcript text]"},
            {"role": "assistant", "content": "[Expert analysis of the transcript]"}
        ]}
        # Add more examples here
    ]
    
    with open('ux_research_dataset.jsonl', 'w') as f:
        for item in dataset:
            f.write(json.dumps(item) + '\n')
    
    return 'ux_research_dataset.jsonl'

def fine_tune_model(dataset_file):
    file_response = openai_client.files.create(file=open(dataset_file, "rb"), purpose='fine-tune')
    file_id = file_response.id

    fine_tuning_job = openai_client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo-0613"
    )

    # Wait for the fine-tuning to complete (this is a simplified version)
    while True:
        job_status = openai_client.fine_tuning.jobs.retrieve(fine_tuning_job.id)
        if job_status.status == 'succeeded':
            return job_status.fine_tuned_model
        elif job_status.status == 'failed':
            raise Exception("Fine-tuning failed")

    return None
