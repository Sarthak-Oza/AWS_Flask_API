New-Item -ItemType Directory -Path ".\lambda_function"
pip install -r .\requirements.txt --target .\lambda_function
Move-Item .\api.py .\lambda_function\
Compress-Archive -Path .\lambda_function\* -DestinationPath .\lambda_function.zip -Force
Remove-Item -Path .\lambda_function\ -Recurse
