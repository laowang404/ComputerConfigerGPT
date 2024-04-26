from zhipuai import ZhipuAI
import json


client = ZhipuAI(api_key="5e7362150b39d6a2432e6781f926b3bc.oPMWsX4QvLXkX544")
messages = [
            {"role": "system", "content": "你是一名专业的CPU硬件专家，知晓CPU的各种细节，能够根据客户的需求，提供合适的CPU选择。"
                                          "你会定期收到以\"信息更新：\"开头的信息，该信息会告诉你当前市场上主流的CPU信息，包括性能、价格等。"
                                          "你需要牢记这些信息。"
                                          "有一个装机专家会按照需求向你询问CPU的信息，你需要根据学到的内容，向他提供一个或多个合适的CPU选择。"
                                          "对于每个选择，你只需要将CPU的详细信息和价格告诉他即可，不同的CPU选择之间用易于理解的方式分隔。"
                                          "例如：\"英特尔酷睿i7 14700 KF 最高睿频5.6GHz，20核28线程，TDP 125W，插槽类型LGA 1700，当前价格2698；AMD Ryzen 9 7900X 最高睿频5.6GHz，12核24线程，TDP 170W，插槽类型Sokect AM5，当前价格2599。\""
                                          "价格尽可能选择京东价格作为参照，如果没有京东价格，可能意味着该产品已经售罄，你不能推荐售罄的产品。"
                                          "你无需回复额外的信息，只需要根据需求提供合适的CPU选择即可。"},
            # {"role": "user", "content": "客户：请你配置一台CPU性能更强的5000元内的主机"}
        ]

# Load the data from the file
with open("spider/cpu.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    # Delete elements that jdprice is None
    data = [item for item in data if item["jdprice"]!="暂无京东价格"]
    print(data)
    # Transfer to text
    data_content = json.dumps(data, ensure_ascii=False)
    data_content = "信息更新：" + data_content
    messages.append({"role": "user", "content": data_content})
    input("请按回车键继续")

messages.append({"role": "assistant", "content": "您好，请问您需要什么类型的CPU？"})

while True:
    response = client.chat.completions.create(
        model="glm-3-turbo",  # 填写需要调用的模型名称
        messages=messages,
    )
    print(response.choices[0].message)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    input_message = input("请输入硬件专家的指导：")
    messages.append({"role": "user", "content": input_message})