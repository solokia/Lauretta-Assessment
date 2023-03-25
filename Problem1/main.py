import os
import cv2
import numpy as np

def extract_coords(image):
    #Mask for color
    red_mask = cv2.inRange(image, (200, 0, 0), (255, 20, 20))
    #contours with mask should return dots instead of counting pixels
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_mask = cv2.inRange(image, (0, 0, 200), (20, 20, 255))
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(blue_contours),len(red_contours)



def solve_puzzle(folder_path):
    puzzle_images = []
    coords = []
    for filename in os.listdir(folder_path):
        image = cv2.imread(os.path.join(folder_path, filename))
        puzzle_images.append(image)

    coords = [extract_coords(image) for image in puzzle_images]
    max_row = max(coords, key=lambda x: x[0])[0] 
    max_col = max(coords, key=lambda x: x[1])[1] 

    # sort using lexsort since coords are in (row,col)
    sorted_indices = np.lexsort((np.array(coords)[:, 0], np.array(coords)[:, 1]))
    sorted_images = [puzzle_images[i] for i in sorted_indices]
    
    row_images = []
    for i in range(max_row):
        #since images is sorted in a row*col manner we can slice and append to get into 2d array
        row_images.append(sorted_images[i*max_col:(i+1)*max_col])
    stacked_images = [np.concatenate(row_images[i], axis=1) for i in range(max_row)]
    stacked_images = np.array(stacked_images)

    # cv2.vconcat concat the images vertically, use if we do by col then use hconcat
    final_image = cv2.vconcat(stacked_images)

    return final_image

def find_folders(folder_path):
    folders = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            folders.append(os.path.join(root, dir))
    return folders

def run():
    image_folder = 'images'
    output_folder = 'output'
    puzzle_folders = find_folders(image_folder)

    for folder in puzzle_folders:
        print(f'solving {folder}')
        final_image = solve_puzzle(folder)
        output_folder = os.path.join(output_folder, os.path.basename(folder))
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, 'final_image.jpg')
        cv2.imwrite(output_path, final_image)

if __name__ == "__main__":
    run()