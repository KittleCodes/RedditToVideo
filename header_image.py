'''
Create a header image.
'''
import textwrap
from PIL import Image, ImageDraw, ImageFont

def create_rounded_rectangle_mask(size, radius, alpha=255):
    '''
    Create a rounded rectangle mask.
    '''
    factor = 5
    radius = radius * factor
    image = Image.new('RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(255, 255, 255, alpha + 55))

    mx, my = (size[0] * factor, size[1] * factor)

    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(255, 255, 255, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(255, 255, 255, alpha))
    image = image.resize(size, Image.ANTIALIAS)

    return image

def header_image(question, upvotes, comments, username):
    '''
    Create a header image for the video using the given question, upvotes, and comments.
    '''
    image = create_rounded_rectangle_mask((800,200),20)

    logo = Image.open('icon.png', 'r')

    draw = ImageDraw.Draw(image)
    txt = question
    fontsize = 1

    img_fraction = .4

    font2 = ImageFont.truetype("ARLRDBD.TTF", fontsize)
    while font2.getsize(username)[0] < img_fraction*image.size[0]:
        fontsize += 1
        font2 = ImageFont.truetype("ARLRDBD.TTF", fontsize)

    font = ImageFont.truetype("ARLRDBD.TTF", 30)
    fontsize -= 1
    font2 = ImageFont.truetype("ARLRDBD.TTF", fontsize)

    margin, offset = (30, 75)
    for line in textwrap.wrap(txt, width=50):
        draw.text((margin, offset), line, font=font, fill="#000000")
        offset += font.getsize(line)[1]
    draw.text((90, 15), username, font=font2, fill=(0,0,0))

    draw.text((30, 165),
              f"Upvotes: {upvotes}        Comments: {comments}",
              font=ImageFont.truetype("ARLRDBD.TTF", 22),
              fill=(0,0,0))

    logo = logo.resize((50,50),Image.Resampling.LANCZOS)
    image.paste(logo, (30,10))
    image.save("header.png")
