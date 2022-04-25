from django import template
from ..forms import ReportForm

register = template.Library()

@register.inclusion_tag('report.html')
def report_form():
    form = ReportForm()
    return {'form': form}