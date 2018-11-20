from PIL import Image

img1 = Image.open("test_img1.jpg","r")
img2 = Image.open("test_img2.jpg","r")

size1 =img1.size
size2 =img2.size

print(size1)
print(size2)

#make one left to right
width = size1[0]+size2[0]
height = max(size1[1],size2[1])

print(width,height)
new_image = Image.new("RGB",(width,height))
new_image.paste(im=img1,box=(0,0))
new_image.paste(im=img2,box=(size1[0],0))

new_image.save("Image_stitched_vert.png","PNG")

#make one right to left
new_image = Image.new("RGB",(width,height))
new_image.paste(im=img2,box=(0,0))
new_image.paste(im=img1,box=(size1[0],0))

new_image.save("Image_stitched_vert_different.png","PNG")

#horizontal
height = size1[1]+size2[1]
width = max(size1[0],size2[0])

new_image = Image.new("RGB",(width,height))
new_image.paste(im=img1,box=(0,0))
new_image.paste(im=img2,box=(0,size1[1]))

new_image.save("Image_stitched_hor.png","PNG")

print(new_image.format)