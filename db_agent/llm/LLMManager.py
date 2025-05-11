from typing import Union
from langchain_openai import OpenAI, ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import db_agent.config as local_config


class LLMManager:
    """Manage the LLM model and its configuration"""
    
    @staticmethod
    def get_llm(provider,model: str) -> Union[OpenAI, ChatOpenAI, ChatOllama, ChatGroq,ChatGoogleGenerativeAI]:
        """
        Returns an LLM instance based on the provider and model specified.
        """

        provider = provider.lower()

        if provider == "openai":
            if model.startswith("gpt-4") or model.startswith("gpt-3.5"):
                return ChatOpenAI(
                    model=model,
                    api_key=local_config.get_api_key(),
                    temperature=0.7,
                )
            else:
                return OpenAI(
                    model=model,
                    api_key=local_config.get_api_key(),
                    temperature=0.7,
                )
        
        elif provider == "ollama":
            return ChatOllama(
                model=model
            )
        
        elif provider == "groq":
            return ChatGroq(
                model=model,
                api_key=local_config.get_api_key(),
                temperature=0.7,
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model,
                api_key=local_config.get_api_key()
            )
        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. "
                "Supported providers: 'openai', 'ollama', 'groq'"
            )

