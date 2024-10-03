from openai import OpenAI
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, InputForm
from django.http import JsonResponse
from PIL import Image
import base64
from io import BytesIO
import os, requests
import hashlib
import datetime
from django.http import HttpResponse
from email.utils import formatdate
from xml.etree import ElementTree as ET
# Create your views here.

def image_gallery(request):
    # This is the view to render the main page with images
    images = [
        {'name': 'Tokyo', 'url': 'TOKYO1.png'}
    ]
    return render(request, 'take/design.html', {'images': images})

def load_image_for_customization(request, image_name):
    # This view is used to load the image dynamically when clicked
    # Assumes 'image_name' is passed as a URL parameter and it returns a JSON response.
    image_url = f'/static/{image_name}'
    return JsonResponse({'image_url': image_url})

class DesignPageView(View):
    template_name = 'myapp/design_page.html'

    # Handle GET request (render the design page)
    def get(self, request, *args, **kwargs):
        return render(request, 'take/interface.html')

    # Handle POST request (process image data)
    def post(self, request, *args, **kwargs):
        # Extract base64 image data from the request
        design_data = request.POST.get('image_data')
        
        # Decode the base64 image
        format, imgstr = design_data.split(';base64,')
        img_data = base64.b64decode(imgstr)

        # Convert to a PIL image
        img = Image.open(BytesIO(img_data))

        # Save the image to a file (e.g., in the media folder)
        img.save('media/custom_design.png', 'PNG')

        # Respond with a success message
        return JsonResponse({'status': 'success', 'message': 'Design saved!'})

class Index(TemplateView):
    template_name = 'take/index.html'

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'take/signup.html', {'form': form})
    
