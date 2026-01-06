"""
Python script (should work with versions 3.11+) to compute the Normalized Hotspot Indices
(HNI), using only Landsat 8 & 9 data, developed by Marchese et al. (2019) and Genzano et
al. (2020). The last authors also developed a freely available web app, named the NHI tool
accesible through the following link: https://nicogenzano.users.earthengine.app/view/nhi-tool
This tool computes the NHI indices for Landsat and Sentinel-2 data for any volcano listed in the
Smithsonian Instituions's Global Volcanism Program (GVP), and also leverages the Google Earth
Engine (GEE) data archive and JavaScript resources freely available.

This current script, instead, computes the NHI for Landsat 8 & 9 data only. A future release
will include the Sentinel-2 data processing as well.
Unlike the NHI tool, this script is able to compute the NHI indices for any point on Earth,
and the outputs are:
1) A CSV file containing the following results:
    1.1) "Date" of each Landsat image available within the given time frame
    1.2) "Total HNI SWIR hot pixels"
    1.3) "Total HNI SWNIR hot pixels"
    1.4) "Total HNI SWIR + SWNIR hot pixels"
    1.5) "Hot pixels area m2"
    1.6) "Total NHI extreme pixels"
    1.7) "Extreme hot pixels area m2"
    1.8) "Radiance B6 (1.6 μm)"
    1.9) "Radiance B7 (2.2 μm)"

2) Individual images of the Landsat 8 & 9 raster data in GeoTiff format, in which NHI hot
   pixels were found
   
3) Vector shapefile (ESRI format) data of those Landsat 8 & 9 raster images mentioned in item 2)

4) Plots in interactive HTML format of some variables listed in item 1)

Thus, the user must have a Gmail or an institutional workspace account. To avoid charges,
you must select the Non-commercial or Research/Academic track during registration. Details
on how to properly register your account can be found here:
https://code.earthengine.google.com/register?authuser=2

Assuming that you have setup your GEE account properly and your prompt in the terminal window
is located within the folder containg this script, you can run this script through the linux
(or conda) terminal window by executing the following command line:
python nhi_oli_8_9_sp_v01.py input_file.txt

But, if you are under a Windows OS, execute instead:
python.exe nhi_oli_8_9_sp_v01.py input_file.txt

More details are found in my GitHub page

This scripts's author details:
Name: José Armando Saballos
E-mail: j.a.saballos@gmail.com
GitHub: https://github.com/saballos
ResearchGate: https://www.researchgate.net/profile/Jose-Saballos-2

Main papers this script is based on:
Marchese, F., Genzano, N., Neri, M., Falconieri, A., Mazzeo, G., & Pergola, N. (2019).
A multi-channel algorithm for mapping volcanic thermal anomalies by means of Sentinel-2 MSI
and Landsat-8 OLI data. Remote Sensing, 11(23), 2876.

Genzano, N., Pergola, N., & Marchese, F. (2020).
A Google Earth Engine tool to investigate, map and monitor volcanic thermal anomalies at global
scale by means of mid-high spatial resolution satellite data. Remote Sensing, 12(19), 3232.

Genzano, N., Saballos, J. A., Gutierrez, W., & Marchese, F. (2024).
Volcán de Fuego (Guatemala) monitoring with the Normalized Hotspot Indices (NHI) tool.
ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 10, 147-154.

"""
#================================================================================#

#==================================================================#
#                         DATOS DE ENTRADA                         #
#==================================================================#


#===================================================================#
import argparse
import sys
parser = argparse.ArgumentParser(
    description="NHI index computation with Landsat 8 & 9 images"
)
parser.add_argument(
    "input_file",
    type=str,
    help="Text file containing the input parameters for the script: nhi_oli_8_9_sp_v01.py)"
)
args = parser.parse_args()

