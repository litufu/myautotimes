import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

class Model(nn.Module):
    def __init__(self, configs):
        super(Model, self).__init__()
        self.device = configs.gpu
        print(self.device)
        model_name = "Qwen/Qwen3-1.7B-Base"

        self.qwen = AutoModelForCausalLM.from_pretrained(
            configs.llm_ckp_dir,
            device_map=self.device,
            torch_dtype=torch.float16,
        )
        self.qwen_tokenizer = AutoTokenizer.from_pretrained(configs.llm_ckp_dir)
        self.qwen_tokenizer.pad_token = self.qwen_tokenizer.eos_token
        self.vocab_size = self.qwen_tokenizer.vocab_size
        self.hidden_dim_of_qwen = 2048
        
        for name, param in self.qwen.named_parameters():
            param.requires_grad = False

    def tokenizer(self, x):
        output = self.qwen_tokenizer(x, return_tensors="pt")['input_ids'].to(self.device)
        result = self.qwen.get_input_embeddings()(output)
        return result   
    
    def forecast(self, x_mark_enc):        
        # x_mark_enc: [bs x T x hidden_dim_of_qwen]
        x_mark_enc = torch.cat([self.tokenizer(x_mark_enc[i]) for i in range(len(x_mark_enc))], 0)
        text_outputs = self.qwen.model(inputs_embeds=x_mark_enc)[0]
        text_outputs = text_outputs[:, -1, :]
        return text_outputs
    
    def forward(self, x_mark_enc):
        return self.forecast(x_mark_enc)