# Create your models here.
from contextlib import nullcontext
from django.db import models
from django.forms import FloatField

# Create your models here.
class Treatment(models.Model):
    # patient id
    patient_id = models.CharField(max_length=100, primary_key=True)

    # ROI dose
    roi_dose = models.FloatField()
    # PTV dose
    ptv_dose = models.FloatField()
    # PTV volume
    ptv_volume = models.FloatField()
    # ROI-ROI distance
    roi_roi_distance = models.FloatField()
    # ROI-ROI overlap
    roi_roi_overlap = models.FloatField()
    # RT dose
    rt_dose = models.FloatField()
    # ROI 
    roi = models.CharField(max_length=200)
    # institution
    institution = models.CharField(max_length=200)

# dummy dataset to store random generated similarity (will implement algo later)
class Similarity(models.Model):
    # patient_id 
    patient_id = models.OneToOneField("Treatment", on_delete=models.CASCADE)
    # similarity
    similarity = models.FloatField(null=True)

class Document(models.Model):
    # the uploaded file to be stored in the media folder
    uploadedFile = models.FileField(upload_to = "Uploaded_DICOM/")

# parsed dicom 
class parsed_dicom(models.Model):
    # patient info
    patient_name = models.CharField(max_length=200, null=True)
    patient_birthday = models.CharField(max_length=200, null=True)
    patient_sex = models.CharField(max_length=100, null=True)
    patient_ethnic_group = models.CharField(max_length=100, null=True)
    # study info
    study_instance_uid = models.CharField(max_length=200, null=True)
    study_date = models.CharField(max_length=200, null=True)
    study_description = models.CharField(max_length=1000, null=True)
    # series 
    series_instance_uid = models.CharField(max_length=200, null=True)
    series_date = models.CharField(max_length=200, null=True)
    series_description = models.CharField(max_length=1000, null=True)
    modality = models.CharField(max_length=200, null=True)
    series_number = models.CharField(max_length=200, null=True)
    physicians_of_record = models.CharField(max_length=200, null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    # sop
    sop_instance_uid = models.CharField(max_length=200, null=True)
    sop_class_uid = models.CharField(max_length=200, null=True)

    image_type = models.CharField(max_length=200, null=True)
    photo_metric_interpretation = models.CharField(max_length=1000, null=True)
    rescale_slope = models.CharField(max_length=200, null=True)
    rescale_intercept = models.CharField(max_length=200, null=True)
    slice_location = models.CharField(max_length=200, null=True)
    pixel_spacing = models.CharField(max_length=200, null=True)
    image_orientation_patient = models.CharField(max_length=200, null=True)
    image_position_patient = models.CharField(max_length=200, null=True)
    slice_thickness = models.CharField(max_length=200, null=True)
    body_part_examined = models.CharField(max_length=200, null=True)
    # roi
    roi_name = models.CharField(max_length=200, null=True)

    # date time of uploading
    upload_time = models.DateTimeField(null=True) 