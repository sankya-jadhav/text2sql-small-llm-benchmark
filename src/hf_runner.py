import time

import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from src.model_runner import ModelRunner
from src.models import GenerationResult


class HFRunner(ModelRunner):

    def __init__(self, model_name):

        super().__init__(model_name)

        print(f"Loading {model_name}...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )

        print("Model Loaded Successfully!")

    def generate(
        self,
        prompt,
        prompt_type
    ):

        start = time.perf_counter()

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(

            **inputs,

            max_new_tokens=256,

            temperature=0.0,

            do_sample=False

        )

        generated_text = self.tokenizer.decode(

            outputs[0],

            skip_special_tokens=True

        )

        latency = time.perf_counter() - start

        completion = generated_text[len(prompt):].strip()

        return GenerationResult(

            model_name=self.model_name,

            prompt_type=prompt_type,

            prompt=prompt,

            generated_sql=completion,

            latency=latency,

            success=True,

            prompt_tokens=inputs["input_ids"].shape[1],

            completion_tokens=outputs.shape[1] - inputs["input_ids"].shape[1],

            total_tokens=outputs.shape[1]
        )