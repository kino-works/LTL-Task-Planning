import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

class Planner(object):
    """
    LLM Planner: generates action sequences for the household domain.
    """
    def __init__(self, arg, is_log_example=False, temperature=0):
        self.arg = arg
        self.model = arg.model
        self.temperature = temperature
        self.messages = None
        self.log_dir = arg.logdir
        self.log_file_path = os.path.join(self.log_dir, "planner_log.txt")
        self.is_log_example = is_log_example

        # Support only the household domain
        if self.arg.domain != 'household':
            raise ValueError(f"Unsupported domain for Planner: {self.arg.domain}")

        # Few-shot example settings
        self.max_examples = 4
        self.num_plan_example = min(self.arg.num_plan_ex, self.max_examples)
        # Directory containing opening.txt and example{i}.txt for household
        self.prompt_example_root = arg.plan_prompt_dir

        # Initialize message history
        self.init_messages()

    def write_content(self, content, is_append):
        mode = 'a' if is_append else 'w'
        os.makedirs(self.log_dir, exist_ok=True)
        with open(self.log_file_path, mode) as f:
            f.write(content + "\n")

    def init_messages(self, is_reinitialize: bool = False):
        # Load opening prompt
        opening_path = os.path.join(self.prompt_example_root, "opening.txt")
        with open(opening_path, 'r') as f:
            opening = f.read()
        self.messages = [{"role": "system", "content": opening}]
        if self.is_log_example:
            self.write_content(opening, is_append=False)

        # Load few-shot planning examples
        for i in range(self.num_plan_example):
             ex_path = os.path.join(self.prompt_example_root, f"example{i}.txt")
             with open(ex_path, 'r') as f:
                 full = f.read().split('Action Sequence', 1)
             question = full[0]
             answer   = 'Action Sequence' + full[1]

             self.messages.append({"role": "system", "name": "example_user",      "content": question})
             self.messages.append({"role": "system", "name": "example_assistant", "content": answer})
             if self.is_log_example and not is_reinitialize:
                 self.write_content(question, is_append=True)
                 self.write_content(answer,   is_append=True)

    def query(self, content, is_append = False, temperature: float = None):
        # Build the message sequence for this query
        seq = self.messages.copy() if not is_append else self.messages
        seq.append({"role": "user", "content": content})
        self.write_content(content, is_append=True)

        # Call the OpenAI API
        use_temp = self.temperature if temperature is None else temperature
        response = client.chat.completions.create(
            model=self.model,
            messages=seq,
            temperature=use_temp
        )
        # Extract the planner's response
        resp = response.choices[0].message.content
        self.write_content(resp, is_append=True)
        return resp
