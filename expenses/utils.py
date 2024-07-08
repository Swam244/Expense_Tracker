from xhtml2pdf import pisa
from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO

def html_to_pdf(template_source,context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),context_type="application/pdf")
    return None

