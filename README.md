# mosquito-risk
Geo-Statistical Modeling of Mosquito Risk Epicenters in Selected Kenyan Localities

## Summary

The Geospatial Risk Analysis of Mosquitoes in Kenya (GRAMIK) tool is a mathematical and computational interface for quantifying the risk of mosquito occurrence across geographic locations. This computational approach employs K-Nearest Neighbors (KNN) regression models and integrates spatio-temporal data with environmental factors, namely elevation and proximity to water bodies. The risk is represented on a scale ranging from 1 (low) to 3 (high). The algorithm successfully adapts to the dynamic nature of risk factors by accounting for monthly variations and provides a reliable predictive framework that can be extended to other epidemiological studies.

## Dataset Collection and Methodology

To facilitate the application of our computational model for predicting mosquito risk in Kenya, a comprehensive dataset was used, integrating a multitude of factors deemed relevant to the risk calculation. These factors include but are not limited to geographical coordinates, elevation, proximity to water bodies, climate type, and monthly risk levels. The dataset presently encompasses 40 Kenyan localities, each meticulously characterized to ensure robustness in the risk assessment.

### Mosquito Breeding Grounds: 

Information on endemic regions in Kenya where mosquitoes predominantly breed was extracted from a study available on NCBI.

### Disease-Causing Mosquito Species and Vectors: 

Species-specific data were obtained from NCBI and included in the dataset to reflect the heterogeneity in disease risk across species.

### Densities of Mosquito Vectors: 

Data on mosquito density were sourced from a study in Wiley Online Library.

### Predictive Models for Mosquito Density: 

Empirical models from NCBI were reviewed to inform the algorithm's predictive capabilities.

### Seasonal Abundance: 

Seasonal factors were accounted for based on a study available on BioMed Central.

### Mosquito Occurrence Dataset: 

Additional occurrence data were obtained from the GBIF database.

### Full List of Datasets: 

Mosquito Breeding Grounds
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6627689/#:~:text=Mosquito%2DBorne%20Disease%20Endemic%20Regions%20in%20Kenya&text=Some%20of%20these%20regions%20include,breeding%20areas%20for%20mosquito%20species. 

Disease Causing Mosquito Species 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6627689/table/insects-10-00173-t001/ 

Mosquito Vectors in Kenya
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6627689/table/insects-10-00173-t001/  

Densities of Mosquito Vectors
https://onlinelibrary.wiley.com/doi/full/10.1111/j.1948-7134.2013.12019.x 

Predictive Models for Mosquito Density
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6367629/ 

Seasonal Abundance of Mosquitos
https://parasitesandvectors.biomedcentral.com/articles/10.1186/s13071-017-2598-2#:~:text=Aedes%20aegypti%2C%20the%20known%20DENV,Kilifi%20and%20Kisumu%20vs%20Nairobi. 

mosquito occurrence dataset
​​https://www.gbif.org/occurrence/download?dataset_key=88e38292-f762-11e1-a439-00145eb45e9a 


The final dataset comprises multiple attributes for each locality, such as:

- location: Name of the locality
- region: Geographical region within Kenya
- Latitude and Longitude: Geographic coordinates
- elevation: Elevation in meters above sea level
- climate: Köppen Climate Classification
- january to december: Monthly mosquito risk level (Low/Moderate/High)
- dist_from_water: Distance from the nearest water body in meters

## Methodology

### Climate Factors 
The Köppen Climate Classification is integrated into the data set, offering detailed categorizations of climate like 'Tropical Rainforest,' 'Hot semi-arid,' and 'Temperate.' Each location's climate classification is utilized to modify the temporal weightings for the risk calculation. For instance, in a 'Tropical Rainforest' climate, the risk of mosquito occurrence might be consistently high but could be prone to subtle fluctuations based on the wet and dry seasons. On the other hand, 'Hot semi-arid' climates may experience more substantial variations in risk depending on water availability.

### Temporal Weighting
The algorithm accepts a date string and extracts the month and day for temporal analysis, accounting for seasonal variations in mosquito risks. It dynamically computes the 'current month' and 'next month' based on the input date, accounting for year transitions (e.g., from December to January). A weight is calculated for the current and next months, which is proportional to the number of days remaining in the current month and days elapsed, respectively.​
 
### Spatial Data Modeling
The K-Nearest Neighbors (KNN) regression models are trained on latitude and longitude for predicting elevation and distance from water bodies at unmeasured points. For each query point, the model predicts from relevant climate features based on the 5 nearest neighbors.

### Risk Calculation
A weighted average is computed using the risk values for the current and next months from the data. The predicted elevation and distance from water bodies at a given location further modulate this weighted average. The risk is adjusted using sub-linear transformations of elevation and distance from water bodies.

The resulting risk output is then clipped to lie between 1 and 3, ensuring interpretability and practical utility.

## Results
The algorithm produces a risk output for each geographic point, and the risk value is inherently adaptive to temporal and environmental variations. It yields a granular risk stratification, which is crucial for focused interventions in public health.

## Conclusion
The algorithm provides a robust, adaptive, and spatially aware method for quantifying the risk of mosquito occurrence. It accommodates dynamic risk factors and leverages both temporal and spatial data for more accurate and actionable predictions. This interdisciplinary approach opens new avenues for epidemiological studies and has significant implications for public health strategies.
