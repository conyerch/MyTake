from PIL import Image, ImageDraw, ImageFont, ImageOps

def create_tshirt_design(image_path, shape='none', text='Company Name'):
    # Open the input image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size

    bar_height = 80  # Bar height (adjust as needed)
    bar = Image.new('RGBA', (width, bar_height), (255, 255, 255, 255))  # Semi-transparent white bar
    img.paste(bar, (0,700), bar)  # Place the bar 2/3 down the image

    # Create a blank canvas (white background)
    canvas = Image.new('RGBA', (width, height), (255, 255, 255, 255))

    # Resize image to fit within 2/3 of the total height, leaving space for text

    # Create mask and apply shape constraints if any
    if shape == 'circle':
        mask = Image.new('L', (width, height), 0)  # Create a black mask
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((30, 30, width-30, height-30), fill=255, outline=128)  # Full circle covering the image
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)  # Apply the mask to the image

        draw_outline = ImageDraw.Draw(img)
        draw_outline.ellipse((30, 30, width-30, height-30), outline=(128, 128, 128, 255), width=10)

    elif shape == 'square':
        mask = Image.new('L', (width, height), 0)  # Create a black mask
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rectangle((0, 0, width, height), fill=255)  # Full square (no corners cut)
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)

    # Paste the image on the canvas

    canvas.paste(img, (0, 0), img)

    font = ImageFont.load_default()

    text_position = (width // 2, 700)
    text_color = (0, 0, 0, 255)

    draw = ImageDraw.Draw(canvas)

    draw.text(text_position, text, font=(font), fill=text_color)
    
    # Load a font

    # Convert to RGB before saving (removes transparency)
    final_img = canvas.convert('RGB')

    # Save the result
    final_img.save('output.png')

# Example Usage
create_tshirt_design('NYCT2.png', shape='circle', text='ONEDIGITAL')
