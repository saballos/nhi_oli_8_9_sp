# nhi_oli_8_9_sp
This is a Python script (should work with versions 3.11+) to compute the Normalized Hotspot Indices (HNI), using only Landsat 8 &amp; 9 data, developed by Marchese et al. (2019) and Genzano et al. (2020) of any point on Earth. The last authors also developed a freely available web app, named the **NHI tool** (https://nicogenzano.users.earthengine.app/view/nhi-tool).

This tool computes the NHI indices for Landsat and Sentinel-2 data for any volcano listed in the Smithsonian Instituions's Global Volcanism Program (GVP) catalog, and also leverages the Google Earth Engine (GEE) data archive and JavaScript resources freely available.

This current script, instead, computes the NHI for Landsat 8 &amp; 9 data only. A future release will include the Sentinel-2 data processing as well.
Unlike the NHI tool, this script is able to compute the NHI indices for any point (or circular area) on Earth, and provides the results in raster Geotiff and shape formats. The complete list of outputs is:
1. A CSV file containing the following results:
   
    1.1. "Date" of each Landsat image available within the given time frame
   
    1.2. "Total HNI SWIR hot pixels"
   
    1.3. "Total HNI SWNIR hot pixels"
   
    1.4. "Total HNI SWIR + SWNIR hot pixels"
   
    1.5. "Hot pixels area m<sup>2</sup>"
   
    1.6. "Total NHI extreme pixels"
   
    1.7. "Extreme hot pixels area m<sup>2</sup>"
   
    1.8. "Radiance B6 (1.6 μm)"
   
    1.9. "Radiance B7 (2.2 μm)"

3. Individual images of the Landsat 8 & 9 raster data in GeoTiff format, in which NHI hot
   pixels were found
   
4. Vector shapefile (ESRI format) data of those Landsat 8 &amp; 9 raster images mentioned in item 2.

5. Plots in interactive HTML format of some variables listed in item 1.

Thus, the user must have a Gmail or an institutional workspace account. To avoid charges, you must select the Non-commercial or Research/Academic track during registration. Details on how to properly register your account can be found here: (https://code.earthengine.google.com/register?authuser=2)

Assuming that you have setup your GEE account properly and your prompt in the terminal window is located within the folder containg this script, you can run this script through the linux (or conda) terminal window by executing the following command line:
**python nhi_oli_8_9_sp_v01.py input_file.txt**

But, if you are under a Windows OS, execute instead:
**python.exe nhi_oli_8_9_sp_v01.py input_file.txt**

If you want to know more about my research, please visit my ResearchGate profile: (https://www.researchgate.net/profile/Jose-Saballos-2)

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

## Requirements

- python (3.11, 3.12, or 3.13)
- pandas
- numpy
- geopandas
- matplotlib
- plotly
- shapely
- geemap
- earthengine-api

## Installation

There are different ways to install and run this script. I will describe here only three different installation methods.
#### 1. Conda environment creation:
If you have ```conda``` already installed on your OS, follow the steps below. If you do not have ```conda``` installed in your system (Linux/Unix, macOS, Windows), I recommend to install ```miniconda``` following the instruction provided on the ```miniconda``` website [miniconda page](https://docs.anaconda.com/miniconda/). After the installation of miniconda follow these steps:

* Copy the ```URL``` of this repository by clicking on the ```<> Code``` green button at the top of this tool's GitHub page and copying the ```HTTPS``` address that is shown, i.e. ```https://github.com/saballos/nhi_oli_8_9_sp.git```
* Make sure you have the ```Git``` software already installed on your computer. If not, you must downloaded it from the [Git page](https://git-scm.com/downloads) and install it. There is a version for Linux/Unix, macOS and Windows systems. After the installation of the Git software, open a terminal window in your Linux or macOS system (in Windows OS open a ```git bash``` command line window)
* Locate yourself into the folder you want this repository to be cloned by using the ```cd``` command 
* Type the following command line: ```git clone https://github.com/saballos/nhi_oli_8_9_sp.git```, and hit enter. You'll see a new folder named ```nhi_oli_8_9_sp```
* If you are using Windows OS, open a ```conda``` terminal window and locate yourself into the ```modvolc_py_sp``` folder that was cloned. But if you are using linux/Unix or macOS move into the ```nhi_oli_8_9_sp``` folder with the ```cd``` command (e.g. ```cd nhi_oli_8_9_sp```). Then, type the following command line: ```conda env create -f nhi_oli_8_9_sp.yml```, and hit enter. This process may take a while
* You have now created the ```nhi_oli_8_9_sp``` conda environment. Type in your terminal ```conda env list``` and you'll see the ```nhi_oli_8_9_sp``` env listed, and now you have to activate it by typing the following command: ```conda activate nhi_oli_8_9_sp```, and hitting enter
* Since your terminal window (or conda command line window) is located inside the ```nhi_oli_8_9_sp``` cloned folder and the ```nhi_oli_8_9_sp``` conda environment is activated, type now: ```pip .```, and hit enter. Type ```y``` when prompted and hit enter

#### 2. Installation with pip command:
* Linux/Unix users open a terminal window and type: ```pip install nhi_oli_8_9_sp```, and hit enter
* For Windows OS users, you need to have installed ```python 3.11``` or ```python 3.12``` or ```python 3.13``` first, then open a python command line window and type: ```pip install nhi_oli_8_9_sp```, and hit enter

#### 3. python environment creation:
For linux/Unix users, create a virtal environment in the following way:
* Clone the ```nhi_oli_8_9_sp``` GitHub repository as described above, in section 1. ```Conda environment creation```
* Move yourself into the cloned folder with the ```cd``` command
* Type in your terminal: ```python3 -m venv nhi_oli_8_9_sp```, and hit enter
* Activate the environment just created by typing: ```source nhi_oli_8_9_sp/bin/activate```, and hitting enter
* Type ```pip install -r requirements.txt```, and hit enter

For Windows OS users:
* Clone the ```nhi_oli_8_9_sp``` GitHub repository as described above, in section 1. ```Conda environment creation```
* Open a python command line window and move yourself into the cloned folder and type in your terminal: ```python.exe -m venv modvolc_py_sp```, and hit enter
* Activate the enviroment just created by typing: ```modvolc_py_sp\Scripts\activate.bat```, and hitting enter
* Type ```pip install -r requirements.txt```, and hit enter
