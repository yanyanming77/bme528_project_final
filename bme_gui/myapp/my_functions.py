from datetime import datetime
from turtle import fillcolor, width

from plotly.offline import plot
import plotly.graph_objects as go

# define a function to generate parsed data
def parse_dicom(ds, db_object):
    # dictionary to hold data
    dict = {}

    # patient info
    if ("PatientName"in ds)and("PatientBirthDate"in ds)and("PatientSex"in ds)and("EthnicGroup"in ds):
        dict['Patient Name'] = ds.PatientName
        dict['Patient Birthday'] = ds.PatientBirthDate
        dict['Patient Sex'] = ds.PatientSex
        dict['Patient Ethnic Group'] = ds.EthnicGroup

        db_object.patient_name = ds.PatientName
        db_object.patient_birthday = ds.PatientBirthDate
        db_object.patient_sex = ds.PatientSex
        db_object.patient_ethnic_group= ds.EthnicGroup

    # study info
    if ("StudyInstanceUID"in ds)and("StudyDate"in ds)and("StudyDescription"in ds):
        dict['Study Instance UID'] = ds.StudyInstanceUID
        dict['Study Date'] = ds.StudyDate
        dict['Study Description'] = ds.StudyDescription

        db_object.study_instance_uid = ds.StudyInstanceUID
        db_object.study_date = ds.StudyDate
        db_object.study_description = ds.StudyDescription

    # series 
    if ("SeriesInstanceUID"in ds)and("SeriesDate"in ds)and("SeriesDescription"in ds)and("Modality" in ds)and("SeriesNumber"in ds)and("Manufacturer"in ds)\
    and("PhysiciansOfRecord"in ds):
        dict['Series Instance UID'] = ds.SeriesInstanceUID
        dict['Series Date'] = ds.SeriesDate
        dict['Series Description'] = ds.SeriesDescription
        dict['Modality'] = ds.Modality
        dict['Series Number'] = ds.SeriesNumber
        dict['Physicians of Record'] = ds.PhysiciansOfRecord 
        dict['Manufacturer'] = ds.Manufacturer

        db_object.series_instance_uid= ds.SeriesInstanceUID
        db_object.series_date = ds.SeriesDate
        db_object.series_description = ds.SeriesDescription
        db_object.modality = ds.Modality
        db_object.series_number = ds.SeriesNumber
        db_object.physicians_of_record = ds.PhysiciansOfRecord 
        db_object.manufacturer = ds.Manufacturer
    # sop and image
    if ("SOPInstanceUID"in ds)and("SOPClassUID"in ds)and("ImageType"in ds)and("PhotometricInterpretation"in ds)and("RescaleSlope"in ds)and("RescaleIntercept"in ds)\
    and("SliceLocation"in ds)and("PixelSpacing"in ds)and("ImageOrientationPatient"in ds)and("ImagePositionPatient"in ds)and("SliceThickness"in ds)\
    and("BodyPartExamined"in ds)and("Rows"in ds)and("Columns"in ds):
        dict['SOP Instance UID'] = ds.SOPInstanceUID
        dict['SOP Class UID'] = ds.SOPClassUID

        dict['Image Type'] = ds.ImageType
        dict['Photo Metric Interpretation'] = ds.PhotometricInterpretation
        dict['Rescale Slope'] = ds.RescaleSlope
        dict['Rescale Intercept'] = ds.RescaleIntercept
        dict['Slice Location'] = ds.SliceLocation
        dict['Pixel Spacing'] = ds.PixelSpacing
        dict['Image Orientation Patient'] = ds.ImageOrientationPatient
        dict['Image Position Patient'] = ds.ImagePositionPatient
        dict['Slice Thickness'] = ds.SliceThickness
        dict['Body Part Examined'] = ds.BodyPartExamined

        db_object.sop_instance_uid= ds.SOPInstanceUID
        db_object.sop_class_uid = ds.SOPClassUID

        db_object.image_type= ds.ImageType
        db_object.photo_metric_interpretation = ds.PhotometricInterpretation
        db_object.rescale_slope = ds.RescaleSlope
        db_object.rescale_intercept = ds.RescaleIntercept
        db_object.slice_location = ds.SliceLocation
        db_object.pixel_spacing = ds.PixelSpacing
        db_object.image_orientation_patient= ds.ImageOrientationPatient
        db_object.image_position_patient = ds.ImagePositionPatient
        db_object.slice_thickness = ds.SliceThickness
        db_object.body_part_examined = ds.BodyPartExamined
    # only sop
    if ("SOPInstanceUID"in ds)and("SOPClassUID"in ds):
        dict['SOP Instance UID'] = ds.SOPInstanceUID
        dict['SOP Class UID'] = ds.SOPClassUID

        db_object.sop_instance_uid = ds.SOPInstanceUID
        db_object.sop_class_uid = ds.SOPClassUID
    # roi
    if ("ROIName"in "ROIStructureSetSequence"in ds):
        dict['ROI Name'] = ds.ROIStructureSetSequence.ROIName

        db_object.roi_name = ds.ROIStructureSetSequence.ROIName

    # upload time
    db_object.upload_time = datetime.now()
    # save and return
    db_object.save()
    return(dict)

# define a function to generate plots
def make_plot(data, x_value, y_value, x_text, y_text,color):
    # graph object
    graphs = []
    # add plot
    graphs.append(
        go.Scatter(x = data[x_value], y=data[y_value], mode='markers', opacity=0.8, name='', 
                hovertemplate = y_text+": %{y} <br>"+x_text+": %{x}", line_color=color)
    )
    layout={'title': y_text + ' vs. ' + x_text, 'xaxis_title': x_text + ' (%)', 'yaxis_title': y_text, 'title_x':0.5, 'height':400, 'width':500}
    plot_div = plot({'data':graphs, 'layout':layout}, output_type='div')
    return plot_div