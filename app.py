import streamlit as st
import json
from openai import OpenAI
from datetime import datetime
import time
import markdown  # để render Markdown

# ===============================
# 🔹 Cấu hình DeepSeek API
# ===============================
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ===============================
# 🔹 Load dữ liệu OCR
# ===============================
with open("ocr_text.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# ===============================
# 🔹 Cấu trúc chương - mục
# ===============================
chapter_structure = {
    "Chương 1: Khái luận về Triết học và Triết học Mác - Lênin": {
        "I. Triết học và vấn đề cơ bản của triết học": (10, 47),
        "II. Triết học Mác - Lênin và vai trò của triết học Mác - Lênin trong đời sống xã hội": (47, 115),
    },
    "Chương 2: Chủ nghĩa duy vật biện chứng": {
        "I. Vật chất và ý thức": (116, 181),
        "II. Phép biện chứng duy vật": (181, 256),
        "III. Lý luận nhận thức": (256, 282),
    },
    "Chương 3: Chủ nghĩa duy vật lịch sử": {
        "I. Học thuyết hình thái kinh tế - xã hội": (283, 328),
        "II. Giai cấp và dân tộc": (328, 383),
        "III. Nhà nước và cách mạng xã hội": (383, 418),
        "IV. Ý thức xã hội": (418, 446),
        "V. Triết học về con người": (446, 488),
    },
}

st.set_page_config(page_title="💬 Chatbot Triết học Mác - Lênin", layout="wide")

# ===============================
# 🔹 Session state
# ===============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "section_state" not in st.session_state:
    st.session_state.section_state = {}

if "chat_input_temp" not in st.session_state:
    st.session_state.chat_input_temp = ""

# ===============================
# 🔹 CSS
# ===============================
st.markdown("""
<style>
.chat-container {height:60vh; overflow-y:auto; padding:10px; border-radius:12px; background:#f0f2f6; box-shadow: inset 0 0 10px #00000011;}
.user-msg {background-color:#DCF8C6; padding:10px 14px; border-radius:12px; margin:8px 0; text-align:right; max-width:80%; float:right; clear:both;}
.bot-msg {background-color:#ffffff; padding:10px 14px; border-radius:12px; margin:8px 0; border:1px solid #ddd; max-width:80%; float:left; clear:both;}
.timestamp {font-size:0.7em; color:gray; margin-top:2px;}
.typing {color: gray; font-style: italic;}
.input-container {display:flex; align-items: flex-start; gap:5px;}
.text-area {flex:1;}

/* Cột trái: tiêu đề đẹp */
.left-header {
    font-size: 1.5em;
    font-weight: bold;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 0 10px #00000033;
    margin-bottom: 10px;
}

/* Hover effect cho checkbox labels */
div[role="checkbox"] > label:hover {
    background-color: #e0e8f5 !important;
    border-radius: 6px;
    padding: 2px 6px;
    transition: background-color 0.2s ease;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Layout
# ===============================
col_left, col_right = st.columns([1.4, 2.7])

# -----------------------
# Cột trái: chương cố định, expander mục
# -----------------------
with col_left:
    st.markdown('<div class="left-header">💬 Chatbot Triết học Mác - Lênin</div>', unsafe_allow_html=True)
    st.info("⚠️ Nội dung trả lời có thể không chính xác. Hãy kiểm tra kỹ **nội dung câu trả lời** và **nguồn tham khảo**.")
    selected_sections = []

    for ch, sections in chapter_structure.items():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            padding: 8px 12px;
            border-radius: 8px;
            font-weight: bold;
            color: white;
            box-shadow: 0 0 15px #00000055;
            margin-bottom: 3px;
        ">{ch}</div>
        """, unsafe_allow_html=True)

        with st.expander("Hiển thị các mục", expanded=False):
            for sec_name in sections:
                sec_selected = st.checkbox(
                    sec_name,
                    value=st.session_state.section_state.get(f"{ch}_{sec_name}", False),
                    key=f"{ch}_{sec_name}"
                )
                st.session_state.section_state[f"{ch}_{sec_name}"] = sec_selected
                if sec_selected:
                    selected_sections.append((ch, sec_name))

# -----------------------
# Cột phải: chat cố định
# -----------------------
chat_placeholder = col_right.container()
chat_area = chat_placeholder.empty()  # luôn tồn tại

# -----------------------
# Hàm render chat (Markdown -> HTML)
# -----------------------
def render_chat(extra_msg=None, typing=False):
    chat_html = '<div class="chat-container" id="chat-container">'
    for msg in st.session_state.chat_history:
        ts = msg.get("time", "")
        content_html = markdown.markdown(msg["content"], extensions=['extra'])
        if msg["role"] == "user":
            chat_html += f'<div class="user-msg">{content_html}<div class="timestamp">{ts}</div></div>'
        else:
            chat_html += f'<div class="bot-msg">{content_html}<div class="timestamp">{ts}</div></div>'
    if extra_msg and typing:
        extra_html = markdown.markdown(extra_msg, extensions=['extra'])
        chat_html += f'<div class="bot-msg typing">{extra_html}</div>'
    chat_html += '</div>'
    chat_area.markdown(chat_html, unsafe_allow_html=True)

# -----------------------
# 🔹 Gửi câu chào khi lần đầu truy cập
# -----------------------
if "welcome_sent" not in st.session_state:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "Chào bạn! Tôi là chatbot Triết học Mác - Lênin. Bạn có thể hỏi tôi bất cứ câu gì liên quan đến nội dung đã chọn.",
        "time": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.welcome_sent = True

# Render chat ban đầu
render_chat()

# -----------------------
# Hàm gửi câu hỏi + AI trả lời (giữ ngữ cảnh)
# -----------------------
def send_question():
    user_input = st.session_state.chat_input_temp.strip()
    if not user_input:
        return

    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({"role":"user","content":user_input,"time":now})
    st.session_state.chat_input_temp = ""  # reset input
    render_chat(extra_msg="AI đang suy nghĩ...", typing=True)

    # Lấy dữ liệu OCR trong vùng chọn
    blocks = []
    MAX_CHARS = 20000
    char_count = 0

    for ch, sec in selected_sections:
        start, end = chapter_structure[ch][sec]
        # Lọc các đoạn thuộc trang từ start -> end
        section_texts = [p for p in ocr_data if start <= p["page"] + 1 <= end]
        for p in section_texts:
            true_page = p["page"] + 1
            text_piece = f"[{ch} – {sec} – Trang {true_page}]\n{p['text']}\n"
            if char_count + len(text_piece) > MAX_CHARS:
                break
            blocks.append(text_piece)
            char_count += len(text_piece)

    combined_text = "\n\n".join(blocks)

    # Chuẩn bị messages để AI giữ ngữ cảnh
    messages = [
        {"role": "system", "content":
            "Bạn là trợ lý Triết học Mác - Lênin. Dựa chủ yếu trên 'Nội dung tham khảo' được cung cấp, "
            "trả lời câu hỏi người dùng. Bạn có thể **suy luận nhẹ, giải thích, khái quát** từ dữ liệu tham khảo, "
            "nhưng KHÔNG thêm thông tin ngoài dữ liệu OCR. "
            "Trình bày Markdown đẹp, dễ đọc: in đậm, in nghiêng, danh sách, xuống dòng hợp lý. "
            "Khi chắc chắn, trích nguồn: Chương – Mục và số trang. "
            "Nếu thông tin chỉ có thể suy luận từ dữ liệu, hãy giải thích rõ đó là kết luận dựa trên dữ liệu tham khảo. "
            "Trả lời ngắn gọn, rõ ràng, trực tiếp, không lan man."
         }
    ]

    # Thêm lịch sử chat vào messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        else:
            messages.append({"role": "assistant", "content": msg["content"]})

    # Thêm câu hỏi hiện tại kèm nội dung tham khảo
    messages.append({"role": "user", "content": f"Câu hỏi mới: {user_input}\nNội dung tham khảo:\n{combined_text}"})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.4,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Lỗi khi gọi DeepSeek API: {e}"

    # Typing effect từng ký tự
    displayed = ""
    for c in answer:
        displayed += c
        render_chat(extra_msg=displayed, typing=True)
        time.sleep(0.01)

    st.session_state.chat_history.append({"role":"assistant","content":answer,"time":datetime.now().strftime("%H:%M:%S")})
    render_chat()


# -----------------------
# Input + nút gửi
# -----------------------
with col_right:
    st.text_area(
        label="⚠️ Nội dung trả lời có thể không chính xác. Hãy kiểm tra kỹ **nội dung câu trả lời** và **nguồn tham khảo**.",
        key="chat_input_temp",
        height=80,
        placeholder="Nhập câu hỏi của bạn ở đây..."
    )
    st.button("Gửi ✈️", on_click=send_question)
