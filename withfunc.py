from dotenv import load_dotenv
load_dotenv()

import os
from autogen import AssistantAgent, UserProxyAgent,Agent

# LLM への接続設定を環境変数から読み込む。キャッシュは無効化して繰り返し実行時に同じ結果にならないようにする
llm_config = {
    "cache_seed": None,
    "config_list": [
        {
            "model": os.getenv("DEPLOYMENT_NAME"),
            "api_type": "azure",
            "api_key": os.getenv("API_KEY"),
            "base_url": os.getenv("API_ENDPOINT"),
            "api_version": os.getenv("API_VERSION"),
        }
    ]
}

# メッセージを自前でハンドリングするための関数を定義
def print_messages(recipient, messages, sender, config): 
    if "callback" in config and  config["callback"] is not None:
        callback = config["callback"]
        callback(sender, recipient, messages[-1])
    print("======================================")
    print(f"Messages sent to: {recipient.name} | num messages: {len(messages)}")
    print(messages[-1])
    print("======================================")
    print("\n")
    return False, None  # エージェントの通信フローが続行されることを保証するために必要

# LLM でタスク解決を行うためのアシスタントエージェントを定義
assistant = AssistantAgent("assistant", llm_config=llm_config)
assistant.register_reply(
    [Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

# ユーザーの代理となるエージェント (user_proxy) を定義
user_proxy = UserProxyAgent("user_proxy",
                            code_execution_config=False,
                            human_input_mode="NEVER",
                            is_termination_msg=lambda msg: msg.get("content") is not None
                            and "TERMINATE" in msg["content"]
                            )
user_proxy.register_reply(
    [Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

# user_proxy からチャットを開始する。ユーザーからの依頼となるメッセージもここで設定
user_proxy.initiate_chat(
    assistant,
    message="Microsoft の株価について、ポジティブに笑えるジョークを考えてください。一つジョークを考えおわったら TERMINATE と出力してください。",
    silent=True,  # silent=True にすると、autogen が出力するメッセージは表示されない
)
