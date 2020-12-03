import logging
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.conf import settings
# Create your views here.
from django.views.generic.base import View
from nodejs.bindings import node_run

from .forms import AddARForm
from .mixins import CustomLoginRequiredMixin
from .models import AR

logging.basicConfig(
    filename=os.path.join(settings.BASE_DIR, 'add.log'),
    filemode='w',
    level=logging.INFO
)


class AllArView(CustomLoginRequiredMixin, View):
    def get(self, request):
        ars = AR.objects.all()
        context = {
            'ars': ars,
        }
        return render(request, 'ar/projects-page.html', context)


class ArDetailView(View):
    def get(self, request, id):
        ar = AR.objects.get(id=id)

        context = {
            'ar': ar
        }
        return render(request, 'ar/detail.html', context)


class AddArView(CustomLoginRequiredMixin, View):
    allowed_image_exts = (
        '.png',
        '.jpg'
    )

    def get(self, request):
        form = AddARForm()
        context = {
            'form': form,
        }
        return render(request, 'ar/add.html', context)

    def post(self, request):
        form = AddARForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            img = data.get('img', None)
            vid = data.get('video', None)

            logging.info(img.name)
            logging.info(vid.name)

            if img is None or vid is None:
                return HttpResponse('Something went wrong. Image or video is None')

            img_queryset = AR.objects.filter(img__endswith=img.name)
            if img_queryset:
                return HttpResponse('Image with that name already exists. Try to rename your image')

            vid_queryset = AR.objects.filter(video__endswith=vid.name)
            if vid_queryset:
                return HttpResponse('Video with that name already exists. Try to rename your image')

            _, img_ext = os.path.splitext(img.name)
            if img_ext.lower() not in self.allowed_image_exts:
                return HttpResponse('Invalid image type. Should be ' + ' or '.join(self.allowed_image_exts))

            if img.size < 50_000:
                return HttpResponse('Too small image')

            _, vid_ext = os.path.splitext(vid.name)
            if vid_ext.lower() != '.mp4':
                return HttpResponse('Invalid video type. Should be .mp4')

            form.save()
            logging.info('Form has been saved')

            img_path = os.path.join('../media/images', img.name)
            script_path = os.path.join(settings.BASE_DIR, 'generator/app.js')

            stderr, stdout = node_run(
                script_path,
                '-i',
                img_path,
            )
            logging.info('Node has run')
            logging.info(stderr)
            logging.info(stdout)
            return redirect('all_ar')
        else:
            return HttpResponse('Your form is invalid')


class Custom50SomView(View):
    def get(self, request):
        return render(request, 'ar/som50.html')


class CustomMTLogoView(View):
    def get(self, request):
        return render(request, 'ar/mtlogo.html')


class CustomQRProjectView(View):
    def get(self, request):
        return render(request, 'ar/qrproj.html')