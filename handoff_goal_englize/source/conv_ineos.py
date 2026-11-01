import sys
from PIL import Image, ImageOps, ImageDraw
import pillow_heif; pillow_heif.register_heif_opener()
src,dst=sys.argv[1],sys.argv[2]
ims=[]
for n in range(1,10):
    import glob
    p=glob.glob(f'{src}/Slide{n}.*')[0]
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    print(n,im.size)
    im.thumbnail((1400,1400)); im.save(f'{dst}/{n}.jpg',quality=85)
    t=im.copy(); t.thumbnail((500,500)); ims.append(t)
W=500;H=500
sheet=Image.new('RGB',(W*3,H*3),'#222')
for i,t in enumerate(ims):
    x=(i%3)*W+(W-t.width)//2; y=(i//3)*H+(H-t.height)//2
    sheet.paste(t,(x,y)); ImageDraw.Draw(sheet).text(((i%3)*W+8,(i//3)*H+8),str(i+1),fill='yellow')
sheet.save(f'{dst}/sheet.png')
