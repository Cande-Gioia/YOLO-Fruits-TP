import pandas as pd
from PIL import Image
import xml.etree.ElementTree as ET

def create_DF(files, images_dir):
    """
    Convierte una lista de PosixPaths en un dataframe
    """
    df = pd.DataFrame([])
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()

        image_dic = []

        for obj in root.findall('object'):
            label = obj.find('name').text       # pineapple
            image = file.stem + ".png"          # fruit0.png
            bndbox = obj.find('bndbox')         
            xmin = float(bndbox.find('xmin').text)      # 38
            ymin = float(bndbox.find('ymin').text)     # 18
            xmax = float(bndbox.find('xmax').text)     # 271)
            ymax = float(bndbox.find('ymax').text)      # 227)

            image_dic.append({
                "label" : label,
                "left" : xmin, 
                "top" : ymin, 
                "right" : xmax,
                "bottom" : ymax
            })
        
        aux_df = pd.DataFrame(image_dic)
        
        # try:
        image_file = next(images_dir.glob(f"**/{file.stem}*.png"))
        aux_df["height"] = root.find('size').find('height').text
        aux_df["width"] = root.find('size').find('width').text
        aux_df["image"] = image_file
        aux_df["image_name"] = root.find('filename').text
        #df = df.append(aux_df, ignore_index=True)
        pd.concat([df, aux_df])
        # except:
        #     print(file.stem)
    print(df)
    df["center_x"] = (df["right"] + df["left"])/2
    df["center_y"] = (df["bottom"] + df["top"])/2
    df["delta_x"] = df["right"] - df["left"]
    df["delta_y"] = df["bottom"] - df["top"]

    return df