# Lectura y parsing del archivo de parámetros
params = {}
try:
    with open(args.input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            # Debe haber un =
            if "=" not in line:
                print(f"Error en línea {line_num} del archivo {args.input_file}: is missing '='")
                sys.exit(1)
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            # Quitar comillas simples o dobles si las hay (útil para nombres con espacios)
            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            params[key.lower()] = value   # guardamos en minúsculas para ser más flexibles
except FileNotFoundError:
    print(f"Input file not found: {args.input_file}")
    sys.exit(1)
except Exception as e:
    print(f"Error in reading the content of the input file: {e}")
    sys.exit(1)

#==============================================================================#
#             Asignación de variables obligatorias con validación              #
#==============================================================================#
required_keys = ["volcan", "lon", "lat", "radio", "start", "end", "gmail_name"]

for key in required_keys:
    if key not in {k.lower() for k in params.keys()}:
        print(f"Input file is missing one of the input parameters: {key}")
        sys.exit(1)

# Asignación final (las claves las buscamos en minúsculas para ser tolerantes)
volcan      = params.get("volcan", "").strip()
lon         = float(params.get("lon", 0))
lat         = float(params.get("lat", 0))
radio       = float(params.get("radio", 0))
start       = params.get("start", "").strip()
end         = params.get("end", "").strip()
gmail_name  = params.get("gmail_name", "").strip()

# Validación básica de los valores numéricos y fechas
if not (-180 <= lon <= 180 and -90 <= lat <= 90):
    print("Coordinates lon/lat are out of a valid range")
    sys.exit(1)
if radio <= 0:
    print("The serach radius must be in km and greater than 0")
    sys.exit(1)
if not start or not end:
    print("You must provide the 'start' and 'end' dates\n")
    sys.exit(1)

#
print("\nInput data successfully read!")

#==================================================================#
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
#==================================================================#
#           NO CAMBIAR NADA MÁS, EL SCRIPT HARÁ EL RESTO           #
#==================================================================#
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
#==================================================================#
import ee # conda install -c conda-forge earthengine-api
ee.Authenticate()
print("Trying to authenticate the gmail account in GEE platform...\n")
#ee.Initialize()
ee_proj = 'ee-' + gmail_name
ee.Initialize(project=ee_proj)
import geemap # conda install -c conda-forge geemap
import folium
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
from pathlib import Path
from datetime import date


print(f"Account '{ee_proj}' successfully authenticated to the GEE platform\n")
print("Working on site:", volcan)

#===================================================================#
def filter_empty_images(collection, region, scale=30):
    def check_for_data(image):
        # Binarizar las imágenes de la colección
        # 1 for non-zero pixels, 0 for zero pixels
        mask = image.neq(0)
        any_band_has_data_mask = mask.reduce(ee.Reducer.max())
        stats = any_band_has_data_mask.reduceRegion(
            reducer=ee.Reducer.max(),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        )

        # Get the max value (which will be 1 if data exists, 0 if not)
        has_data = ee.Number(stats.get('max'))
        return image.set('has_data', has_data)

    collection_with_stats = collection.map(check_for_data)

    # Remover las imágenes con valor = 0
    filtered_collection = collection_with_stats.filter(
        ee.Filter.eq('has_data', 1)
    )

    return filtered_collection

#===============================================================================#

#==================================================================#
#          ACCEDER a las COLECCIONES Landsat 8 y 9 de GEE          #
#==================================================================#

punto = ee.Geometry.Point(lon, lat)
roi = ee.Geometry.Point([lon, lat]).buffer(radio*1e3)
#
# USGS Landsat 8 Collection 2 Tier 1 Raw Scenes
# Dataset Availability from 2013-03-18T15:58:14Z
L8raw = ee.ImageCollection('LANDSAT/LC08/C02/T1').filterDate(start,end).\
        filterDate(ee.Date(start),ee.Date(end).advance(1, 'day')).\
        filterMetadata('SUN_ELEVATION','greater_than', 0).\
        select(['B1','B5','B6','B7']).filter(ee.Filter.bounds(punto))
#
# USGS Landsat 9 Collection 2 Tier 1 Raw Scenes
# Dataset Availability from 2021-10-31T00:00:00Z
L9raw = ee.ImageCollection('LANDSAT/LC09/C02/T1').filterDate(start,end).\
        filterDate(ee.Date(start),ee.Date(end).advance(1, 'day')).\
        filterMetadata('SUN_ELEVATION','greater_than', 0).\
        select(['B1','B5','B6','B7']).filter(ee.Filter.bounds(punto))
#
print(f"Date interval provided by the user: {start} - {end}\n")
print(f"Number of Landsat-8 images that covers the site \
{volcan} = {L8raw.size().getInfo()}")
#
print(f"Number of Landsat-9 images that covers the site \
{volcan} = {L9raw.size().getInfo()}\n")

#==================================================================#
#          UNIR, CALIBRAR y RECORTAR las imágenes Landsat          #
#==================================================================#

#========================================================#
# Función para calibrar 1 imagen landsat
def cal_landsat(img):
  return ee.Algorithms.Landsat.calibratedRadiance(img).\
     copyProperties(img, ['system:time_start'])
#========================================================#

#========================================================#
# Función para recortar (clip) 1 imagen
def clip_img(img):
   return img.clip(roi)
#========================================================#

#========================================================#
# Función para agregar la propiedad del tiempo
def add_time_start(image):
   return image.set('system:time_start', image.date())
#========================================================#

# Unir, Calibrar (clip) y Recortar todas las imágenes Landsat
Lcal = (L8raw.merge(L9raw)).map(cal_landsat).map(clip_img)

print(f"Total number of merged Landsat 8 & 9 callibrated and crop \
= {Lcal.size().getInfo()}")

# Extraer fechas de la colección Landsat unida
#date_property = Lcal.aggregate_array("system:time_start")
date_property = Lcal.aggregate_array("system:time_start").getInfo()
fechas_dt = pd.to_datetime(date_property, unit="ms", utc=True)

#==================================================================#
#         CALCULAR los NHI (SWIR y SWNIR) y EXTREME PIXELS         #
#==================================================================#

#=========================================#
# Landsat NHI SWIR > 0 | mid-low intensity
#=====================================================#
# Función para calcular los hot pixels (hp) del NHI_SWIR para 1 imagen Landsat
def L_nhi_swir_hp(img):
  nhi = img.normalizedDifference(['B7', 'B6']).rename('nhi_swir')
  return img.addBands(nhi.updateMask(nhi.gt(0)))
#=========================================#

#=======================================#
# Landsat NHI SWNIR > 0 / high intensity
#======================================================#
# Función para calcular los hot pixels (hp) del NHI_SWNIR para 1 imagen Landsat
def L_nhi_swnir_hp(img):
  nhi = img.normalizedDifference(['B6', 'B5']).rename('nhi_swnir')
  return img.addBands(nhi.updateMask(nhi.gt(0)))
#======================================#

#===========================#
# Píxeles calientes extremos
#========================================================#
# Función para Calcular PIXELES EXRTREMOS del NHI Landsat
def L_ext_pixel(img):
  ext_pix = (img.normalizedDifference(['B7', 'B6']))\
    .And(img.select('B6').gte(71.3)).And(img.select('B1').lt(70)).rename('L_ext_pix')
  return img.addBands(ext_pix.updateMask(ext_pix.gt(0)))
#========================================================#

#===================================================#
# Contar pixels en una imagenCollection y banda dada
#===================================================================#
# Function para contar el número de pixels de cada imagen en ImageCollection
def count_pixels_per_image(collection, bandname, scale):
    def f(img):
        band = img.select(bandname)
        # contar pixeles
        pixel_count = band.reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=img.geometry(),
            scale=scale,
            maxPixels=1e13
        ).get(bandname)
        return img.set('pixel_count', pixel_count)
        #
    #nombre = bandname + "_count"
    pixel_counts = collection.map(f).aggregate_array('pixel_count').getInfo()
    return pixel_counts
