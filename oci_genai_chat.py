from oci.generative_ai_agent_runtime.generative_ai_agent_runtime_client import GenerativeAiAgentRuntimeClient
from oci.generative_ai_agent_runtime.models import ChatDetails, CreateSessionDetails, Message, MessageContent
from oci.config import from_file
import uuid
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from oci.retry import RetryStrategyBuilder

def main():
    print("Hello from oci-genai-agent-sdk!")

    # .env ファイルの読み込み
    load_dotenv()

    # 環境変数からエンドポイント情報を取得
    service_endpoint = os.getenv("OCI_SERVICE_ENDPOINT")
    agent_endpoint_id = os.getenv("OCI_AGENT_ENDPOINT_ID")

    if not service_endpoint or not agent_endpoint_id:
        raise EnvironmentError("Environment variables OCI_SERVICE_ENDPOINT and OCI_AGENT_ENDPOINT_ID must be set in the .env file.")

    # OCI 設定の読み込み
    config = from_file()

    # リトライ戦略の設定
    retry_strategy = RetryStrategyBuilder(
        max_attempts_check=True,
        max_attempts=5,
        total_elapsed_time_seconds_check=True,
        total_elapsed_time_seconds=300  # 最大5分間リトライ
    ).get_retry_strategy()

    agents_client = GenerativeAiAgentRuntimeClient(
        config=config,
        service_endpoint=service_endpoint,
        retry_strategy=retry_strategy
    )

    # ユーザーIDの生成
    user_id = os.getenv("USER_ID")  # 環境変数から取得、なければUUIDを生成
    if not user_id:
        user_id = f"user-{uuid.uuid4()}"

    # 初期メッセージに基づいたユーザー設定
    initial_prompt = (
        "You are an expert on 'The Startup CTO's Handbook'. "
        "Answer questions and provide insights on topics such as leadership, technical team management, hiring practices, "
        "startup challenges, technical decision-making, and effective communication as described in the book. "
        "Cite relevant sections or principles from the handbook where applicable."
    )
    user_preferences = {
        "detail_level": "high",  # 応答の詳細度
        "tone": "formal",       # 応答のトーン
        "max_tokens": 100  # 応答のトークン数制限を応答速度に応じて設定
    }

    # セッションの作成
    session_id = agents_client.create_session(
        create_session_details=CreateSessionDetails(
            display_name=str(uuid.uuid4()),
            description=json.dumps({
                "language_code": "en-US",
                "metadata": {
                    "session_type": "interactive",
                    "user_id": user_id,
                    "user_preferences": user_preferences,
                    "session_goal": "Provide insights and detailed answers based on 'The Startup CTO's Handbook'",
                    "topics": [
                        "Leadership",
                        "Technical Team Management",
                        "Hiring",
                        "Startup Challenges",
                        "Technical Decision-Making",
                        "Effective Communication"
                    ]
                }
            })
        ),
        agent_endpoint_id=agent_endpoint_id
    ).data.id

    print(f"Session created with ID: {session_id}")

    # 初期メッセージの送信
    initial_message = Message(
        role="AGENT",
        content=MessageContent(
            text=initial_prompt
        )
    )
    response = agents_client.chat(
        agent_endpoint_id=agent_endpoint_id,
        chat_details=ChatDetails(
            user_message=initial_message.content.text,
            session_id=session_id,
            should_stream=False
        )
    )

    print("Assistant:", response.data.message.content.text)

    while True:
        # ユーザー入力を取得
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        # メッセージの送信
        response = agents_client.chat(
            agent_endpoint_id=agent_endpoint_id,
            chat_details=ChatDetails(
                user_message=user_input,  # ユーザーからのメッセージ
                session_id=session_id,  # セッション ID を指定
                should_stream=False,  # ストリーミングを有効にするか (False がデフォルト)
                max_tokens=user_preferences["max_tokens"]  # トークン数制限を適用
            )
        )

        # 応答の表示
        print("Assistant:", response.data.message.content.text)

if __name__ == "__main__":
    main()
