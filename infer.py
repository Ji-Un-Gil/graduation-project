import torch
import streamlit as st
from transformers import PreTrainedTokenizerFast
from transformers.models.bart import BartForConditionalGeneration
import requests
import json
import urllib
from PIL import Image
from googletrans import Translator
import generator.secrets as secrets

REST_API_KEY = secrets.KARLO_API_KEY
NEGATIVE_PROMPT = 'word'
translator = Translator()

def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'samples': 8
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response


@st.cache(allow_output_mutation=True)
def load_model():
    model = BartForConditionalGeneration.from_pretrained('./kobart_summary')
    tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v2')
    return model, tokenizer

model, tokenizer = load_model()

st.title("E-book Image Generation")
text = st.text_area("Input")

if text:
    text = text.replace('\n', '')
    with st.spinner('processing..'):
        input_ids = tokenizer.encode(text)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        output = model.generate(input_ids, eos_token_id=1, max_length=150, num_beams=5)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        output = translator.translate(output).text
        response = t2i(output, NEGATIVE_PROMPT)

        images_html = ""
        for images in response.get("images"):
            img_url = images.get("image")
            images_html += f'<img src="{img_url}" style="width:200px; margin:5px; float:left;">'
        
        st.write(images_html, unsafe_allow_html=True)
