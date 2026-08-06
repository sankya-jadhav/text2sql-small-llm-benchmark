import time
import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from src.model_runner import ModelRunner
from src.models import GenerationResult
from src.sql_cleaner import SQLCleaner
from transformers import BitsAndBytesConfig

from config import (
    LOAD_IN_4BIT,
    MODEL_NAME
)
from src.logger import get_logger

logger = get_logger(__name__)

class HFRunner(ModelRunner):
    """
    Hugging Face implementation of ModelRunner.

    Supports:
    - Qwen
    - DeepSeek
    - Llama
    """

    def __init__(self, model_name: str):

        super().__init__(model_name)

        logger.info(f"Loading model: {model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        if LOAD_IN_4BIT:

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )

        else:

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )

        self.model.eval()

        logger.info("Model loaded successfully.")

    def generate(
        self,
        prompt: str,
        prompt_type: str
    ) -> GenerationResult:

        start = time.perf_counter()

        try:

            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            formatted_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt"
            ).to(self.model.device)

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False
            )

            generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
           

            generated_text = self.tokenizer.decode(
                generated_ids,
                skip_special_tokens=True
            )

            
            generated_text = SQLCleaner.clean(
                generated_text
            )


            latency = time.perf_counter() - start

            prompt_tokens = inputs["input_ids"].shape[1]
            completion_tokens = generated_ids.shape[0]

            return GenerationResult(

                model_name=self.model_name,

                prompt_type=prompt_type,

                prompt=prompt,

                generated_sql=generated_text,

                latency=latency,

                success=True,

                prompt_tokens=prompt_tokens,

                completion_tokens=completion_tokens,

                total_tokens=prompt_tokens + completion_tokens
            )

        except Exception as e:

            latency = time.perf_counter() - start

            return GenerationResult(

                model_name=self.model_name,

                prompt_type=prompt_type,

                prompt=prompt,

                generated_sql="",

                latency=latency,

                success=False,

                error=str(e)
            )