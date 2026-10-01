from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

SOURCE = Path(__file__).resolve().parent
ARTICLE = SOURCE.parent
OUT = ARTICLE / 'media'
OUT.mkdir(parents=True, exist_ok=True)
MARK_SVG = SOURCE / 'inferock-mark.svg'
MARK_PNG = SOURCE / 'inferock-mark.png'
subprocess.run(['magick', '-background', 'none', str(MARK_SVG), '-resize', '240x240', str(MARK_PNG)], check=True)

NAVY = '#011636'
BLUE = '#0074ff'
PALE = '#e9f1ff'
PAPER = '#f6f9ff'
MID = '#4d9fff'
MUTED = '#526783'
LINE = '#dce8f7'
WHITE = '#ffffff'
FONT = '/usr/share/fonts/rsms-inter-fonts/Inter-Regular.ttf'
FONT_MED = '/usr/share/fonts/rsms-inter-fonts/Inter-Medium.ttf'
FONT_SEMI = '/usr/share/fonts/rsms-inter-fonts/Inter-SemiBold.ttf'
FONT_BOLD = '/usr/share/fonts/rsms-inter-fonts/InterDisplay-Bold.ttf'

def ft(size, weight='regular'):
    return ImageFont.truetype({'regular':FONT, 'medium':FONT_MED, 'semi':FONT_SEMI, 'bold':FONT_BOLD}[weight], size)

def base(w,h):
    im = Image.new('RGB',(w,h),WHITE)
    glow = Image.new('RGBA',(w,h),(0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((w-670,-380,w+370,650),fill=(77,159,255,33))
    gd.ellipse((-440,h-380,560,h+490),fill=(0,116,255,13))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    im = Image.alpha_composite(im.convert('RGBA'),glow)
    d=ImageDraw.Draw(im)
    for x in range(0,w,72):
        d.line((x,0,x,h),fill=(246,249,254,255),width=1)
    for y in range(0,h,72):
        d.line((0,y,w,y),fill=(246,249,254,255),width=1)
    return im

def brand(im,x=96,y=72, size=62):
    mark=Image.open(MARK_PNG).convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
    im.alpha_composite(mark,(x,y))
    d=ImageDraw.Draw(im)
    d.text((x+size+17,y+size/2), 'Inferock',font=ft(int(size*.57),'bold'),fill=NAVY,anchor='lm')

def top_rule(d,w):
    d.rounded_rectangle((0,0,w,9),radius=0,fill=BLUE)

def text_lines(d, xy, lines, font, fill, spacing):
    x,y=xy
    for line in lines:
        d.text((x,y),line,font=font,fill=fill)
        y+=spacing

def save(im,name):
    path=OUT/name
    im.convert('RGB').save(path, 'PNG', optimize=True)
    print(path)

# Header card: typography and the original mark carry the composition.
im=base(1600,900); d=ImageDraw.Draw(im); top_rule(d,1600); brand(im,105,78,68)
watermark=Image.open(MARK_PNG).convert('RGBA').resize((600,600),Image.Resampling.LANCZOS)
watermark.putalpha(watermark.getchannel('A').point(lambda v: int(v*.085)))
im.alpha_composite(watermark,(985,185)); d=ImageDraw.Draw(im)
d.text((110,231),'AN INFEROCK POINT OF VIEW',font=ft(24,'semi'),fill=BLUE)
text_lines(d,(104,310),['Why AI providers','shouldn’t grade','their own bills.'],ft(91,'bold'),NAVY,111)
d.line((111,735,1489,735),fill=(190,217,249,255),width=2)
d.rounded_rectangle((111,730,362,740),radius=5,fill=BLUE)
d.text((111,774),'Independent receipts for every measured call.',font=ft(29,'medium'),fill=MUTED)
save(im,'header-white.png')

# The original Markdown table, typeset as an editorial comparison image.
im=base(1600,1000); d=ImageDraw.Draw(im); top_rule(d,1600); brand(im,96,62,55)
d.text((100,178),'One task. Three attempts.',font=ft(69,'bold'),fill=NAVY)
d.text((103,268),'A successful final answer can hide the cost of getting there.',font=ft(28),fill=MUTED)
d.text((241,354),'WHAT THE APP RECEIVED',font=ft(20,'semi'),fill=BLUE)
d.text((812,354),'WHAT THE RECEIPT CHECKS',font=ft(20,'semi'),fill=BLUE)
rows=[
 ('01','JSON cut off mid-field',['Finish reason, stream completion,','usage, schema result, and charge']),
 ('02','Transport error',['Whether the attempt was processed','or charged']),
 ('03','Valid JSON',['Final usage and charge, plus','the total cost of the task'])]
for i,(num,received,checks) in enumerate(rows):
    yt=394+i*174; yb=yt+151
    d.rounded_rectangle((99,yt,1501,yb),radius=27,fill=(255,255,255,255),outline=(210,227,249,255),width=2)
    d.rounded_rectangle((99,yt,109,yb),radius=5,fill=BLUE if i==2 else MID)
    d.text((148,yt+75),num,font=ft(30,'bold'),fill=BLUE,anchor='lm')
    d.text((241,yt+75),received,font=ft(32,'semi'),fill=NAVY,anchor='lm')
    for j,line in enumerate(checks): d.text((812,yt+43+j*39),line,font=ft(27),fill=NAVY)
d.text((105,941),'The receipt covers the task, including attempts that never reached the user.',font=ft(22,'medium'),fill=MUTED)
save(im,'attempts-table-white.png')
