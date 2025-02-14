# from PIL import Image, ImageDraw, ImageFont
#
#
# def merge_images_with_numbers(image_paths, orientation='horizontal'):
#     images = [Image.open(img_path) for img_path in image_paths]
#     draw = ImageDraw.Draw(images[0])  # Birinchi rasmga chizish obyekti
#
#     font_size = 20  # Shriftsiz o'lchami
#     font = ImageFont.load_default()  # Standart shrift
#
#     if orientation == 'horizontal':
#         total_width = sum(image.width for image in images)
#         max_height = max(image.height for image in images)
#
#         # Yangi rasm yaratish
#         new_image = Image.new('RGB', (total_width, max_height))
#
#         x_offset = 0
#         for index, image in enumerate(images):
#             new_image.paste(image, (x_offset, 0))
#             # Raqamni qo'shish
#             draw = ImageDraw.Draw(new_image)
#             draw.text((x_offset + image.width - 30, 10), str(index + 1), font=font,
#                       fill="white")  # O'ng burchakka joylash
#             x_offset += image.width
#
#     else:  # 'vertical' uchun
#         total_height = sum(image.height for image in images)
#         max_width = max(image.width for image in images)
#
#         # Yangi rasm yaratish
#         new_image = Image.new('RGB', (max_width, total_height))
#
#         y_offset = 0
#         for index, image in enumerate(images):
#             new_image.paste(image, (0, y_offset))
#             # Raqamni qo'shish
#             draw = ImageDraw.Draw(new_image)
#             draw.text((max_width - 30, y_offset + 10), str(index + 1), font=font,
#                       fill="white")  # O'ng burchakka joylash
#             y_offset += image.height
#
#     return new_image
#
#
# # Rasm fayllarining ro'yxatini berish
# image_files = ['https://avatars.mds.yandex.net/i?id=1cf04a6f38f0be15415a0c35010d27a3c5e70e21-4318341-images-thumbs&n=13', 'https://avatars.mds.yandex.net/i?id=5f71be02635003fd03f3e62a9c92b57eda9210380bd88b72-12445046-images-thumbs&n=13']
# merged_image = merge_images_with_numbers(image_files, orientation='horizontal')  # yoki 'vertical'
#
# # Yangi rasmni saqlash
# merged_image.save('merged_image_with_numbers.jpg')


