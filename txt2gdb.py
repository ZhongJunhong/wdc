import pandas as pd
import os
from tqdm import tqdm
import json
import geopandas as gpd


# List all TXT files in dir
def iterTXT(txt_dir):
    def checkTXT(file_name):
        if file_name.rsplit('.')[1] == 'TXT':
            return txt_dir + '/' + file_name
        else:
            return None
    return list(filter(None, list(map(checkTXT, os.listdir(txt_dir)))))


# Create the dir if not exist
def saveDir(dir_path):
    if os.path.exists(dir_path):
        return dir_path
    else:
        os.makedirs(dir_path)
        return dir_path


# Select the quality control code(QCC) column name from given header_name
def selectQCC(header_name):
    qcc = []
    for i in header_name:
        if i.rsplit('_')[-1] == 'code':
            qcc.append(i)
        else:
            continue
    return qcc


# Read TXT to dataframe and select the high quality data
def txt2Dataframe(txt_file_path, header_name):
    df = pd.read_csv(txt_file_path, 
                     sep = '\s+', 
                     header = None, 
                     names = header_name)
    
    # Change the value whose quality control code is not equal to 0 to null
    qcc = selectQCC(header_name).copy()
    
    for i in qcc:
        index = 0
        for v in df.loc[0:len(df), i].values.tolist():
            if v != 0:
                df.at[index, i.strip('_code')] = ''
            else:
                pass
            index += 1

    # Drop columns represented quality code
    df.drop(qcc,
            axis = 1,
            inplace = True)

    return df


# Create a new dataframe to store the grouped by data
def groupbyStation(input_df, header_name0):
    # Remove the quality control code from header name
    header_name = header_name0.copy() # Never remove elements from origin list directly !!!
    for i in selectQCC(header_name):
        header_name.remove(i)
    
    # Create output dataframe
    groupby_result = pd.DataFrame(columns = ['station'])
    groupby_result.set_index(['station'], inplace = True)

    for i in input_df.iloc[0:len(input_df)].values.tolist():
        
        groupby_result.at[i[0], 'latitude'] = i[1] * 0.01
        groupby_result.at[i[0], 'longtitude'] = i[2] * 0.01
        ele = i[3]
        if ele > 100000:
            ele = ele - 100000
        else:
            pass
        groupby_result.at[i[0], 'elevation'] = ele * 0.1

        date = str(i[6])

        for v in header_name[7:]:
            groupby_result.at[i[0], str(v) + '_' + date] = i[header_name.index(v)]

    return groupby_result


# Trans dataframe to GeoDatabase
def table2GDB(df, epsg, gdb_path, feature_name):
    gdf = gpd.GeoDataFrame(df, 
                           geometry = gpd.points_from_xy(df.longtitude, df.latitude), 
                           crs = 'EPSG:' + str(epsg))
    
    gdf.to_file(gdb_path, 
                driver = 'OpenFileGDB', 
                layer = feature_name)

    return None


def main():
    # Read json to load header name
    with open("header.json", "r") as f:
        header_dict = json.load(f)
    
    for wf in tqdm(['SSD', 'TEM', 'GST', 'PRS', 'EVP', 'RHU', 'PRE', 'WIN']):
        for f in tqdm(iterTXT('datasets/' + wf)):
            weather_feature = wf
            input_txt_file = f
            header_name = header_dict[weather_feature]

            df0 = txt2Dataframe(input_txt_file, header_name)
            df1 = groupbyStation(df0, header_name)

            table2GDB(
                df1,
                4326,
                'gdb/' + wf + '.gdb',
                input_txt_file.rsplit('/')[-1].rsplit('.')[0])
            
    return None

if __name__ == '__main__':
    main()
    