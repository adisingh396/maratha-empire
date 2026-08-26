from PIL import Image, ImageDraw
import os
base=os.path.join(os.path.dirname(__file__), "../gfx/flags")
base=os.path.abspath(base)
for size,name in [((82,52),'MAR.tga'),((82,52),'MAR_democratic.tga'),((82,52),'MAR_neutrality.tga'),((82,52),'MAR_fascism.tga'),((82,52),'MAR_communism.tga')]:
    w,h=size
    img=Image.new('RGB',(w,h),(255,102,0))
    d=ImageDraw.Draw(img)
    d.rectangle([0,0,w-1,h-1], outline=(120,40,0))
    if 'fascism' in name:
        d.ellipse([w*0.35,h*0.2,w*0.65,h*0.8], fill=(180,40,0), outline=(255,215,0))
    img.save(os.path.join(base, name))
    Image.new('RGB',(10,7),(255,102,0)).save(os.path.join(base, "small", "10x7_dummy"))
print("done")
