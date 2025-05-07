from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from llama_index.prompts.prompts import SimpleInputPrompt
import torch


def load_model(model_name="TheBloke/Llama-2-7b-Chat-GPTQ", device='gpu'):
    # setting device
    if device == 'gpu':
        gpu=0
        device = torch.device(f"cuda:{gpu}" if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available():
            torch.cuda.set_device(device)
        torch.cuda.get_device_name(0)
    elif device == 'cpu':
        device = torch.device('cpu')
        torch.cuda.set_device(device)

    with open('huggingface_credentials.txt', 'r') as file:
        hf_token = file.readline().strip()

    login(token=hf_token)

    # Create tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name
        ,device_map='cuda'                 
        )

    # Define model
    model = AutoModelForCausalLM.from_pretrained(model_name
        # ,cache_dir=r"C:\Users\henry\.cache\huggingface\hub"
        # ,cache_dir=r"C:\Users\user2\.cache\huggingface\hub"
        ,device_map='cuda'  
        # , torch_dtype=torch.float16
        # ,low_cpu_mem_usage=True
        # ,rope_scaling={"type": "dynamic", "factor": 2}
        # ,load_in_8bit=True,
        ).to(device)

    # streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    # model_obj = {"model": model, "tokenizer": tokenizer, "streamer": streamer, "device": device,  }
    model_obj = {"model": model, "tokenizer": tokenizer, "device": device,  }

    return model_obj


def llm_inference(transcript, model, tokenizer, device, streamer=None, max_length=4000, ):
    plain_text = f"""
متنی که در ادامه آمده، خروجی یک سیستم تشخیص گفتار است. لطفاً این متن را بازنویسی کن تا ایرادات املایی، نگارشی و جدانویسی آن برطرف شود، اما معنی جمله تغییر نکند:

متن: {transcript}
"""
    input_ids = tokenizer(
        plain_text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        )['input_ids'].to(device)
    
    output_ids = model.generate(input_ids
                        # ,streamer=streamer
                        ,use_cache=True
                        ,max_new_tokens=float('inf')
                       )
    answer = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return answer

model_name = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ" 

model_obj = load_model(model_name)
model = model_obj["model"]
tokenizer = model_obj["tokenizer"]
device = model_obj["device"]
streamer = model_obj["streamer"]

# Mistral
system_prompt_mistral = """<|im_start|>system
You are a language refinement assistant that specializes in cleaning up imperfect speech-to-text outputs.
Your job is to correct punctuation, spacing, typos, and word recognition errors in Persian or English transcriptions, while preserving the original meaning as much as possible.
You may fix grammar and clarity, but do not rephrase the sentence entirely or change its intended meaning.
Do not add explanations or comments—just return the cleaned-up version of the text.
Respond only with the corrected version of the input text.
<|im_end|>
<|im_start|>user
"""

query_wrapper_prompt_mistral = SimpleInputPrompt("""{query_str} <|im_end|>
<|im_start|>assistant
""")

system_prompt = system_prompt_mistral
query_wrapper_prompt = query_wrapper_prompt_mistral