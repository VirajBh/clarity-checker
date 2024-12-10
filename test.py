import requests

# API endpoint
url = 'http://127.0.0.1:5000/check-clarity'

# File to upload
file_path = r'C:\Users\viraj\Downloads\download (4).jpg'

files = {'image_data': open(file_path, 'rb')}

# Send POST request
response = requests.post(url, files=files)

# Print the response
print(response.json())
