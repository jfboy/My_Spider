from PIL import Image
import os
import glob
import math

#连续获取文件夹的图片，并制成照片墙
def get_images(images,source_path,keyword,WALL_SIZE):
    imgs_path = source_path + '\\*.jpg'
    img_number= len(glob.glob(imgs_path)) #图片的总个数
    NEW_SIZE = get_oneimg_size(WALL_SIZE, img_number)#计算墙内每张图片的size
    row , column = get_row_column(WALL_SIZE,NEW_SIZE)#计算行列个数
    x_offset, y_offset = get_offset(WALL_SIZE, NEW_SIZE, row, column) #计算行列间隔值
    for img_path in glob.glob(imgs_path):
        img_resize(img_path,images,NEW_SIZE)#将图片改为统一尺寸
    put_on_wall(images,keyword, WALL_SIZE, NEW_SIZE, row , column, x_offset, y_offset)#将重新裁剪后的图片放入图片墙

#将图片改为统一尺寸
def img_resize(img_path,images,NEW_SIZE):
    img = Image.open(img_path)
    r_img = img.resize(NEW_SIZE, Image.NEAREST)
    images.append(r_img)

#计算墙内每张图片的size
def get_oneimg_size(WALL_SIZE,img_number):
    one_area = (WALL_SIZE[0] * WALL_SIZE[1]) // (img_number)
    a = int(math.sqrt(one_area))
    row_x, colum_x = get_row_column(WALL_SIZE, (a,a)) #为确保都能放下，重新规划
    one_area = (WALL_SIZE[0] * WALL_SIZE[1]) // ((row_x+1)*(colum_x+1))
    a = int(math.sqrt(one_area))  # 宽、高相等
    return (a,a)

#计算行、列数
def get_row_column(WALL_SIZE,NEW_SIZE):
    row = WALL_SIZE[1] // NEW_SIZE[1]
    column = WALL_SIZE[0] // NEW_SIZE[0]
    return row, column

#计算行列间隔值
def get_offset(WALL_SIZE,NEW_SIZE,row,column):
    y_offset = (WALL_SIZE[1] - row * NEW_SIZE[1]) // row
    x_offset = (WALL_SIZE[0] - column * NEW_SIZE[0]) // row
    return x_offset//2, y_offset//2   #为确保放的下

#将重新裁剪后的图片放入图片墙
def put_on_wall(images,keyword, WALL_SIZE, NEW_SIZE, row , column, x_offset, y_offset):
    photo_wall_img = Image.new('RGB',WALL_SIZE,'white')
    index = len(images)
    for i in range (row):
        for j in range(column):
            if index > 0:
                photo_wall_img.paste(images[len(images)-index],(j*NEW_SIZE[0]+(j+1)*x_offset, i*NEW_SIZE[1]+(i+1)*y_offset))
                index-=1
            else:
                break
    print("照片墙制作完成！\n共制作{}张图片".format(len(images)-index))
    save_img(photo_wall_img,keyword)

#将照片墙存入一个文件夹
def save_img(photo_wall_img,keyword):
    new_path_name = 'photowallimages'
    wall_img_path = os.getcwd() + os.path.sep + new_path_name #新建的文件夹的路径
    if not os.path.exists(wall_img_path):
        os.makedirs(wall_img_path)
    else:
        print("照片墙文件夹已存在！")
    photo_wall_img.save(new_path_name+ os.path.sep + keyword + '.jpg')


def main(keyword):
    images = []  # 存储要放入照片墙的、重新统一过尺寸的图片
    WALL_SIZE = (1920, 1080)  # 照片墙尺寸
    source_path = os.getcwd() + os.path.sep + keyword
    if os.path.exists(source_path):
        get_images(images, source_path, keyword, WALL_SIZE)  # 连续获取文件夹的图片，并制成照片墙
    else:
        print("未找到图片文件夹")


if __name__ == "__main__":
    keyword = '图片'
    main(keyword)

