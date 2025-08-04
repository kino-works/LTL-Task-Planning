from openai import AzureOpenAI
from copy import deepcopy
import os
import tiktoken
import torch
from transformers import AutoTokenizer, pipeline
from dotenv import load_dotenv


load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
MAX_NEW_TOKENS = 16384


class LLMBase:
    def __init__(self, temp: float = 0., top_p: float = 1.):
        self.temperature = temp
        self.top_p = top_p
        self.prompt_chain = []
        torch.cuda.empty_cache()

    def reset(self):
        self.prompt_chain = []
        torch.cuda.empty_cache()

    def count_tokens(self, string: str):
        pass

    def init_prompt_chain(self, content: str, prompt: str):
        pass

    def update_prompt_chain(self, content: str, prompt: str):
        pass

    def update_prompt_chain_w_response(self, response: str, role: str = "assistant"):
        self.prompt_chain.append({"role": role, "content": response})

    def query(self, content: str, prompt: str):
        pass

    def query_msg_chain(self):
        pass

    @staticmethod
    def log(context: str, save_name: str):
        with open(save_name, "w") as f:
            f.write(context)


class Llama3(LLMBase):
    def __init__(self, model_name: str, temp: float = 0., top_p: float = 1.):
        super().__init__(temp, top_p)
        self.model_id = "meta-llama/Meta-{}".format(model_name)
        self.pipeline = pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={
                "torch_dtype": torch.float16,
                "quantization_config": {
                    "load_in_4bit": True,
                    "bnb_4bit_compute_dtype": torch.bfloat16
                },
                "low_cpu_mem_usage": True,
            },
            device_map="auto"
        )
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

    def count_tokens(self, string: str):
        tokens = self.pipeline.tokenizer.tokenize(string)
        return len(tokens)

    def init_prompt_chain(self, content: str, prompt: str):
        assert len(self.prompt_chain) == 0, "Prompt chain is not empty!"
        self.prompt_chain.extend([{"role": "system", "content": content},
                                  {"role": "user", "content": prompt}])

    def update_prompt_chain(self, content: str, prompt: str):
        self.prompt_chain[0]["content"] = content
        self.prompt_chain.append({"role": "user", "content": prompt})

    def query(self, content: str, prompt: str):
        messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": prompt}
        ]
        response = self.pipeline(
            messages,
            max_new_tokens=MAX_NEW_TOKENS,
            eos_token_id=self.terminators,
            pad_token_id=self.pipeline.tokenizer.eos_token_id,
            do_sample=True,
            # temperature=self.temperature,
            # top_p=self.top_p,
        )
        output = response[0]["generated_text"][-1]['content']
        torch.cuda.empty_cache()
        return output

    def query_msg_chain(self):
        response = self.pipeline(
            self.prompt_chain,
            max_new_tokens=MAX_NEW_TOKENS,
            eos_token_id=self.terminators,
            pad_token_id=self.pipeline.tokenizer.eos_token_id,
            do_sample=True,
            # temperature=self.temperature,
            # top_p=self.top_p,
        )
        output = response[0]["generated_text"][-1]['content']
        torch.cuda.empty_cache()
        return output


class GPT(LLMBase):
    def __init__(self, model_name: str, temp: float = 0., top_p: float = 1.):
        super().__init__(temp, top_p)
        self.model_id = model_name
        self.key = AZURE_API_KEY
        self.client = AzureOpenAI(
            api_key=self.key,
            api_version="2024-02-15-preview",
            azure_endpoint=AZURE_ENDPOINT
        )

    def count_tokens(self, string: str):
        encoding_name = deepcopy(self.model_id)
        if "gpt-35" in encoding_name:
            encoding_name.replace("gpt-35", "gpt-3.5")
        encoding = tiktoken.encoding_for_model(encoding_name)
        return len(encoding.encode(string))

    def init_prompt_chain(self, content: str, prompt: str):
        assert len(self.prompt_chain) == 0, "Prompt chain is not empty!"
        self.prompt_chain.extend([{"role": "system", "content": content},
                                  {"role": "user", "content": prompt}])

    def update_prompt_chain(self, content: str, prompt: str):
        self.prompt_chain[0]["content"] = content
        self.prompt_chain.append({"role": "user", "content": prompt})

    def query(self, content: str, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model_id,
            temperature=self.temperature,
            # top_p=self.top_p,
            # frequency_penalty=0,
            # presence_penalty=0,
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def query_msg_chain(self):
        response = self.client.chat.completions.create(
            model=self.model_id,
            temperature=self.temperature,
            # top_p=self.top_p,
            # frequency_penalty=0,
            # presence_penalty=0,
            messages=self.prompt_chain
        )
        return response.choices[0].message.content


def load_llm(model_name: str, temp: float = 0., top_p: float = 1.):
    if "llama" in model_name.lower():
        return Llama3(model_name, temp, top_p)
    elif "gpt" in model_name.lower():
        return GPT(model_name, temp, top_p)
    else:
        raise Exception("Invalid model name!")
