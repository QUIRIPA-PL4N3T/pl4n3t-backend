from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from companies.models import Member
from django.conf import settings


def accept_invitation(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.status = Member.ACTIVE
    member.save()
    return HttpResponseRedirect(settings.PL4N3T_APPLICATION)
