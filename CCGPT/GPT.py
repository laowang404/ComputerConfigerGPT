from zhipuai import ZhipuAI

class GPT():
    def __init__(self) -> None:
        self.name = 'GPT'
        self.client = ZhipuAI(api_key="5e7362150b39d6a2432e6781f926b3bc.oPMWsX4QvLXkX544")
        self.message = [
            {"role": "system", "content": "你是一名专业的台式机装机专家，知晓装机过程中的各种细节，能够根据客户的装机需求，提供可靠的装机方案。"
                                          "在配置过程中，你将需要询问其他的硬件专家关于当前硬件具体信息及对应价格，包括CPU、主板、内存、硬盘、显卡、显示器、机箱、电源、散热器等。"
                                          "你需要自行分配各个部分的成本，例如将10000的预算分配3000给CPU，分配4000给显卡等，在这个过程中你可能多次请求同一类硬件的信息，每一次请求仅请求一个类别的硬件。"
                                          "每一步询问的结果都将影响到最终的装机方案，所以请你认真对待每一步询问，确保最终的装机方案是合理的。"
                                          "例如询问CPU硬件专家的模板如下："
                                          "询问CPU：当前在2000元价位的CPU中，性能较好的有哪些？"
                                          "你将会收到其他硬件专家的回答，该信息以相应的专家信息起头，例如\"CPU专家：\"，然后你可以根据回答的内容，继续询问其他硬件的信息。"
                                          "如果你对部分配置的选择不确定，可以向客户提出询问，确定对应配置的信息，询问客户的模板以\"询问客户：\"开头。"
                                          "当你认为已经收集到足够的硬件信息后，你可以根据客户的需求，提供一台合理的装机方案。"
                                          "如果客户对你的方案有疑问，你可以继续询问硬件专家，直到客户满意为止。"
                                          "客户每次询问都会以\"客户：\"开头，你需要根据客户的答复，继续询问硬件专家。"},
            {"role": "user", "content": "客户：请你配置一台CPU性能更强的5000元内的主机"}
        ]
    
    def train(self):
        pass

    def start(self):
        pass

    def chat(self, next_scentence, flag):
        self.message.append({"role": "user", "content": next_scentence})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.message,
        )
        self.message.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    




