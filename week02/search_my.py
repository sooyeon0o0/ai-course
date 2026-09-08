import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "버그 수정 요청은 이슈 트래커에 등록해야 한다",
    "개발 서버 접속은 VPN 연결 후 이용 가능하다",
    "코드 리뷰 승인을 받아야 메인 브랜치에 합칠 수 있다",
    "데이터베이스 백업은 매일 새벽 3시에 수행된다",
    "외부 라이브러리 추가 시 보안 검토 과정을 거쳐야 한다",
    "API 문서 업데이트는 기능 개발과 동시에 진행한다",
    "신규 프로젝트 환경 구축은 도커를 활용한다",
    "비밀번호와 API 키는 코드에 직접 적지 않고 환경 변수로 관리한다",
    "테스트 코드가 통과하지 않으면 배포할 수 없다",
    "서버 장애 발생 시 즉시 온콜 담당자에게 연락한다",
]
D = np.stack([emb(d) for d in docs])          # 문서 10개를 미리 벡터로 (10 x 1024)

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))   # 문서 10개와의 코사인을 한 번에
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")

for question in ["프로그램 오류 제보 어디에 제출해?", "보안 토큰이나 인증 정보 숨겨서 저장하려면 어떻게 해?", "작성한 기능에 문제가 없는지 검증하는 검사가 실패하면 서비스 출시 못 해?"]:
    print("Q:", question)
    search(question)