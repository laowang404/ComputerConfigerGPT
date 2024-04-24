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
        pass

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level = self.log_level)
        handler = logging.FileHandler(self.log_file)
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
        while True:
            if flag == "user":
                input_message = input("请输入你的回应：")
                # 
                self.logger.info(f"User: {input_message}")
                next_scentence = (input_message, "user")
                flag = "GPT"
            elif flag == 'assistant':
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
        res_splt = response.split("\n")
        # import pdb ; pdb.set_trace()
        print()
        for line in res_splt:
            if line.startswith("询问客户"):
                return "user", (line, "GPT")
            if line.startswith("询问"):
                return "assistant", (line, "GPT")
            
        logging.warning("可能有错误")
        return "user", "可能有错误"

    def get_response(self):
        pass

    def save(self):
        pass

    def quit(self):
        pass




