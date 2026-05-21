import re
import random

# 定义规则库：模式(正则表达式) -> 响应模板列表
rules = {
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'I work as a (.*)': [
        "What do you love most about being a {0}?",
        "How did your work as a {0} make you feel?",
        "Do you like your work?"
    ],
    r'I study (.*)': [
        "Why do you study {0}?",
        "How did your study of {0} make you feel?",
        "What's the most interesting thing you've learned about {0}?"
    ],
    r'I like (.*)': [
        "Tell me more about {0}.",
        "That's great! What do you like most about {0}?",
        "Do you make some friends through your {0}?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

# 定义代词转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}

# 设置记忆模块
memory = {"name": None, "age": None, "job": None, "hobbies": None}

def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    phrase = phrase.strip('.?!')  # 去除末尾标点  
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)

# 自动提取用户姓名/年龄/工作/爱好
def extract_info(user_input):
    name_match = re.search(r'my name is (\w+)', user_input, re.IGNORECASE)
    age_match = re.search(r'i am (\d+) years old', user_input, re.IGNORECASE)
    job_match = re.search(r'i work as a (.*)', user_input, re.IGNORECASE)
    hobbies_match = re.search(r'i like (.*)', user_input, re.IGNORECASE)

    if name_match:
        memory['name'] = name_match.group(1)
    if age_match:
        memory['age'] = age_match.group(1)
    if job_match:
        memory['job'] = job_match.group(1)
    if hobbies_match:
        memory['hobbies'] = hobbies_match.group(1)

def respond(user_input):
    """
    根据规则库生成响应
    """
    # 首先尝试提取用户信息并更新记忆
    extract_info(user_input)
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # 捕获匹配到的部分
            captured_group = match.group(1) if match.groups() else ''
            # 进行代词转换
            swapped_group = swap_pronouns(captured_group)
            # 从模板中随机选择一个并格式化
            response = random.choice(responses).format(swapped_group)
            # 如果记忆中有用户的姓名，可以在响应中加入称呼
            if memory['name']:
                response = f"{memory['name']}, {response}"
            return response
    # 如果没有匹配任何特定规则，使用最后的通配符规则
    return random.choice(rules[r'.*'])

# 主聊天循环
if __name__ == '__main__':
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print(f"Therapist: Goodbye {memory['name'] if memory['name'] else 'there'}. It was nice talking to you.")
            break
        response = respond(user_input)
        print(f"Therapist: {response}")