class Dashboard(View):
    def get(self, request):
        return render(request, 'take/dashboard.html')

    def post(sel, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        
        return render(request, 'take/signup.html', {'form': form})
    
def chat_gpt(request):
    response_txt = ""
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            client = OpenAI()

            # Call OpenAI API with the user input
            try:
                completion = client.chat.completions.create(
                model = "ft:gpt-4o-mini-2024-07-18:personal::ABu4DoT2",
                messages = [
                    {"role": "system", "content": "You describe visual designs for locations in detail."},
                    {"role": "user", "content": "Create a prompt for " + user_input}
                ]
                )

                response_txt = completion.choices[0].message

            except Exception as e:
                response_txt = "Error: " + str(e)

    else:
        form = InputForm()

    return render(request, 'take/chat.html', {'form': form, 'response_text': response_txt})
    
class ImageView(View):
    def get(self, request):
        images = [
            {
                'src': 'TOKYO2.png',
                'place': 'Tokyo Skyline',
                'style': 'Heavy Ink Painting',
                'mood': 'Lively Nighttime',
                'highlights': 'Light brushstrokes, Tokyo Tower'
            },
            {
                'src': 'GREATWALL.png',
                'place': 'Great Wall of China',
                'style': 'Light Ink Painting',
                'mood': 'Gentle Morning',
                'highlights': 'Mist, aerial view'
            },
            {
                'src': 'LONDON1.png',
                'place': 'London',
                'style': 'Watercolor Paining',
                'mood': 'Prestige, Evening',
                'highlights': 'Red Palette, London Bridge'
            },
            {
                'src': 'NYC2.png',
                'place': 'New York City',
                'style': 'Light Ink Painting',
                'mood': 'Gloomy Nightfall',
                'highlights': 'Hudson River, window lights'
            },
            {
                'src': 'OLDBASEBALL2.png',
                'place': 'Old Baseball Stadium',
                'style': 'Rough Vintage Illustration',
                'mood': 'Lively',
                'highlights': 'Aerial view, vintage, muted colors, filled'
            },
            {
                'src': 'NYC1.png',
                'place': 'New York City Skyline',
                'style': 'Heavy Ink Painting',
                'mood': 'Lively Nighttime',
                'highlights': 'Blotting, vibrant, colorful'
            },
            {
                'src': 'DUBAI3.png',
                'place': 'Dubai Skyline',
                'style': 'Heavy Ink Painting',
                'mood': 'Inspiring',
                'highlights': 'Famous architecture, black and white, buildings only'
            },
            {
                'src': 'TOKYO1.png',
                'place': 'Tokyo Skyline',
                'style': 'Watercolor',
                'mood': 'Vibrant morning',
                'highlights': 'Colorful palette, bright sun'
            },
            {
                'src': 'SPOKANE2.png',
                'place': 'Spokane Riverfront Park',
                'style': 'Vintage Illustration',
                'mood': 'Peaceful',
                'highlights': 'Clock tower, bridge, rapids'
            }
        ]
        return render(request, 'take/img_gallery.html', {'images': images})
    
def upload_file_to_printful(file_path, api_key):
    url = "https://api.printful.com/files"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Open the file from the static directory
    with open(file_path, 'rb') as file_data:
        files = {
            'file': ('file.png', file_data, 'image/png')  # Ensure file is named and mime type is correct
        }
        response = requests.post(url, headers=headers, files=files)
    
    return response.json()

# Django view to upload the file to Printful
def upload_design_to_printful(request):
    # Your Printful API key
    PRINTFUL_API_KEY = "TTU2dfCpJDWmbwJqUv8dy4y8nBVDKxSYnQkgyRKd"
    
    # Path to the PNG file in your static directory
    file_name = "LIGHTHOUSE.png"
    file_path = os.path.join(settings.STATIC_ROOT, file_name)
    file_path2 = "/Users/christopherconyersiv/MyTake-Django/MyTake/take/static/LIGHTHOUSE.png"
    #print(file_pat2)

    if not os.path.exists(file_path2):
        return JsonResponse({"error": "File does not exist"}, status=400)

    # Upload the file to Printful
    upload_response = upload_file_to_printful(file_path2, PRINTFUL_API_KEY)

    if upload_response.get('code') == 200:
        return JsonResponse({"message": "File uploaded successfully", "data": upload_response}, status=200)
    else:
        return JsonResponse({"error": "Failed to upload file", "data": upload_response}, status=400)

def calculate_signature(http_method, request_url, query_string, api_secret, timestamp):
    data_to_sign = f"{http_method}\n{request_url}\n{query_string}\n{api_secret}\n{timestamp}\n"
    #print(repr(data_to_sign))
    signature = hashlib.sha1(data_to_sign.encode('utf-8')).hexdigest()
    return signature

# Function to get current RFC2822 format timestamp
def get_rfc2822_timestamp():
    return formatdate(timeval=None, localtime=False, usegmt=True)

# Step 1: Initialize upload process
def initialize_upload(image_path):
    api_key = settings.PHOTODECK_API_KEY
    api_secret = settings.PHOTODECK_API_SECRET
    request_url = '/medias.xml'
    query_string = ''
    timestamp = get_rfc2822_timestamp()

    # Calculate signature
    signature = calculate_signature('POST', request_url, query_string, api_secret, timestamp)
    #print(os.path.getsize(image_path))
    #print(os.path.basename(image_path))

    # Set headers
    headers = {
        'X-PhotoDeck-Authorization': f'{api_key}:{signature}',
        'X-PhotoDeck-Timestamp': timestamp,
    }

    # Prepare data for the request
    media_params = {
        'media[content][upload_location]': 'REQUEST',
        'media[content][file_name]': os.path.basename(image_path),
        'media[content][file_size]': os.path.getsize(image_path),
        'media[content][mime_type]': 'image/png',  # assuming image/jpeg
    }

    # Send request to create media
    response = requests.post(f'https://api.photodeck.com{request_url}', headers=headers, data=media_params, auth=('chrisconyers4@gmail.com', '*SINGApore8'))

    if response.status_code == 201:
        # Parse the XML response
        root = ET.fromstring(response.text)

        # Inside <media>
        media = root.find('media')
        media_uuid = media.find('uuid').text  # Inside the <media> tag
        upload_url = media.find('upload-url').text
        upload_method = media.find('upload-method').text
        upload_params = {param.tag: param.text for param in media.findall('upload-params/*')}
        upload_file_param = media.find('upload-file-param').text

        # Extract <media-uuid> outside of <media>
        media_uuid_outside = root.find('media-uuid').text  # Outside <media>

        return {
            'media_uuid': media_uuid,  # UUID inside <media>
            'media_uuid_outside': media_uuid_outside,  # UUID outside <media>
            'upload_url': upload_url,
            'upload_method': upload_method,
            'upload_params': upload_params,
            'upload_file_param': upload_file_param,
        }
    else:
        print("eror")
        #print(f"Error: {response.status_code}, {response.text}")
        return None


# Step 2: Upload the file to the URL
def upload_file(image_path, upload_url, upload_params, upload_file_param):
    with open(image_path, 'rb') as file:
        # Upload the image with the necessary parameters
        files = {
            upload_file_param: file  # The file param name provided in the response
        }
        response = requests.post(upload_url, data=upload_params, files=files, auth=('chrisconyers4@gmail.com', '*SINGApore8'))

        # Debug the response for potential issues
        print(f"Upload Response Status: {response.status_code}")
        print(f"Upload Response Text: {response.text}")

        # Return True if the upload was successful (201 Created)
        return response.status_code == 201


# Step 3: Confirm upload
def confirm_upload(media_uuid, image_path):
    api_key = settings.PHOTODECK_API_KEY
    api_secret = settings.PHOTODECK_API_SECRET
    request_url = f'/medias/{media_uuid}.xml'
    query_string = ''
    timestamp = get_rfc2822_timestamp()

    # Calculate signature
    signature = calculate_signature('PUT', request_url, query_string, api_secret, timestamp)

    # Set headers
    headers = {
        'X-PhotoDeck-Authorization': f'{api_key}:{signature}',
        'X-PhotoDeck-Timestamp': timestamp,
    }

    # Prepare data to finalize upload
    media_params = {
        'media[content][upload_location]': 'REQUEST',
        'media[content][file_name]': os.path.basename(image_path),
        'media[content][file_size]': os.path.getsize(image_path),
        'media[content][mime_type]': 'image/png',  # assuming the image is PNG
    }

    # Send PUT request to confirm upload
    response = requests.put(f'https://api.photodeck.com{request_url}', headers=headers, data=media_params, auth=('chrisconyers4@gmail.com', '*SINGApore8'))

    # Debugging output
    print(f"Confirm Upload Status: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Return True if the confirmation was successful (200 or 204)
    return response.status_code in [200, 204]

# Full process
def upload_to_photodeck(request):
    image_path = '/Users/christopherconyersiv/MyTake-Django/MyTake/take/static/LIGHTHOUSE.png'

    if not os.path.exists(image_path):
        return HttpResponse('Image file not found!', status=404)

    # Step 1: Initialize upload
    upload_info = initialize_upload(image_path)
    #print(upload_info)  # Debugging to check the values

    if upload_info:
        # Step 2: Upload the file
        upload_success = upload_file(
            image_path,
            upload_info['upload_url'],
            upload_info['upload_params'],  # Params to be passed with file
            upload_info['upload_file_param']  # The file param name
        )

        if upload_success:
            # Step 3: Confirm the upload using media_uuid from <media>
            if confirm_upload(upload_info['media_uuid'], image_path):
                return HttpResponse('Image uploaded and confirmed successfully!')
            else:
                return HttpResponse('Failed to confirm upload.', status=500)
        else:
            return HttpResponse('Failed to upload file.', status=500)
    else:
        return HttpResponse('Failed to initialize upload.', status=500)
