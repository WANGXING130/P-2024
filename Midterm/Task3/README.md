# Task 3

请补充个人信息后，在此完成报告！

接入LLM的web-api  
~~~python
import time
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="c5b203c6b5273632daba494387afdb75.MhywiWSvmqnf4DY4")  # 请填写您自己的APIKey

response = client.chat.asyncCompletions.create(
    model="glm-4-plus",  # 请填写您要调用的模型名称
    messages=[
        {
            "role": "user",
            "content":
                "玉皇大帝住在平流层还是对流层？"
}
],
)
task_id = response.id
task_status = ''
get_cnt = 0

while task_status != 'SUCCESS' and task_status != 'FAILED' and get_cnt <= 40:
    result_response = client.chat.asyncCompletions.retrieve_completion_result(id=task_id)
    print(result_response)
    task_status = result_response.task_status

    time.sleep(2)
    get_cnt += 1

~~~

本地模型  
下载LFS并放到Qwen2.5-1.5B-Instruct文件夹中后，修改model_name为名称、路径都报错（没安装pytorch等  安装完成后，说需要accelerate  
下载完成后再运行，发现成功运行但是空白......  
实在是不理解  

@Author:  
@Email:
