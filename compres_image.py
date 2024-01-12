import os 
import numpy as np
import subprocess
import shutil
import cv2
from skimage import img_as_float
from skimage import img_as_ubyte
from skimage.util import random_noise

def process_image(path_to_image,compressed_image_path,decompressed_image_path, q_parameter):
    path_to_coder = r'coders\bpgenc.exe'
    path_to_decoder = r'coders\bpgdec.exe'
    argsLine = ['-m 9 -b 8 -q '+ str(q_parameter) + " " + path_to_image + ' -o ' + str(compressed_image_path)]
    cmd = [path_to_coder, argsLine]
    subprocess.check_call(cmd)
    argsLine = ['-o '+ decompressed_image_path + " " + str(compressed_image_path)]        
    cmd = [path_to_decoder, argsLine]
    subprocess.check_call(cmd)

def image_noise(path_to_image, sigma_in):
    """
    sigma=0.004*sigma - convertion for random_noise func

    variance 100 = sigma 10 \n
    variance 196 = sigma 14 \n
    variance 64 = sigma 8 \n
    """
    sigma=0.004*sigma_in
    image_array = cv2.imread(path_to_image,0)
    image_array_noise = random_noise(img_as_float(image_array), mode='gaussian', seed=42,  var=sigma**2)
    image_array_noise = img_as_ubyte(image_array_noise)
    path_to_noised_images = os.path.join("noised_images", f"noised_s{sigma_in}_" + os.path.basename(path_to_image).replace('init_',''))
    cv2.imwrite(path_to_noised_images, image_array_noise,[cv2.IMWRITE_PNG_COMPRESSION, 0]) 
    return path_to_noised_images

def check_dir(q):
    if not os.path.isdir(f"compressed_images\{q}"):
                os.mkdir(f"compressed_images\{q}")
    if not os.path.isdir(f"decompressed_images\{q}"):
                os.mkdir(f"decompressed_images\{q}")

def cleanning():
    print("type Y if want to clean up comp/decomp folders (type smth else to skip):")
    if str(input()).lower() == "y":
        decompressed_folder = os.path.abspath('decompressed_images')
        compressed_folder = os.path.abspath('compressed_images')
        for q_folder in os.listdir(decompressed_folder):
            shutil.rmtree(os.path.join(decompressed_folder,q_folder))
            shutil.rmtree(os.path.join(compressed_folder,q_folder))

def dir_creation():
    if not os.path.isdir("compressed_images"):
        os.mkdir("compressed_images")
    if not os.path.isdir("decompressed_images"):
        os.mkdir("decompressed_images")
    if not os.path.isdir("noised_images"):
        os.mkdir("noised_images")
        
def main():
    sigma_in=10
    q_parameter_array = np.arange(33, 49, 1) #if you want create different dataset of compressed/decompressed images you should varry this parameter
    path_to_image = os.path.abspath('init_images')
    for q_parameter in q_parameter_array:
        for image in os.listdir(path_to_image):
            print(image,q_parameter)
            path_to_current_image = os.path.join(path_to_image,image)
            check_dir(q_parameter)
            path_to_noised_image = image_noise(path_to_current_image, sigma_in=sigma_in)
            """
            you can replace noised image with initial by replacing os.path.basename(path_to_noised_image).replace("noised_", "compressed_") -> image (same for decompression), for correct path building 
            after it process_image func should take path_to_current_image for inintal image compression
            """
            path_to_compressed_image=os.path.join(path_to_image.replace("init_", "compressed_"),str(q_parameter),os.path.basename(path_to_noised_image).replace("noised_", "compressed_").replace(".png", ".bpg"))
            path_to_decompressed_image=os.path.join(path_to_image.replace("init_", "decompressed_"),str(q_parameter),os.path.basename(path_to_noised_image).replace("noised_", "decompressed_"))
            process_image(path_to_noised_image,path_to_compressed_image,path_to_decompressed_image, q_parameter)


if __name__ == '__main__':
    dir_creation()
    cleanning()
    main()
    
