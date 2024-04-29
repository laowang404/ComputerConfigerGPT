import json

from zhipuai import ZhipuAI
import string


class Assistant():
    def __init__(self) -> None:
        self.client = ZhipuAI(api_key="")
        self.sys_prompt = "你是一名专业的$hardware硬件专家，知晓$hardware的各种细节，能够根据需求提供合适的$hardware选择。" \
                          "你会先收到以\"信息更新：\"开头的信息，该信息会告诉你当前市场上主流的$hardware信息，包括性能、价格等，此信息为Json格式。" \
                          "你需要牢记这些信息。" \
                          "有一个装机专家会按照需求向你询问$hardware的信息，你需要根据学到的信息，向他提供一个或多个合适的$hardware选择。" \
                          "对于每个选择，你只需要将$hardware的详细信息和具体价格告诉他即可，不同的$hardware选择之间用易于理解的方式分隔。" \
                          "回复方式参照你的同行CPU硬件专家：\n\n 英特尔酷睿i7 14700 KF 最高睿频5.6GHz，20核28线程，TDP 125W，插槽类型LGA 1700，当前价格2698；AMD Ryzen 9 7900X 最高睿频5.6GHz，12核24线程，TDP 170W，插槽类型Sokect AM5，当前价格2599。\n\n" \
                          "请勿直接回复读取的Json信息，参考以上模板总结选项，选项不超过5个，所选目标务必和需求中的价位接近，绝对不能超过预算，也不能低于预算超过20%。"\
                          "你无需回复额外的信息，只需要根据需求提供合适的$hardware选择即可。" \
                          "价格尽可能选择京东价格作为参照，如果没有京东价格，可能意味着该产品已经售罄，你不能推荐售罄的产品。"
        self.sys_prompt_template = string.Template(self.sys_prompt)
        self.template_dict = {"hardware": None}

        self.hw_translator = {
            "询问CPU": ["cpu"],
            "询问主板": ["motherboard"],
            "询问内存": ["memory"],
            "询问硬盘": ["ssd", "harddisk"],
            "询问显卡": ["graphicscard"],
            "询问显示器": ["monitor"],
            "询问机箱": ["chassis"],
            "询问电源": ["power"],
        }

        self.callback = "您好，请问您需要什么类型的$hardware？"

    def __load_data(self, hardware: str):
        """
        :param hardware:
        :return: data_content: str
        """
        union_data = []

        for hw in self.hw_translator[hardware]:
            with open(f"spider/{hw}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                # Delete elements that jdprice is None
                # data = [item for item in data if item["jdprice"] != "暂无京东价格"]
                # Delete all keys of price
                for i in range(len(data)):
                    del data[i]['price']
                union_data.extend(data)

        data_content = json.dumps(union_data, ensure_ascii=False)
        data_content = "信息更新：" + data_content

        return data_content

    def train(self):
        pass

    def chat(self, message: str, hardware: str):
        """
        :param message: chat message
        :param hardware: specific hardware expert
        :return:
        """
        print("from GTP:", message)

        # Construct the system prompt
        self.template_dict["hardware"] = hardware
        sys_prompt = self.sys_prompt_template.safe_substitute(self.template_dict)

        try:
            # Load the data from the file
            data_content = self.__load_data(hardware)

            messages = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": data_content},
                {"role": "assistant", "content": self.callback},
                {"role": "user", "content": message}
            ]

            # responce = input("请输入硬件专家的指导：")
            response = self.client.chat.completions.create(
                model="glm-3-turbo",  # 填写需要调用的模型名称
                messages=messages,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return "对不起，我无法理解您的问题。"

    def start(self):
        pass