#===================================================================#


#============================================================================#
#         Calcular las radiancias Landsat B6 (1.6$μ$m) y B7 (2.2$μ$)         #
#============================================================================#

#=========================================================================#
# Función para enmascarar la B6 del OLI utilizando al NHI_SWIR como máscara
def mask_L_B6_swir(img):
  nhi = img.normalizedDifference(['B7', 'B6'])
  return img.select('B6').updateMask(nhi.gte(0)).rename('B6_nhi_masked_swir')
#=========================================================================#

#==========================================================================#
# Función para enmascarar la B6 del OLI utilizando al NHI_SWNIR como máscara
def mask_L_B6_swnir(img):
  nhi = img.normalizedDifference(['B6', 'B5'])
  return img.select('B6').updateMask(nhi.gte(0)).rename('B6_nhi_masked_swnir')
#==========================================================================#

#=========================================================================#
# Función para enmascarar la B7 del OLI utilizando al NHI_SWIR como máscara
def mask_L_B7_swir(img):
  nhi = img.normalizedDifference(['B7', 'B6'])
  return img.select('B7').updateMask(nhi.gte(0)).rename('B7_nhi_masked_swir')
#=========================================================================#

#==========================================================================#
# Función para enmascarar la B7 del OLI utilizando al NHI_SWNIR como máscara
def mask_L_B7_swnir(img):
  nhi = img.normalizedDifference(['B6', 'B5'])
  return img.select('B7').updateMask(nhi.gte(0)).rename('B7_nhi_masked_swnir')
