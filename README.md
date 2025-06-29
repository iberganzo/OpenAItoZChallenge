# OpenAI to Z Challenge
Visual Language Modeling for Automated Large-Scale Archaeological Site Detection Across the Amazon: An End-to-End Workflow Inspired by the OpenAI to Z Challenge

## 1. Dataset
Prior to implementing the workflow for a new archaeological survey, it is necessary to generate the dataset using Sentinel-2 satellite imagery through Google Earth Engine. Identify the target area for the survey (roi), replicate the JavaScript code (GEE_EVI_NDRE.txt) precisely within Google Earth Engine, and execute the processes required to export the corresponding satellite imagery, enhanced vegetation index (EVI) and normalized difference red edge (NDRE).

The next step involves subdividing the survey area into tiles to enable the implementation of the workflow, which classifies images based on the presence or absence of archaeological sites rather than detecting them directly. This will be done using the TIF_to_JPG_and_Crop.py script, which partitions the original TIF file into 128x128 pixel tiles, producing outputs in both TIF format (to retain geospatial referencing) and JPG format.

As a result, two datasets have been generated: EVI and NDRE. The EVI dataset will be used to identify potential archaeological sites, while the NDRE dataset will assist in detecting rivers and paleochannels—critical features for assessing the likelihood of a site's validity. The survey area used in the challenge to locate new potential sites can be found in the survey_area.zip ZIP file.

## 2. Survey area
But how do we choose the area in which to conduct the survey? The answer to this question was obtained by analyzing known archaeological sites through data extraction using OpenAI's o3 model.

To this end, we analyzed various publications and selected 'Pre-Columbian earth-builders settled along the entire southern rim of the Amazon' (De Souza et al., 2018) as the basis for extracting site information from its supplementary material PDF. This study was chosen as a compelling case due to the inclusion of geographic coordinates for the published archaeological sites. By running PART I of the Jupyter Notebook (BerganzoBesga_Orengo_OpenAItoZ_Workflow.ipynb) in Google Colab, our code leverages the OpenAI's o3 model to automatically extract archaeological sites (if any are present) and subsequently generates a shapefile with the results. In this manner, we extracted 104 sites, corresponding to all those reported in the article, which we used as ground-truth. Therefore, by simply changing the URL to a different article (or providing a local PDF path if no URL is available), the same extraction process can be applied to obtain archaeological site data from other publications. Remember to set your OPenAI API key before running the notebook.

## 3. The archaeological sites are detectable beneath the forest canopy without LiDAR
By analyzing satellite imagery from Landsat-5 (pre-1995) and Sentinel-2 over the known archaeological sites extracted from De Souza et al. (see section 2), we observed that these sites are visible despite being located beneath forest canopy, without the need for additional tools such as LiDAR. To overcome the issues presented by the use of Landsat 5 imagery, such as the low-resolution, Sentinel-2 satellite imagery has been employed. For this purpose, we use the EVI imagery, generated through Google Earth Engine (see section 1), and apply OpenAI’s GPT-4.1 model to classify the JPG images based on the presence or absence of archaeological sites. To ensure reproducibility of results, PART II of the Jupyter Notebook (BerganzoBesga_Orengo_OpenAItoZ_Workflow.ipynb) shows the same performance metrics that guided the selection of our prompt.

![Figure8](https://github.com/user-attachments/assets/ba23a2f7-38db-416e-802c-06e88e3fe0e5)

A new comprehensive survey can be conducted using PART IV of the Jupyter Notebook (BerganzoBesga_Orengo_OpenAItoZ_Workflow.ipynb) by simply specifying your own survey area.

## 4. Validation
Another conclusion drawn from the analysis of known archaeological sites using satellite imagery (see Section 2) is that these sites are typically located near rivers and paleochannels, which are no longer visible today. Therefore, by utilizing the NDRE index, we can visualize paleochannels and employ this insight as a validation method for detected sites (see Section 3). To this end, we developed a code that, leveraging OpenAI’s GPT-4.1 and building upon the approach used previously, classifies NDRE images based on the presence or absence of rivers and paleorivers, for those previously detected sites (see section 3). Those near rivers or paleochannel will be identified as new potential sites (potential_sites_detected.txt). To ensure reproducibility of results, PART III of the Jupyter Notebook (BerganzoBesga_Orengo_OpenAItoZ_Workflow.ipynb) shows the same performance metrics that guided the selection of our prompt.

![Figure9](https://github.com/user-attachments/assets/d0f7959d-be96-494f-8d76-4a3d8859ddb6)

A new comprehensive survey can be conducted using PART IV of the Jupyter Notebook (BerganzoBesga_Orengo_OpenAItoZ_Workflow.ipynb) by simply specifying your own survey area.

## 5. Georeferencing
Once the sites have been detected and validated, a TXT file (potential_sites_detected.txt) is generated containing information about the potential new sites detected, along with their locations within the images. Using the geo.py script, and specifying the path to the previously cropped TIF files, a shapefile with the detected potential sites (potential_sites_detected.shp) can be created.


