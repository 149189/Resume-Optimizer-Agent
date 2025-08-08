import fitz  # PyMuPDF
import docx2txt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
