from zhipuai import ZhipuAI

class GPT():
    def __init__(self) -> None:
        self.name = 'GPT'
        self.client = ZhipuAI(api_key="9a0cb62c576a25d83a00ac432c5fcc7a.Wkl0gAJVDuvu1EAS")
        self.message = [
            {"role": "system", "content": "你是一名专业的台式机装机专家，知晓装机过程中的各种细节，能够根据客户的装机需求，提供可靠的装机方案。"
                                          "在配置过程中，你将需要询问其他的硬件专家关于当前硬件具体信息及对应价格，包括CPU、主板、内存、硬盘、显卡、显示器、机箱、电源，并确定这8项硬件的具体配置，请勿询问这8项以外的硬件。"
                                          "你需要自行分配各个部分的成本，例如将10000的预算分配3000给CPU，分配4000给显卡等，选择的配置尽可能充分利用预算。"
                                          "如果CPU支持核显，那么可以考虑不选用显卡。"
                                          "在这个过程中你可多次请求同一类硬件的信息，注意每一次仅请求一个类别的硬件，请勿同时请求多个类别硬件，询问过程中的价位必须是对应当前硬件的，不应使用剩余预算询问。"
                                          "例如询问CPU硬件专家的模板如下：\n\n"
                                          "询问CPU：当前在2000元价位的CPU中，性能较好的有哪些？\n\n"
                                          "你将会收到对应硬件专家的回答，该信息以相应专家信息起头，例如\n\nCPU专家：\n\n，然后你可以根据回答的内容，选择接近对应预算的产品，确认自己已完成的硬件配置和未完成的硬件类别，以及当前剩余预算，然后继续逐个询问其他硬件信息。"
                                          "如果专家提供的信息价格和预算相差较大，你可以进一步强调配置信息，以便专家提供更合适的选择。"
                                          "如果你对部分配置的选择不确定，或完成所有配置内容后，可以向客户提出询问，确定对应配置的信息，询问客户的模板以\n\n询问客户：\n\n开头。"
                                          # "当你认为已经收集到足够的硬件信息后，你可以根据客户的需求，提供一台合理的装机方案。"
                                          # "如果客户对你的方案有疑问，你可以继续询问硬件专家，直到客户满意为止。"
                                          "客户每次回复都会以\n\n客户：\n\n开头，你需要根据客户的答复，继续按照以上要求询问对应的硬件专家，直到客户满意为止。"
                                          "请勿自己充当某一硬件专家的角色，请严格遵循以上交流的格式，每次请求只允许询问一类硬件。"
                                          "请你务必在得到客户需求时将分配好的预算展示出来，并在每次更新配置后展示预算使用情况。"},
            # {"role": "user", "content": "客户：请你配置一台CPU性能更强的5000元内的主机"}
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
    




