# nhi_oli_8_9_sp
Python script (should work with versions 3.11+) to compute the Normalized Hotspot Indices (HNI), using only Landsat 8 &amp; 9 data, developed by Marchese et al. (2019) and Genzano et al. (2020) of any point on Earth. The last authors also developed a freely available web app, named the "NHI tool"(https://nicogenzano.users.earthengine.app/view/nhi-tool)
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
