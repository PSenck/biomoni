This is a dash app that used the biomoni package, the app displays measurement data along with its simulated data generated through parameter estimation. There are three options to use the app. Either with data on Azure (option 1), with automatically generated data on your drive (option 2) or with data measured historiacally in the example_data folder. For connecting to Azure you need the connection string of your storage account. The data there has to be present as file share data, more information on https://docs.microsoft.com/en-us/python/api/overview/azure/storage-file-share-readme?view=azure-python.

What you may have to change: at the bottom of the app `dash_app.run_server` there is a Linux/Mac variant and a Windows variant. In Linux/mac you can use both variants, but for Windows you have to use the Windows Variant, debug must be False in Windows.

For the Deployment on Azure:
First get the requirements needed to build a Python Environments in azure 
1. Open the folder where your dash app is present.
2. Optionally: activate desired python version using pyenv (done in Linux but not needed you can also create a virtualenv with anaconda)
`pyenv install 3.10.0` 
`pyenv shell 3.10.0` 
4. Create and activate virtual Environment using venv (Linux)
`python -m venv venv`
5. In Windows there are priblems to install cryptography using venv, therefore use virtualenv
`python -m virtualenv venv `
6. activate venv on Linux in same current folder
7. `source venv/bin/activate`
8. Windows
9. `venv/Scripts/activate`
10. Install all packages
11. create requirements.txt
`pip freeze > requirements.txt`

Azure Deployment
12. Now that you have the requirements.txt create a Github repo with your app and your requirements.txt
13. The app should be named app.py, but inside the app there should no variable be named app, if you have a dash app name it app_dash instead
14. Go to portal.azure.com 
15. click on App Services and create app with, puplish: Code Runtimestapel: Python 3.9
16. click on Deploymentcenter and connect to your Github repo
17. You can monitor your deployment on Logs

Hint:
Sometimes the maximum function evaluations `maxfev` are reached leading to insufficiently estimated params, you can increase them in the `settings_dash.py` file in `kwargs_estimate`.
If you use Azure you need a script or a txt file to set the connection string in your environmental variables. Or you do it manually each time in the console.
