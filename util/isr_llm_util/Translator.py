import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

class Translator(object):
    """
    LLM Translator: translates a natural language household task description
    into a complete PDDL problem file (including :init and :goal sections).
    """
    def __init__(self, arg, is_log_example=False, temperature=0):
        self.arg = arg
        self.model = arg.model
        self.temperature = temperature
        self.messages = None
        self.log_dir = arg.logdir
        self.log_file_path = os.path.join(self.log_dir, "translator_log.txt")
        self.is_log_example = is_log_example

        # Support only household domain
        if self.arg.domain != 'household':
            raise ValueError(f"Unsupported domain for Translator: {self.arg.domain}")

        # Set example root for household domain
        self.max_examples = 4
        self.num_trans_example = min(arg.num_trans_ex, 3)
        self.prompt_example_root = arg.trans_prompt_dir

        # Initialize few-shot messages
        self.init_messages()

    def write_content(self, content, is_append):
        mode = 'a' if is_append else 'w'
        os.makedirs(self.log_dir, exist_ok=True)
        with open(self.log_file_path, mode) as f:
            f.write(content + "\n")

    def init_messages(self):
        # Load opening prompt
        opening_path = os.path.join(self.prompt_example_root, "opening.txt")
        with open(opening_path, 'r') as f:
            opening = f.read()
        self.messages = [{"role": "system", "content": opening}]
        if self.is_log_example:
            self.write_content(opening, is_append=False)

        # Load few-shot examples
        for i in range(self.num_trans_example):
            ex_path = os.path.join(self.prompt_example_root, f"example{i}.txt")
            with open(ex_path, 'r') as f:
                full = f.read().split('\n', 1)
            user_q, assistant_a = full[0], full[1]
            self.messages.append({"role": "system", "name": "example_user", "content": user_q})
            self.messages.append({"role": "system", "name": "example_assistant", "content": assistant_a})
            if self.is_log_example:
                self.write_content(user_q, is_append=True)
                self.write_content(assistant_a, is_append=True)

    def query(self, content, is_append=False):
        # Build messages sequence
        seq = self.messages.copy() if not is_append else self.messages
        seq.append({"role": "user", "content": content})
        self.write_content(content, is_append=True)

        # Call OpenAI
        response = client.chat.completions.create(
            model=self.model,
            messages=seq,
            temperature=self.temperature
        )
        resp = response.choices[0].message.content
        self.write_content(resp, is_append=True)
        return resp
