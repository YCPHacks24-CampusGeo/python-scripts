input_folder = "C:/Users/16673/Downloads/profile_input"
output_folder = "C:/Users/16673/Downloads/profile_output"
overlay_image_path = "map-icon-small.png"
output_list = "public static List<string> Markers = ["

import os
from PIL import Image, ImageDraw



def resize_images(size=(128, 128)):
    global output_list

    if not os.path.exists(output_folder + "/icons"):
        os.makedirs(output_folder + "/icons")

    if not os.path.exists(output_folder + "/markers"):
        os.makedirs(output_folder + "/markers")

    overlay_image = Image.open(overlay_image_path)
    overlay_width, overlay_height = overlay_image.size

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            img = img.resize(size, Image.ANTIALIAS)
            output_path = os.path.join(output_folder + "/icons", filename)
            img.save(output_path)

            # Create a mask for the circular crop with extra 10 pixels on each side
            mask_size = (size[0] - 20, size[1] - 20)
            mask = Image.new('L', mask_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + mask_size, fill=255)

            # Apply the mask to create a circular image
            circular_img = Image.new('RGBA', mask_size)
            circular_img.paste(img.crop((10, 10, size[0] - 10, size[1] - 10)), (0, 0), mask)

            # Create a new image with the same width but taller height
            combined_img = Image.new('RGBA', (size[0], overlay_height))

            # Calculate the horizontal position to center the circular image
            horizontal_center = (size[0] - mask_size[0]) // 2

            # Paste the circular image at the top, centered horizontally
            combined_img.paste(circular_img, (horizontal_center, 10), circular_img)

            # Paste the overlay image below the circular image
            combined_img.paste(overlay_image, mask=overlay_image)

            combined_img.thumbnail((65, 999999), Image.ANTIALIAS)

            output_path = os.path.join(output_folder + "/markers", filename.replace(".jpg", ".png"))
            combined_img.save(output_path, format="PNG")

            output_list += f"""\n    \"{filename.replace('.jpg', '')}\","""



resize_images()
output_list += "\n];"
print(output_list)