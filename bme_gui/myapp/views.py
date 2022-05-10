from pickle import TRUE
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse

# import DB
from myapp.models import *

# import forms
from myapp.forms import *

# authentication
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.template.loader import get_template

# import functions
from myapp.my_functions import *

# other packages
import pandas as pd
from pydicom import dcmread
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go


# home page
def homepage(request):
    return render(request, 'homepage.html')

# registration page
def register_request(request):
	if request.method == "POST":
		form = user_registration(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = user_registration()
	return render (request=request, template_name="register.html", context={"register_form":form})


# index page - introduction
@login_required
def index(request):
    return render(request, 'index.html')


# similarity match page
@login_required
def similarity_match(request):
    # upload dicom
    parsed_dicom_from_file = {} # an empty dict to prevent error
    print("parsed_dicom before posting: ", parsed_dicom)
    ptv_dose_plot = None
    roi_dose_plot = None
    ptv_volume_plot = None
    rt_dose_plot = None
    roi_roi_distance_plot = None
    roi_roi_overlap_plot = None
    flag_df_empty=0
    selected_roi=None
    selected_institution=None
    selected_similarity_min=None
    selected_roi_min=None
    selected_roi_max=None
    selected_ptv_min=None
    selected_ptv_max=None
    selected_ptv_volume_min=None
    selected_ptv_volume_max=None
    selected_roi_roi_distance=None
    selected_roi_roi_overlap=None
    submitbutton=None


    dicom_form=UploadForm()
    # if a file is uploaded
    if request.method == "POST":
        dicom_form = UploadForm(request.POST, request.FILES)
        if dicom_form.is_valid():
            dicom_form.save()
            uploaded_file = request.FILES['uploadedFile']
            print("type of file: ", type(uploaded_file))

            # save file
            document = Document(
                uploadedFile = uploaded_file
            )
            document.owner = request.user
            document.save()

            # read dicom
            read_dicom = dcmread(uploaded_file.open())
            # print("read dicom: ", read_dicom)

            # parse dicom and store into DB
            parsed_dicom_db = parsed_dicom() # create a db object
            parsed_dicom_from_file = parse_dicom(read_dicom, parsed_dicom_db)
            # print("parsed dicom after posting: ", parsed_dicom_from_file)

            # if there's an upload, generate dummy similarity score for each record in in <similarity> DB
            random_similarity = list(np.random.uniform(0.1,0.99,600).round(2))
            for i in range(1,len(random_similarity)+1):
                s = Similarity.objects.get(id=i)
                s.similarity = random_similarity[i-1]
                s.save()

    forms = big_form()
    # if the form is submitted
    if request.method =='GET':
        forms=big_form(request.GET)
        print("method is validated")
        if forms.is_valid():
            print("the form is valid ")
            selected_roi= forms.cleaned_data['roi']
            print("aaaa selected roi: ", selected_roi)
            submitbutton = request.GET.get('submit_button')
            print("submit status: ", submitbutton)

            if submitbutton:
                print("new submit status: ", submitbutton)
                # selected values
                selected_roi = forms.cleaned_data['roi']
                selected_institution = forms.cleaned_data['institution']
                selected_similarity_min = float(request.GET.get('range_similarity'))/100
                selected_roi_min = float(request.GET.get('ROI_min'))
                selected_roi_max = float(request.GET.get('ROI_max'))
                selected_ptv_min = float(request.GET.get('PTV_min'))
                selected_ptv_max = float(request.GET.get('PTV_max'))
                selected_ptv_volume_min = float(request.GET.get('PTV_volume_min'))
                selected_ptv_volume_max = float(request.GET.get('PTV_volume_max'))
                selected_roi_roi_distance = float(request.GET.get('ROI_distance'))
                selected_roi_roi_overlap = float(request.GET.get('ROI_overlap'))/100

                print("roi: {}, institution: {}, min_similarity: {}, roi_min: {}, roi_max: {}, ptv_min: {}, ptv_max: {}, ptv_volume_min: {}, ptv_volume_max: {}, roi_roi_distance: {}, roi_roi_overlap: {}".format(selected_roi, selected_institution, selected_similarity_min, selected_roi_min, selected_roi_max, selected_ptv_min, selected_ptv_max, selected_ptv_volume_min, selected_ptv_volume_max, selected_roi_roi_distance, selected_roi_roi_overlap))

                # chaining filters
                # filters for other slide bars
                t = Treatment.objects.filter(roi_dose__range=[selected_roi_min, selected_roi_max],
                                            ptv_dose__range=[selected_ptv_min,selected_ptv_max],
                                            ptv_volume__range=[selected_ptv_volume_min,selected_ptv_volume_max],
                                            roi_roi_distance__lte=selected_roi_roi_distance,
                                            roi_roi_overlap__lte=selected_roi_roi_overlap)
                # filters for roi and institution (could be left blank)
                if selected_roi != "enter":
                    t = t.filter(roi__exact=selected_roi)
                    # print("query1: ", t.query)
                if selected_institution != "":
                    cleaned_institution = selected_institution.replace('[','').replace(']','').replace("'",'')
                    cleaned_institution = list(cleaned_institution.split(', '))       
                    t = t.filter(institution__in=cleaned_institution)
                    # print("query 2: ",t.query)

                # filters for similarity
                s = Similarity.objects.filter(similarity__gte=selected_similarity_min)
                    # print("s value: ", s.values())
                # create an empty list for the patient_ids
                retreived_patient_id_list = []
                for record in list(s.values()):
                    retreived_patient_id_list.append(record['patient_id_id'])
                # print("id list: ", retreived_patient_id_list)
                ts = t.filter(patient_id__in = retreived_patient_id_list)

                # convert to df and merge the results
                ts=ts.values()
                df1 = pd.DataFrame(list(ts)) 
                s = s.values()
                df2 = pd.DataFrame(list(s))
                # print("df1: ", df1.head())
                # print("df2: ", df2.head())

                # if both df1 and df2 have records
                if len(df1)>0 and len(df2)>0:
                    # inner join two tables
                    df = df1.merge(df2, left_on='patient_id', right_on='patient_id_id')
                    print("head of the file: ", df.head())
                    print("shape of the file", df.shape)

                    # create visualizations
                    ptv_dose_plot = make_plot(df, 'similarity', 'ptv_dose', 'Similarity', 'PTV Dose', '#8fbc8f')
                    roi_dose_plot = make_plot(df, 'similarity', 'roi_dose', 'Similarity', 'ROI Dose', '#e9967a')
                    ptv_volume_plot = make_plot(df, 'similarity', 'ptv_volume', 'Similarity', 'PTV Volume', '#00bfff')
                    rt_dose_plot = make_plot(df, 'similarity', 'rt_dose', 'Similarity', 'RT Dose', '#ffd700')
                    roi_roi_distance_plot = make_plot(df, 'similarity', 'roi_roi_distance', 'Similarity', 'ROI-ROI Distance', '#cd5c5c')
                    roi_roi_overlap_plot = make_plot(df, 'similarity', 'roi_roi_overlap', 'Similarity', 'ROI-ROI Overlap', '#b0c4de')
                elif len(df1)==0 or len(df2)==0:
                    flag_df_empty=1
            else:
                print("submit status: not yet")
        else:
            print("the form is not valid")
    print("flag df empty: ", flag_df_empty)
    return render(request, 'similarity_match.html',
                 {'forms':forms, 'parsed_dicom_from_file':parsed_dicom_from_file, 
                 'dicom_form':dicom_form,
                 # plots
                 'ptv_dose_plot':ptv_dose_plot, 'roi_dose_plot':roi_dose_plot, 'ptv_volume_plot':ptv_volume_plot, 'rt_dose_plot':rt_dose_plot, 'roi_roi_distance_plot':roi_roi_distance_plot, 'roi_roi_overlap_plot':roi_roi_overlap_plot, 
                 # indicator
                 'flag_df_empty':flag_df_empty,
                 # selected filters
                 'selected_roi': selected_roi, 'selected_institution':selected_institution, 'selected_similarity_min':selected_similarity_min,
                 'selected_roi_min':selected_roi_min, 'selected_roi_max': selected_roi_max,
                 'selected_ptv_min':selected_ptv_min, 'selected_ptv_max': selected_ptv_max,
                 'selected_ptv_volume_min': selected_ptv_volume_min, 'selected_ptv_volume_max':selected_ptv_volume_max,
                 'selected_roi_roi_distance': selected_roi_roi_distance, 
                 'selected_roi_roi_overlap':selected_roi_roi_overlap,
                 # submission
                 'submitbutton': submitbutton
                 })


# verify uploaded data
@login_required
def stored_sql(request):
    # retrieve objects from Sqlite parsed_dicom table
    all_records_list = list(parsed_dicom.objects.all().values())
    # convert each record to dataframe
    all_records_df = pd.DataFrame(all_records_list)

    return render(request, 'stored_sql.html', {'all_records_df': all_records_df, 'all_records_list':all_records_list})