#==========================================================================#

#========================================================#
# Función para sumar el valor de todos los píxeles de
# una banda específica en una ImgColección
def sum_band_each_image(collection, bandname, scale):
  def sum_band_per_image(img):
    band = img.select(bandname)
    sum_val = band.reduceRegion( reducer=ee.Reducer.sum(),
                                geometry=img.geometry(),
                                scale=scale,
                                maxPixels=1e13 ).get(bandname)
    return ee.Feature(None, {bandname: sum_val})
  sum_per_image = collection.map(sum_band_per_image)
  sum_values = sum_per_image.aggregate_array(bandname)
  return sum_values
#========================================================#

#=====================================================#
# Función para convertit una ee.lista and numpy float
def eelist2float(eelist):
  return np.array(eelist.getInfo(), dtype='float32')
#=====================================================#

print("\nComputing the NHI index over the entire image collection...")
#========================================#
#     NHI píxles calientes y extremos    #
# Aquí estoy creando una multicoleccion #
#========================================#
L_nhi_ext_pix = Lcal.map(L_nhi_swir_hp).map(L_nhi_swnir_hp).map(L_ext_pixel)
#print('\nSize of original L_nhi_ext_pix collection:', L_nhi_ext_pix.size().getInfo())


#==================================================#
#   Contando los NHI pixeles calientes y extremos  #
# Aquí estoy divdiendo la collection L_nhi_ext_pix #
#==================================================#
L_nhi_swir_pc = count_pixels_per_image(L_nhi_ext_pix, 'nhi_swir', 30)
L_nhi_swnir_pc = count_pixels_per_image(L_nhi_ext_pix, 'nhi_swnir', 30)
L_nhi_ep_pc = count_pixels_per_image(L_nhi_ext_pix, 'L_ext_pix', 30)


#====================================================================#
#                  ELIMINAR LAS IMÁGENES NHI VACÍAS                  #
#====================================================================#
filt_L_nhi_swir = filter_empty_images(
    collection=L_nhi_ext_pix.select('nhi_swir'),
    region=roi,
    scale=30
)

filt_L_nhi_swnir = filter_empty_images(
    collection=L_nhi_ext_pix.select('nhi_swnir'),
    region=roi,
    scale=30
)

filt_L_nhi_ep = filter_empty_images(
    collection=L_nhi_ext_pix.select('L_ext_pix'),
    region=roi,
    scale=30
)


#===================================================================#
#               AGREGAR EL CALCULO DE LA RADIANCIA B6 y B7 #
#===================================================================#

print('\nComputing the Landsat radiances for bands 6 & 7...')

