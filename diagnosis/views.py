from django.shortcuts import render, redirect, get_object_or_404
from .forms import DermaCaseForm
from .models import DermaCase
from load import predict_image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.conf import settings
import os

def submit_case(request):
    if request.method == 'POST':
        form = DermaCaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                description = request.POST.get('description', '')
                case.description = description
                file_name = default_storage.save(f'derma_images/{image_file.name}', ContentFile(image_file.read()))
                case.image = file_name
                
                # Log the file path
                full_path = os.path.join(settings.MEDIA_ROOT, file_name)
                print(f"Image saved at: {full_path}")
                
                try:
                    case.diagnosis = predict_image(full_path,case.description)
                except Exception as e:
                    case.diagnosis = f"Error in diagnosis: {str(e)}"
                    print(f"Prediction error: {str(e)}")
            else:
                case.diagnosis = "No image provided"
            case.save()
            return redirect('case_result', case_id=case.id)
    else:
        form = DermaCaseForm()
    return render(request, 'diagnosis/submit_case.html', {'form': form})


def case_result(request, case_id):
    case = get_object_or_404(DermaCase, id=case_id)
    print(case.diagnosis)
    
    context = {
        'diagnosis': case.diagnosis.split(",")[0][2:-2],
        'case_id': case_id,
        'advice': "".join(case.diagnosis.split(",")[1:])[2:-3],
        'image_url': case.image.url if case.image else None  # Pass image URL to template
    }
    
    print(type(case.diagnosis))
    # Render the template first
    response = render(request, 'diagnosis/case_result.html', context)
    
    return response

def delete_image(request, case_id):
    case = get_object_or_404(DermaCase, id=case_id)
    if case.image:
        try:
            if os.path.isfile(case.image.path):
                os.remove(case.image.path)
                print(f"Image deleted: {case.image.path}")
            else:
                print(f"Image file not found: {case.image.path}")
            case.image.delete(save=True)
        except Exception as e:
            print(f"Error deleting image: {str(e)}")
    return HttpResponse("Image deleted")