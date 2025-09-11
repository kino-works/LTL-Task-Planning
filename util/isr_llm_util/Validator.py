import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

class Validator(object):

    def __init__(self, arg, is_log_example=False, temperature=0):
        self.arg = arg
        self.model = arg.model
        self.temperature = temperature
        self.messages = None
        self.log_dir = arg.logdir
        self.log_file_path = os.path.join(self.log_dir, "validator_log.txt")
        self.is_log_example = is_log_example

        # Support only the household domain
        if self.arg.domain != 'household':
            raise ValueError(f"Unsupported domain for Validator: {self.arg.domain}")

        # Few-shot example settings
        self.max_examples = 8
        self.num_valid_example = min(self.arg.num_valid_ex, self.max_examples)
        # Directory containing opening.txt and example{i}.txt for household validation
        self.prompt_example_root = arg.valid_prompt_dir

        # Initialize message history
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

        # Load few-shot validation examples
        for i in range(self.num_valid_example):
            ex_path = os.path.join(self.prompt_example_root, f"example{i}.txt")
            with open(ex_path, 'r') as f:
                full = f.read().split('Answer:', 1)
            question = full[0]
            answer = 'Answer:' + full[1]

            self.messages.append({"role": "system", "name": "example_user", "content": question})
            self.messages.append({"role": "system", "name": "example_assistant", "content": answer})
            if self.is_log_example:
                self.write_content(question, is_append=True)
                self.write_content(answer, is_append=True)

    def query(self, content, is_append=False):
        # Build the message sequence for this validation query
        seq = self.messages.copy() if not is_append else self.messages
        seq.append({"role": "user", "content": content})
        self.write_content(content, is_append=True)

        # Call the OpenAI API
        response = client.chat.completions.create(
            model=self.model,
            messages=seq,
            temperature=self.temperature
        )
        # Extract and return the validator's response
        resp = response.choices[0].message.content
        self.write_content(resp, is_append=True)
        return resp