#=============================#
# Para la banda 6 del Landsat #
#=============================#
Lb6_masked_swir = Lcal.map(mask_L_B6_swir)
#print('Lb6_masked_swir:',Lb6_masked_swir.first().bandNames().getInfo())

Lb6_masked_swnir = Lcal.map(mask_L_B6_swnir)
#print('Lb6_masked_swnir:',Lb6_masked_swnir.first().bandNames().getInfo())

Lrad_b6_swir = sum_band_each_image(Lb6_masked_swir, 'B6_nhi_masked_swir', 30)
#print('Radiancia banda 6 nhi_swir:', Lrad_b6_swir.getInfo())
#
Lrad_b6_swnir = sum_band_each_image(Lb6_masked_swnir, 'B6_nhi_masked_swnir', 30)
#print('Radiancia banda 6 nhi_swnir:', Lrad_b6_swnir.getInfo())

rad_tot_Lb6 = eelist2float(Lrad_b6_swir) + eelist2float(Lrad_b6_swnir)
#print('Landsat B6 radiancia total =', rad_tot_Lb6, '\n')

#=============================#
# Para la banda 7 del Landsat #
#=============================#
Lb7_masked_swir = Lcal.map(mask_L_B7_swir)
#print('Lb7_masked_swir:',Lb7_masked_swir.first().bandNames().getInfo())

Lb7_masked_swnir = Lcal.map(mask_L_B7_swnir)
#print('Lb6_masked_swnir:',Lb6_masked_swnir.first().bandNames().getInfo())

Lrad_b7_swir = sum_band_each_image(Lb7_masked_swir, 'B7_nhi_masked_swir', 30)
#print('Radiancia banda 7 nhi_swir:', Lrad_b7_swir.getInfo())
#
Lrad_b7_swnir = sum_band_each_image(Lb7_masked_swnir, 'B7_nhi_masked_swnir', 30)
#print('Radiancia banda 7 nhi_swnir:', Lrad_b7_swnir.getInfo())

rad_tot_Lb7 = eelist2float(Lrad_b7_swir) + eelist2float(Lrad_b7_swnir)
#print('Landsat B7 radiancia total =', rad_tot_Lb7)
#

#=============================================================================#
def gee_raster_2_shp(collection, output_folder, scale=30):
    import geopandas as gpd
    from shapely.geometry import shape # Opcional, para manejo avanzado de geometrías
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img_list = collection.toList(collection.size())
    num_images = collection.size().getInfo()

    for i in range(num_images):
        image = ee.Image(img_list.get(i))
        img_id = image.get('system:index').getInfo()
        
        image_int = image.select([0]).multiply(100).toInt32()
        print(f"Vectorizando imagen: {img_id}...")

        try:
            vectors = image_int.reduceToVectors(
                geometry=image.geometry(),
                scale=scale,
                geometryType='polygon',
                eightConnected=True,
                labelProperty='value',
                maxPixels=1e10
            )

            features = vectors.getInfo()['features']
            
            if features:
                gdf = gpd.GeoDataFrame.from_features(features)
                gdf.crs = "EPSG:4326"
                
                # Volver el valor a decimal en el archivo final
                gdf['value'] = gdf['value'] / 100.0
                
                file_path = os.path.join(output_folder, f"{img_id}.shp")
                gdf.to_file(file_path)
                print(f"Guardado: {file_path}")
            else:
                print(f"Sin datos en {img_id}")
                
        except Exception as e:
            print(f"Error en {img_id}: {e}")

#=============================================================================#

#================================================================#
#                CARPETAS PARA GUARDAR RESULTADOS                #
#================================================================#

