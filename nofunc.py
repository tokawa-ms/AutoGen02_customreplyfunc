from dotenv import load_dotenv
load_dotenv()

import os
from autogen import AssistantAgent, UserProxyAgent

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

# LLM でタスク解決を行うためのアシスタントエージェントを定義
assistant = AssistantAgent("assistant", llm_config=llm_config)

# ユーザーの代理となるエージェント (user_proxy) を定義
user_proxy = UserProxyAgent("user_proxy",
                            code_execution_config=False,
                            human_input_mode="NEVER",
                            is_termination_msg=lambda msg: msg.get("content") is not None
                            and "TERMINATE" in msg["content"]
                            )

# user_proxy からチャットを開始する。ユーザーからの依頼となるメッセージもここで設定
user_proxy.initiate_chat(
    assistant,
    message="Microsoft の株価について、ポジティブに笑えるジョークを考えてください。一つジョークを考えおわったら TERMINATE と出力してください。",
)
