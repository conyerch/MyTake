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
# Create your views here.

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