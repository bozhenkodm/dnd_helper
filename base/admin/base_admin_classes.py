import io
import subprocess
from abc import abstractmethod

from django.contrib import admin
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from pytesseract import image_to_string


class TextFromImage(admin.ModelAdmin):

    @abstractmethod
    def _apply_parsed_data(self, text, obj):
        pass

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if (
            not form.cleaned_data.get('upload_from_clipboard')
            and 'from_image' not in form.files
        ):
            return
        # Обработка изображения из буфера обмена
        if form.cleaned_data.get('upload_from_clipboard'):
            try:
                # Получаем изображение из буфера обмена (Linux)
                bash_command = 'xclip -selection clipboard -t image/png -o'
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                if error:
                    raise Exception(f"Ошибка получения из буфера: {error.decode()}")

                img = Image.open(io.BytesIO(output))

                self._apply_parsed_data(image_to_string(img, lang='rus'), obj)

            except Exception as e:
                self.message_user(
                    request, f"Ошибка обработки изображения: {str(e)}", level='ERROR'
                )

        # Обработка загруженного через форму изображения
        elif 'from_image' in form.files:
            uploaded_file = form.cleaned_data['picture']
            try:
                # Для InMemoryUploadedFile
                if isinstance(uploaded_file, InMemoryUploadedFile):
                    image_data = uploaded_file.read()
                    img = Image.open(io.BytesIO(image_data))

                    self._apply_parsed_data(image_to_string(img, lang='rus'), obj)

            except Exception as e:
                self.message_user(
                    request, f"Ошибка распознавания текста: {str(e)}", level='ERROR'
                )
        super().save_model(request, obj, form, change)
