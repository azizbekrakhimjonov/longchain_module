from langgraph.graph import StateGraph, END
from typing import TypedDict

# --- 1. State holatini belgilash
class AgentState(TypedDict):
    image_path: str
    description: str
    price: str
    poster: str

# --- 2. Sub-agent funksiyalar
def analyze_image(state: AgentState) -> AgentState:
    # Bu joyda image analysis qilinadi (CLIP / OpenAI Vision API orqali)
    state["description"] = "Qora rangli iPhone 12 Pro Max, yaxshi holatda"
    return state

def fetch_price(state: AgentState) -> AgentState:
    # Bu joyda OLX yoki boshqa marketplace'dan scraping qilish mumkin
    state["price"] = "500 USD"
    return state

def generate_poster(state: AgentState) -> AgentState:
    # Bu joyda image generation ishlatiladi (DALL·E, Stable Diffusion va h.k.)
    state["poster"] = f"Poster tayyorlandi: {state['description']} - {state['price']}"
    return state

# --- 3. Agent graph tuzish
graph = StateGraph(AgentState)

graph.add_node("analyze", analyze_image)
graph.add_node("price", fetch_price)
graph.add_node("poster", generate_poster)

graph.set_entry_point("analyze")
graph.add_edge("analyze", "price")
graph.add_edge("price", "poster")
graph.add_edge("poster", END)

app = graph.compile()

# --- 4. Ishga tushirish
result = app.invoke({"image_path": "iphone.jpg"})
print(result)
