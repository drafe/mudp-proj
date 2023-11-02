from PIL import Image, ImageDraw # Include ior library

def invert_colors(img_in):
    w, h = img_in.size
    img_out = Image.new('L',(w, h))
    for x in range(w):
        for y in range(h):
            original_pxl = img_in.getpixel((x, y)) # The value of the
            result_pxl = 255 - original_pxl
            img_out.putpixel((x, y), result_pxl)
    return img_out

def blend_image(img1, img2, alpha):
    w1, h1 = img1.size
    w2, h2 = img2.size
    dw = abs(w1 - w2)
    dh = abs(h1 - h2)
    img_big = img1 if (w1 > w2 and h1 > h2) else img2
    img_small = img2 if (w1 > w2 and h1 > h2) else img1
    w = w2 if (w1 > w2) else w1
    h = h2 if (h1 > h2) else h1
    img_cut = Image.new('L', (w2, h2))
    for x in range(w):
        for y in range(h):
            pxl = img_big.getpixel((x+dw/2, y+dh/2))
            img_cut.putpixel((x, y), pxl)
    img_out = Image.new('L', (w, h))
    for x in range(w):
        for y in range(h):
            pxl1 = img_cut.getpixel((x, y))
            pxl2 = img_small.getpixel((x, y))
            result_pxl = int((1 - alpha)*pxl1 + alpha*pxl2)
            img_out.putpixel((x, y), result_pxl)
    return img_out

def selet_frame(img, point1, point2):
    img_f = img
    draw = ImageDraw.Draw(img_f)
    start = point1
    w = point2[0] - point1[0]
    h = point2[1] - point1[1]
    draw.rectangle([start, (w,h)], outline = (255, 0, 0), width = 3)
    img_f.show()

def color_invert(img):
    r, g, b = img.split()
    r_new = invert_colors(r)
    g_new = invert_colors(g)
    b_new = invert_colors(b)
    img_out = Image.merge('RGB',[r_new, g_new, b_new])
    return img_out

def color_blend(img1, img2, alpha):
    r1, g1, b1 = img1.split()
    r2, g2, b2 = img2.split()
    r_new = blend_image(r1, r2, alpha)
    g_new = blend_image(g1, g2, alpha)
    b_new = blend_image(b1, b2, alpha)
    img_out = Image.merge('RGB',[r_new, g_new, b_new])
    return img_out

if __name__ == '_main_':

    with Image.open('cow.jpg') as img_cow: # Open file
        img_cow.load()                    # Open like PIL image

    with Image.open('cow.jpg') as img_monk: # Open file
        img_monk.load() 

    img_cow_inv = color_invert(img_cow)
    img_cow_inv.show()
    img_blend = color_blend(img_cow, img_monk, 0.5)
    img_blend.show()