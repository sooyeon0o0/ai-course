import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    amount = ""
    people = ""
    items = None

    if request.method == 'POST':
        try:
            # 영수증 이미지 처리
            image_file = request.files.get('receipt_image')
            
            if image_file and image_file.filename != '':
                image_bytes = image_file.read()
                prompt = "영수증의 각 항목과 금액을 추출해서 JSON 형식으로 응답해줘. JSON 형식은 [{'item': '항목명', 'price': 금액}, ...] 형태여야 해. 다른 말은 하지 말고 JSON만 답해줘."
                response_text = ask(prompt, image_bytes=image_bytes)
                items = parse_json(response_text)
                
                if items:
                    # 항목들을 기반으로 총액 계산
                    total_amount = sum(item['price'] for item in items)
                    # 인원수 가져오기
                    people_str = request.form.get('people', '1')
                    people = int(people_str)
                    if people <= 0:
                        error = "인원수는 1명 이상이어야 합니다."
                    else:
                        result = total_amount / people
                        amount = total_amount
                else:
                    error = "읽지 못했습니다"
            else:
                # 기존 숫자 입력 방식
                amount_str = request.form.get('amount', '')
                people_str = request.form.get('people', '')
                
                if amount_str:
                    amount = float(amount_str)
                if people_str:
                    people = int(people_str)

                if amount != "" and people != "":
                    if people <= 0:
                        error = "인원수는 1명 이상이어야 합니다."
                    else:
                        result = float(amount) / int(people)
                elif not image_file:
                     error = "금액을 입력하거나 영수증을 올려주세요."

        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, error=error, amount=amount, people=people, items=items)

if __name__ == '__main__':
    app.run(debug=True)

