import openai
from openai import OpenAI
from copy import deepcopy
import os
import tiktoken
from dotenv import load_dotenv
import torch

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
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

class GPT(LLMBase):
    def __init__(self, model_name: str, temp: float = 0., top_p: float = 1.):
        super().__init__(temp, top_p)
        self.model_id = model_name
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def count_tokens(self, string: str):
        encoding_name = deepcopy(self.model_id)
        if "gpt-35" in encoding_name:
            encoding_name = encoding_name.replace("gpt-35", "gpt-3.5")
        encoding = tiktoken.encoding_for_model(encoding_name)
        return len(encoding.encode(string))

    def init_prompt_chain(self, content: str, prompt: str):
        assert len(self.prompt_chain) == 0, "Prompt chain is not empty!"
        self.prompt_chain.extend([
            {"role": "system", "content": content},
            {"role": "user",   "content": prompt}
        ])

    def update_prompt_chain(self, content: str, prompt: str):
        self.prompt_chain[0]["content"] = content
        self.prompt_chain.append({"role": "user", "content": prompt})

    def query(self, content: str, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": content},
                {"role": "user",   "content": prompt}
            ],
            temperature=self.temperature,
            top_p=self.top_p
        )
        return completion.choices[0].message.content

    def query_msg_chain(self):
        completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=self.prompt_chain,
            temperature=self.temperature,
            top_p=self.top_p
        )
        return completion.choices[0].message.content

def load_llm(model_name: str, temp: float = 0., top_p: float = 1.):
    if "llama" in model_name.lower():
        return Llama3(model_name, temp, top_p)
    elif "gpt" in model_name.lower():
        return GPT(model_name, temp, top_p)
    else:
        raise Exception("Invalid model name!")
