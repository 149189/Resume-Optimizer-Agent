import fitz  # PyMuPDF
import docx2txt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from prometheus_client import Counter, Histogram
from .models import EmbeddingDoc
import json
import os
import math

MATCH_REQUESTS = Counter('match_requests_total', 'Total number of match API requests')
MATCH_LATENCY = Histogram('match_request_latency_seconds', 'Latency for match API requests')

@api_view(['POST'])
def upload_resume(request):
    file_obj = request.FILES.get('file')
    if not file_obj:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    text = ""
    if file_obj.name.endswith('.pdf'):
        # Read PDF
        with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file_obj.name.endswith('.docx'):
        # Save temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            for chunk in file_obj.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
        text = docx2txt.process(tmp_path)
    else:
        return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"text": text})


@api_view(['POST'])
def match(request):
    MATCH_REQUESTS.inc()
    with MATCH_LATENCY.time():
        data = request.data or {}
    resume_text = (data.get('resume_text') or '').strip()
    job_text = (data.get('job_text') or '').strip()
    if not resume_text or not job_text:
        return Response({"error": "resume_text and job_text are required"}, status=status.HTTP_400_BAD_REQUEST)

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])

    # top keywords per document
    feature_names = vectorizer.get_feature_names_out()
    resume_vec = tfidf[0].toarray()[0]
    job_vec = tfidf[1].toarray()[0]
    top_resume_terms = [term for _, term in sorted(zip(resume_vec, feature_names), reverse=True)[:15] if _ > 0]
    top_job_terms = [term for _, term in sorted(zip(job_vec, feature_names), reverse=True)[:15] if _ > 0]

    return Response({
        "score": round(score, 4),
        "top_resume_terms": top_resume_terms,
        "top_job_terms": top_job_terms,
    })


@api_view(['GET'])
def health(request):
    return Response({"status": "ok"})


def _embed_with_openai(texts):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        # Use a small, inexpensive embedding model
        resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [d.embedding for d in resp.data]
    except Exception:
        return None


def _embed_with_hash(texts):
    hv = HashingVectorizer(n_features=1024, alternate_sign=False, norm='l2', stop_words='english')
    mat = hv.transform(texts)
    return [row.toarray()[0].tolist() for row in mat]


def _cosine(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


@api_view(['POST'])
def ingest(request):
    data = request.data or {}
    text = (data.get('text') or '').strip()
    title = (data.get('title') or '').strip()
    if not text:
        return Response({"error": "text is required"}, status=status.HTTP_400_BAD_REQUEST)
    vectors = _embed_with_openai([text]) or _embed_with_hash([text])
    vec = vectors[0]
    doc = EmbeddingDoc.objects.create(title=title, text=text, vector_json=json.dumps(vec))
    return Response({"id": doc.id})


@api_view(['POST'])
def search_match(request):
    data = request.data or {}
    query = (data.get('query') or '').strip()
    top_k = int(data.get('top_k') or 5)
    if not query:
        return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
    q_vec = (_embed_with_openai([query]) or _embed_with_hash([query]))[0]
    results = []
    for doc in EmbeddingDoc.objects.order_by('-created_at')[:1000]:
        vec = json.loads(doc.vector_json)
        score = _cosine(q_vec, vec)
        results.append({"id": doc.id, "title": doc.title, "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    return Response({"results": results[:top_k]})
