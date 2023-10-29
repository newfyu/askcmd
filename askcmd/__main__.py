import argparse
import yaml
import os
import openai


# 获得执行本脚本所在的目录
pwd = os.path.dirname(os.path.abspath(__file__))
user_home = os.path.expanduser("~")

gen_cmd_function = {
  "name": "generate_commamd",
  "description": f"当前所在的目录是{pwd}。你现在要根据用户的需求生成对应的命令行命令(liunx,bash,shell,powershell等)。如果用户的请求不是请求一个终端命令或是要求解释命令，则直接给出回答",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "array",
        "description": "根据用户的请求生成对应的命令行命令,仅输出命令,不要包含其他解释",
        "items":{"type":"string"}
      },
        "other-response": {
        "type": "array",
        "description": "用户要求解释某个命令，或请求不是关于命令行命令，则根据用户的请求回答",
        "items":{"type":"string"}
      },
    },
  }
}

def make_config():
    config_path = os.path.join(user_home, ".askcmd")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    config_file = os.path.join(config_path, "config.yaml")
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("key: \n")
            f.write("model: gpt-3.5-turbo\n")
            f.write("api_base: \n")
            f.write("proxy: \n")


def set_proxy():
    with open(os.path.join(user_home, ".askcmd", "config.yaml")) as f:
        opt = yaml.safe_load(f)
    proxy_address = opt.get("proxy", None)
    if proxy_address:
        os.environ["http_proxy"] = f"{proxy_address}"
        os.environ["https_proxy"] = f"{proxy_address}"

def del_proxy():
    if os.environ.get("http_proxy"):
        del os.environ["http_proxy"]
        del os.environ["https_proxy"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_str', nargs='?', default=None, help='输入要生成命令的请求')
    parser.add_argument('--key', help='设置openai的key')
    parser.add_argument('--model', help='设置模型, 默认为gpt-3.5-turbo')
    parser.add_argument('--api-base', help='设置反向代理地址, 设置为none可以删除反向代理')
    parser.add_argument('--proxy', help='设置代理地址, 设置为none可以删除代理')
    args = parser.parse_args()
    return args

def read_write_config(key=None, model=None, api_base=None, proxy=None):
    with open(os.path.join(user_home, ".askcmd", "config.yaml"), 'r+') as f:
        config = yaml.safe_load(f)
        if key:
            config['key'] = key
            print(f"Set key to {key}")
        else:
            key = config.get('key')
            if not key:
                key = input('请输入key: ')
                config['key'] = key
        if model:
            config['model'] = model
        if api_base:
            if api_base == "none":
                config['api_base'] = None
                print("Remove api_base")
            else:
                config['api_base'] = api_base
                print(f"Set api_base to {api_base}")
        if proxy:
            if proxy == "none":
                config['proxy'] = None
                print("Remove proxy")
            else:
                config['proxy'] = proxy
                print(f"Set proxy to {proxy}")
        f.seek(0)
        yaml.dump(config, f)
        f.truncate()
    return config

def get_cmd(input_str):
    messages=[
    {"role": "system", "content": "You are an assistant to help user generate or explain command line commands."},
    {"role": "user", "content": f"{input_str}"}
    ]
    set_proxy()
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        functions = [gen_cmd_function],
        function_call = {"name":"generate_commamd"}
        )
    del_proxy()
    cmd = completion.choices[0].message["function_call"]["arguments"]
    cmd = eval(cmd)
    try:
        cmd = " ".join(cmd["command"])
        print(cmd)
        execute = input('你想执行这个命令吗? (y/n): ')
        if execute.lower() in ['y', 'yes']:
            execute_command(cmd)
    except:
        cmd = "".join(cmd["other-response"])
        print(cmd)

def execute_command(cmd):
    os.system(cmd)

def main():
    args = parse_args()
    make_config()
    config = read_write_config(args.key, args.model, args.api_base, args.proxy)
    openai.api_key = config['key']
    if config['api_base']:
        openai.api_base = config['api_base']
    if config['key']:
        if not args.input_str:
            input_str = input('Ask any command: ')
        else:
            input_str = args.input_str
        if input_str == "exit" or input_str == "quit" or input_str == "q":
            exit()
        get_cmd(input_str)
        

if __name__ == '__main__':
    main()
