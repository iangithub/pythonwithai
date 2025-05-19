from openai import OpenAI
import time

client = OpenAI(
    api_key = "sk-xx",
)    

batch_file = client.files.create(
  file=open("5-5/mydata.jsonl", "rb"),
  purpose="batch"
)

file_id = batch_file.id
print(file_id)


batch_job = client.batches.create(
  input_file_id=file_id,
  endpoint="/v1/chat/completions",
  completion_window="24h"
)

batch_id = batch_job.id
print(f"Batch Job ID: {batch_id}")

while True:
    job_status = client.batches.retrieve(batch_id)
    if job_status.status == "completed":
        print("Batch job completed!")
        result_file_id = job_status.output_file_id
        result = client.files.content(result_file_id).content
        result_file_name = "5-5/batch_job_results.jsonl"
        with open(result_file_name, 'wb') as file:
            file.write(result)
        break

    elif job_status.status in ["failed", "canceled", "expired"]:
        raise RuntimeError(f"Batch job ended with status: {job_status.status}")
    
    else:
        print(f"Current status: {job_status.status}... waiting")
        time.sleep(5)