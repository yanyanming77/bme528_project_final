# BME 528 Project Group3
# Decision Support for Radiation Therapy

What's in it:
1. The bme_gui folder contains all the code to run this app
2. The requirement.txt contains all the required packages to run the app
3. The generate_insert_data.ipynb is the notebook I used to generate dummy data and store them in the SQlite database
4. The sample_dcm folder conatins 5 .dcm files to test the functionality of this app

Run the app:
1. To run the app, install all the packages listed in the requirements.txt file
2. After installing all the packages and dependencies, run the following line in the work directory: 
  python manage.py runserver 
3. Then open the promped link on local host

Use the app:
1) home (welcome) page: The home page, you can log in to the system
2) login page: here you can log in, create a new account, or go back to the welcome page
3) introduction page: here the background and the general CAD system workflow are introduced
4) similarity match page: 
   1. upload DICOM
      choose a .dcm from the local folder, click "Parse Data" button, the file will be parsed by pydicom parser at the backend, the parsed content will be displayed below
   2. verify the stored .dcm file
      click "Verify Record Storage", a table will show all the records currently in the database, scroll down to the bottom to find the latest uploaded file
   everytime there's an upload, similarity scores to the current case will be randomly generated for each case in the database, to simulate the general similarity score calculation in the general CAD/data mining process
   3. filter historical cases
       choose ROI from the dropdown menu, select institution by checking the boxes, and define similarity score, ROI dose PTV dose, PTV volume, etc. by dragging the slide bars
       click "Filter Results"
       all the filter criteria defined by the user will be displayed in the result box
       if no matching cases, there will be a warning message in the result box to ask the user to change the filter criteria
       if there are matching cases, the results will be displayed
   4. visualization
       the scatter plots dipicting variables such as PTV dose, ROI dose, etc. vs. % of similarity will be displayed in an interactive format
       the user can hover over the plots and see the detailed values of each point (each historical case)
