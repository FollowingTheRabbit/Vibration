# Vibration
- This document is based on a case study for Binahki. 
- The data concerns a small motor (Power: $250W$) whose stated vibration on the $(x,y,z)$ axis is measured with accelerometer sensors.
- The main data are in the directory *./Data/Vibration and Temperature Data*. You can also find them in a zipped *.rar* file.
  - The title of these files, which are, for example, *1658832447 - 1658832513.csv*, corresponds to the time spent collecting the data. There is about one minute in each file and about an hour between one file and another.
- With this data a dashboard was developed with the **Dash** library of **python**. This is in the file *./src/dashboar_vibracao/app.py* which is supported in the file *./src/dashboar_vibracao/analise.py*, where some auxiliary functions are defined. 
- As a training assignment, another simple dashboard has been developed in the directory *./src/dashboard_current_phases/app.py*. This is supported in the files *./src/dashboard_current_phases/analysis.py* and the files *Input v2.csv* and *Validation v2.csv* stored in the directory *./Data*.
- In both cases, the *analysis.ipynb* file is a preliminary study to help develop the dashboard.
- The codes are a bit polluted with some functions and pieces of code that are not used in this latest version. In the future they will be cleaned up.
- The application file contains most of the libraries used in this project. However, some libraries from previous projects are still there, I hope to soon reduce it to the only libraries used.
