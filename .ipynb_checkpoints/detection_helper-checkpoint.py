import pandas as pd
from PIL import Image

def create_DF(files,images_dir):
    """
    Convierte una lista de PosixPaths en un dataframe
    """
    df = pd.DataFrame([])
    for file in files:
        aux_df = pd.read_csv(file, names=["label","left","top","right","bottom"], sep=" ")
        try:
            image_file = next(images_dir.glob(f"**/{file.stem}*jpg"))
            img = Image.open(image_file)
            aux_df["height"],aux_df["width"]=img.size
            aux_df["image"] = image_file
            aux_df["image_name"] = image_file.stem
            df = df.append(aux_df, ignore_index=True)
        except:
            print(file.stem)
    df["center_x"] = (df["right"] +df["left"])/2
    df["center_y"] = (df["bottom"] +df["top"])/2
    df["delta_x"] = df["right"] - df["left"]
    df["delta_y"] = (df["bottom"] -df["top"])
    return df