from .spider import WebSpider
from .GPT import GPT
from .Assistant import Assistant
import logging
import datetime
import time
import random

def printer(text):
    """打字机效果"""
    
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(random.uniform(0.1, 0.13))


class CCGPT():
    
    def __init__(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = f"log_{current_time}.txt"
        self.log_level = logging.INFO
        self.logger = self.get_logger()

        self.spider = WebSpider()
        self.GPT = GPT()
        self.assistant = Assistant()

        self.prompt_dict = {
            "询问CPU": "cpu",
            "询问主板": "motherboard",
            "询问内存": "memory",
            "询问硬盘": "harddisk",
            "询问显卡": "graphicscard",
            "询问显示器": "monitor",
            "询问机箱": "chassis",
            "询问电源": "power",
            "询问固态": "ssd",
        }
        pass

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level = self.log_level)
        handler = logging.FileHandler(self.log_file ,encoding="utf-8")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # console = logging.StreamHandler()
        # console.setLevel(logging.INFO)
        
        logger.addHandler(handler)
        # logger.addHandler(console)
        
        return logger

    def train(self):
        self.assistant.train()
        self.GPT.train()
        pass

    def start(self):
        self.GPT.start()
        self.assistant.start()
        self.spider.start()
        pass

    def chat(self):
        flag = "user"
        next_scentence = "请输出相关"
        while flag != "finish":
            print("------------------")
            if flag == "user":
                input_message = input("请输入你的回应：")
                # import pdb; pdb.set_trace()
                # 
                self.logger.info(f"User: {input_message}")
                next_scentence = (input_message, "user")
                flag = "GPT"
            elif flag == 'assistant':
                # import pdb; pdb.set_trace()
                responce = self.assistant.chat(*next_scentence)
                print(responce)
                self.logger.info(f"Assistant: {responce}")
                next_scentence = (responce, "assistant")
                flag = "GPT"
                pass
            elif flag == 'GPT':
                
                responce = self.GPT.chat(*next_scentence)
                
                print(responce)
                self.logger.info(f"GPT: {responce}")
                flag, next_scentence = self.select_chatter(responce)
                pass

    def parser(self):
        pass

    def select_chatter(self, response):
        res_splt = response.split("\n\n")
        # import pdb ; pdb.set_trace()
        # print()
        for line in res_splt:
            if line.startswith("询问客户"):
                return "user", (line, "GPT")
            if line.startswith("询问"):
                hardware = line.split("：")[0]
                # 如果hardware中包含“专家”，删除这两个字
                hardware = hardware.replace("专家", "")
                if hardware in self.prompt_dict.keys():
                    return "assistant", (line, hardware)
                else:
                    regeneration_prompt = "请你严格按照回复格式重新回复，每次请求只允许询问一个硬件的信息。"
                    return "GPT", (regeneration_prompt, "user")
        
        # regeneration_prompt = "请你严格按照回复格式重新回复"
        self.logger.info("------------配置完成------------")
        return "finish", None

    def get_response(self):
        pass

    def save(self):
        pass

    def quit(self):
        pass




