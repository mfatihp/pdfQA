import torch
import transformers


class LibrarianLLM:
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.2-1B-Instruct"

        self.pipeline = transformers.pipeline(task="text-generation",
                                              model=self.model_name,
                                              torch_dtype=torch.bfloat16,
                                              device_map="auto")
