import os
import torch
from transformers import (
    AutoModelForCausalLM,
    GenerationConfig,
    BitsAndBytesConfig,
    StoppingCriteriaList,
    StoppingCriteria
    )
from models.services.tokenizer_work import TokenizerWork as tw
from modules.palette import Palette as p
from models.instructions.instructions import Instructor

class Executer:
    def __init__(
        self,
        save_dir: str = "models/core/llama-7b",
        load_in_4bit: bool = True,
        offload_folder: str = "offload",
        torch_dtype: torch.dtype = torch.float16,
        auth_token: str = None,
        **generation_overrides
    ):
        if not os.path.isdir(save_dir) or not os.path.exists(os.path.join(save_dir, "config.json")):
            raise FileNotFoundError(f"model not founded in '{save_dir}'. Firstly start LlamaDownloader.download()")

        self.tokenizer = tw(save_dir).get_tokenizer() 
        self.eos_token_id = self.tokenizer.eos_token_id
        self.tokenizer.pad_token_id = self.eos_token_id
        self.generation_config = GenerationConfig.from_pretrained(save_dir)
        self.generation_config.pad_token_id = self.eos_token_id
        self.generation_config.eos_token_id = self.eos_token_id
        self.auth = auth_token
        
        quant_config = BitsAndBytesConfig(
            load_in_4bit=load_in_4bit,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
            llm_int8_enable_fp32_cpu_offload=True
        )


        self.model = AutoModelForCausalLM.from_pretrained(
            save_dir,
            quantization_config=quant_config,
            device_map="auto",
            offload_folder=offload_folder,
            offload_state_dict=True,
            torch_dtype=torch_dtype
        )
        self.model.config.pad_token_id = self.eos_token_id
        self.model.config.eos_token_id = self.eos_token_id
        
        self.model.generation_config = self.generation_config
        for key, value in generation_overrides.items():
            setattr(self.generation_config, key, value)
        
        stop_tokens = Instructor().choose(args=["stop_tokens"])["stop_tokens"]
        class StopOnTokens(StoppingCriteria):
            def __init__(self, tokenizer, stop_tokens_list):
                super().__init__()
                self.stop_ids = [
                    tokenizer(seq, add_special_tokens=False)["input_ids"]
                    for seq in stop_tokens_list
                ]

            def __call__(self, input_ids, scores, **kwargs):
                for seq in self.stop_ids:
                    if input_ids[0][-len(seq):].tolist() == seq:
                        return True
                return False

        self.stopping_criteria = StoppingCriteriaList([
            StopOnTokens(self.tokenizer, stop_tokens)
        ])


    def generate(
        self,
        prompt: str,
        **generate_overrides
    ) -> str:
        f_prompt = Instructor().choose(
            args=["describe","instructions","examples"],
            prompt=prompt
        )

        inputs = self.tokenizer(f_prompt, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        gen_kwargs = self.generation_config.to_dict()
        gen_kwargs.pop("max_length", None)
        gen_kwargs.pop("max_new_tokens", None)


        gen_kwargs["eos_token_id"] = self.eos_token_id
        gen_kwargs["pad_token_id"] = self.eos_token_id
        gen_kwargs["stopping_criteria"] = self.stopping_criteria
        gen_kwargs.update(generate_overrides)

        
        output_ids = self.model.generate(**inputs, **gen_kwargs)
        raw = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        if raw.startswith(f_prompt):
            raw = raw[len(f_prompt):]

        stop_tokens = Instructor().choose(args=["stop_tokens"])["stop_tokens"]
        for tok in stop_tokens:
            idx = raw.find(tok)
            if idx != -1:
                raw = raw[:idx]

        return raw.strip()
