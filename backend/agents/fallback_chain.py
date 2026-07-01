import logging
from langchain_ollama import ChatOllama

PRIMARY_MODEL = "fake-model"
FALLBACK_MODEL = "llama3.2:latest"


def get_llm_with_fallback(tools=None):
    primary = ChatOllama(model=PRIMARY_MODEL)
    fallback = ChatOllama(model=FALLBACK_MODEL)

    if tools:
        primary = primary.bind_tools(tools)
        fallback = fallback.bind_tools(tools)

    def invoke_with_fallback(messages):
        try:
            print("\nUsing PRIMARY model:", PRIMARY_MODEL)
            return primary.invoke(messages)

        except Exception as e:
            print("\nPrimary model failed!")
            print(e)
            logging.warning(f"Primary model failed: {e}")

            print("\nTrying FALLBACK model:", FALLBACK_MODEL)

            try:
                response = fallback.invoke(messages)
                print("Fallback model worked!")
                return response

            except Exception as e2:
                print("\nFallback model also failed!")
                print(e2)
                logging.error(f"Fallback model failed: {e2}")
                raise

    return invoke_with_fallback