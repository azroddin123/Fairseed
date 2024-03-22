from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
import os
from django.apps import apps
import logging


class Command(BaseCommand):
    help = 'Deletes images not associated with any model record from the media folder'

    def handle(self, *args, **options):
        self.stdout.write('Starting image cleanup process...')
        media_root = settings.MEDIA_ROOT
        self.delete_orphaned_images(media_root)
        self.stdout.write(self.style.SUCCESS('Image cleanup process complete.'))

    def delete_orphaned_images(self, directory):
        # Get all image files in the media directory
        image_files = self.get_image_files(directory)

        # Instead of iterating through all models, build a lookup of all field paths
        field_paths = self.get_field_paths()

        # Check if each image file is associated with any field
        for file_path in image_files:
            if file_path not in field_paths:
                # Log details about the deleted image (optional)
                logging.warning(f"Deleting potentially orphaned image: {file_path}")
                # Consider adding a mechanism to confirm deletion before proceeding
                # os.remove(file_path)
                # self.stdout.write(self.style.SUCCESS(f'Deleted orphaned image: {file_path}'))

    def get_image_files(self, directory):
        image_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if self.is_image(file):
                    image_files.append(os.path.join(root, file))
        return image_files

    def is_image(self, filename):
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        return filename.lower().endswith(image_extensions)

    def get_field_paths(self):
        field_paths = set()
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                for field in model._meta.get_fields():
                    if isinstance(field, models.ImageField):
                        field_name = field.name
                        # Check if any model instances reference this field
                        if model.objects.filter(**{field_name: field_name}).exists():
                            field_paths.add(field_name)
        return field_paths


# # Add logging configuration in your settings.py
# LOGGING = {
#     'version': 1,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'WARNING',  # Adjust log level as needed
#             'class': 'logging.FileHandler',
#             'filename': 'image_cleanup.log',
#         },
#     },
#     'loggers': {
#         'image_cleanup': {
#             'handlers': ['file'],
#             'level': 'WARNING',  # Adjust log level as needed
#             'propagate': True,
#         },
#     },
# }
