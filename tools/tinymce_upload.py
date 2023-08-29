import os
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        try:
            permit_file_suffix = settings.TINYMCE_DEFAULT_CONFIG.get("images_file_types").split(",")
        except:
            permit_file_suffix = "jpeg,jpg,jpe,jfi,jif,jfif,png,gif,bmp,webp".split(",")
        if file_name_suffix not in permit_file_suffix:
            return JsonResponse({"message": "错误的文件格式"})

        upload_time = timezone.now()
        _file = os.path.join(
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day),
            file_obj.name
        )
        file = default_storage.save(_file, file_obj)
        file_url = default_storage.url(file)

        return JsonResponse({
            'message': '上传图片成功',
            'location': file_url
        })
    return JsonResponse({'detail': "错误的请求"})
