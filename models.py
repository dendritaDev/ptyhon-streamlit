from dataclasses import dataclass, asdict
import streamlit as st

# 1) Ejemplo clase propia
@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price: float

    def to_dict(self): 
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)

# Ejemplo Singleton
class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @st.cache_resource
    @staticmethod
    def get(base_url: str):
        return ApiClient(base_url)