pwd = os.getcwd()
#
title1 = "Number of NHI hot and extreme pixels for " + volcan
title2 = "Landsat Radiances B6 and B7 for " + volcan
volcan = volcan.replace(" ","_")
#
# carpeta: NHI_SWIR_results rásters #
n1 = volcan+"_NHI_raster_mid_2_low_hot_pixels"
nhi_swir_folder = os.path.join(pwd, n1)
#print("nhi_swir_folder:", nhi_swir_folder)
#
# carpeta: NHI_SWNIR_results rásters #
n2 = volcan+"_NHI_raster_high_intensity_pixels"
nhi_swnir_folder = os.path.join(pwd, n2)
#print("nhi_swnir_folder:", nhi_swnir_folder)
#
# carpeta: NHI_EXTREMOS_results rásters #
n3 = volcan+"_NHI_raster_extreme_hot_pixels"
nhi_extremes_folder = os.path.join(pwd, n3)
#print("nhi_extremos_folder:", nhi_extremos_folder)
#
# carpeta para los html
n4 = volcan+"_NHI_html_results"
nhi_html_folder = os.path.join(pwd, n4)#=================================#

#==================================================================#

#=======================================================================================#
#                          Guardar resultados Rasters y shapes                          #
#=======================================================================================#
# Colección NHI_SWIR #==========================================================#
if (filt_L_nhi_swir.size().getInfo()) == 0:
    print("\nNo NHI SWIR pixels were found")

else:
    if (Path(nhi_swir_folder).is_dir()) == False:
        print('The following folder will be crated:"nhi_swir_results"\n')
        os.mkdir(nhi_swir_folder)
    geemap.ee_export_image_collection(filt_L_nhi_swir, out_dir=nhi_swir_folder)
    gee_raster_2_shp(filt_L_nhi_swir.select('nhi_swir'), nhi_swir_folder)
#=============================#

#=====================#
# Colección NHI_SWNIR #=========================================================#
if (filt_L_nhi_swnir.size().getInfo()) == 0:
    print("\nNo NHI SWNIR pixels were found \n")

else:
    if (Path(nhi_swnir_folder).is_dir()) == False:
        print('The following folder will be crated:"nhi_swnir_results"\n')
        os.mkdir(nhi_swnir_folder)
    geemap.ee_export_image_collection(filt_L_nhi_swnir, out_dir=nhi_swnir_folder)
    gee_raster_2_shp(filt_L_nhi_swnir.select('nhi_swnir'), nhi_swnir_folder)
#=============================#

#=====================#
# Colección NHI_EP #=========================================================#
if (filt_L_nhi_ep.size().getInfo()) == 0:
    print("\nNo NHI Extreme Pixels were found \n")

else:
    if (Path(nhi_extremes_folder).is_dir()) == False:
        print('The following folder will be crated:"nhi_extremes_results"\n')
        os.mkdir(nhi_extremes_folder)
    geemap.ee_export_image_collection(filt_L_nhi_ep, out_dir=nhi_extremes_folder)
    gee_raster_2_shp(filt_L_nhi_ep.select('L_ext_pix'), nhi_extremes_folder)
#=============================#


print('\nNumber of images containing NHI low to moderate hot pixels =', filt_L_nhi_swir.size().getInfo())
print("Number of images containing NHI strong hot pixels:", filt_L_nhi_swnir.size().getInfo())
print("Number of images containing NHI extreme hot pixels:", filt_L_nhi_ep.size().getInfo())
print("")

#=============================================================================================#

#===============================================================================#
#       Convertir todos los resultados importantes a 1 solo pd.DataFrame        #
#===============================================================================#

print('Generating the CSV data file...')
#=====================================================#
# Función para convertit una ee.lista and numpy entero
def list2int(lista):
  return np.array(lista, dtype='int')
#=====================================================#

#======================================#
# nhi pix calientes
nhi_tot_swir_pc = list2int(L_nhi_swir_pc)

nhi_tot_swnir_pc = list2int(L_nhi_swnir_pc)

#nhi_tot_hpc = list2int(L_nhi_swir_pc) + list2int(L_nhi_swnir_pc)
nhi_tot_hpc = nhi_tot_swir_pc + nhi_tot_swnir_pc
#print('Landsat Cantidad Total de pixeles calientes por imagen:',nhi_tot_hpc)

