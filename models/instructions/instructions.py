import json, os
from modules.palette import Palette as p


class Instructor:
    def __init__(self):
        self.instructions_path = "models/instructions/instructions.json"
        
        
    def choose(self,args:list[str],prompt:str=None):
        if not os.path.exists(self.instructions_path) or not os.path.isfile(self.instructions_path):
            raise FileNotFoundError(f"Instructions file not found at '{self.instructions_path}'")
        
        with open(self.instructions_path, "r") as f:
            instructions = json.load(f)
        
        if "examles" in instructions and "examples" not in instructions:
            instructions["examples"] = instructions.pop("examles")
            
        hf = instructions.get("hf_stop_tokens")
        if isinstance(hf, list) and len(hf) == 1 and isinstance(hf[0], dict):
            instructions["hf_stop_tokens"] = hf[0]
            
        
        possible = {"describe","instructions","stop_tokens","hf_stop_tokens","examples"}
        if not args:
            raise ValueError("No arguments provided")
        if prompt is None:
            return {arg: instructions[arg] for arg in args}
        parts: list[str] = []
        for arg in args:
            if arg not in possible:
                raise ValueError(f"Invalid argument '{arg}'. Possible values are {possible}")
            match arg:
                case "describe":
                    parts.append(instructions.get("describe", ""))
                case "instructions":
                    parts.extend(instructions.get("instructions", []))
                case "examples":
                    for ex in instructions.get("examples", []):
                        parts.append(f"Input: {ex['input']}\nOutput: {ex['output']}")
                case _:
                    continue
        parts.append(f"Input: {prompt}\nOutput:")
        return "\n\n".join(parts)
        