# area nhi pix calientes
nhi_tot_area = nhi_tot_hpc*900
#print('Landsat Área Total de pixeles calientes por imagen:',nhi_tot_area)

# nhi pix calientes extremos
L_nhi_ep_pc = list2int(L_nhi_ep_pc)
#print('Landsat Cantidad Total de pixeles calientes EXTREMOS:',L_nhi_ep_pc)

# area nhi pix calientes extremos
L_nhi_ep_pc_area = L_nhi_ep_pc*900
#print('Landsat área Total de píxeles calientes EXTREMOS:',L_nhi_ep_pc_area)

columnas = ["Date", "Total NHI SWIR hot pixels", "Total NHI SWNIR hot pixels", \
           "Total NHI SWIR + SWNIR hot pixels", "Hot pixels area m2",\
           "Total NHI extreme pixels", "Extreme hot pixels area m2",\
           "Radiance B6 (1.6 μm)", "Radiance B7 (2.2 μm)"]
#
df = pd.DataFrame(zip(fechas_dt, nhi_tot_swir_pc, nhi_tot_swnir_pc, nhi_tot_hpc, nhi_tot_area,\
     L_nhi_ep_pc, L_nhi_ep_pc_area,rad_tot_Lb6,rad_tot_Lb7),columns=columnas)
#
df = df.sort_values(by='Date', ascending=True)
df['Date'] = df['Date'].dt.strftime('%Y-%b-%d')
#print("df['Date']\n", df['Date'])
nombre_csv_ext = "NHI_all_results_"+volcan+".csv"
csv_name = os.path.join(pwd, nombre_csv_ext)
df.to_csv(nombre_csv_ext, index=False)
print("Snippet of the CSV's file content:")
print(df.head())
print(f"\nNHI and radiance results saved into file: {nombre_csv_ext}\n")

#=====================================================================================#
#                                      GRÁFICAS                                       #
#=====================================================================================#

import plotly.express as px
print("Generating the plots in HTML formats...\n")

fig = px.line(df, x='Date', y=["Total NHI SWIR hot pixels", "Total NHI SWNIR hot pixels",\
    "Total NHI extreme pixels"], markers=True,\
    title=title1,\
    color_discrete_map={"Total NHI SWIR hot pixels": "orange", "Total NHI SWNIR hot pixels": "red",\
    "Total NHI extreme pixels": "purple"},\
    symbol="variable",
    symbol_map={"Total NHI SWIR hot pixels": "circle", "Total NHI SWNIR hot pixels": "square",\
    "Total NHI extreme pixels": "triangle-down"})
fig.update_yaxes(title_text="Number of pixels",\
    title_font=dict(size=14, color='blue'))
fig.update_xaxes(rangeslider_visible=True)
NHI_pix_html = "NHI_pixels_"+volcan+".html"
fig.write_html(NHI_pix_html)

fig = px.line(df, x='Date', y=["Radiance B6 (1.6 μm)","Radiance B7 (2.2 μm)"], markers=True,\
    title=title2,\
    color_discrete_map={"Radiance B6 (1.6 μm)": "black", "Radiance B7 (2.2 μm)": "red"},\
    symbol="variable",
    symbol_map={"Radiance B6 (1.6 μm)": "circle", "Radiance B7 (2.2 μm)": "square"})
fig.update_yaxes(title_text=r"$Spectral Radiance \, (W\,sr^{-1}\,m^{-2}\,μm{-1})$",\
    title_font=dict(size=14, color='blue'))
fig.update_xaxes(rangeslider_visible=True)
OLI_radiance_html = "OLI_Radiances_B6_B7_"+volcan+".html"
fig.write_html(OLI_radiance_html)
#fig.show()

#============================================================================#

print("The script has successfully finish processing the Landsat 8 & 9 data")
print("Thanks for using this script!\n")
print("Don't forget to cite it as:")
print("Saballos, J. A. (2026). Python script to compute the Normalized Hotspot Index (NHI) with Landsat 8 and 9 data. GitHub: https://github.com/saballos/nhi_oli_8_9_sp.py\n")