from flask import Flask, render_template,request, send_from_directory
from werkzeug import secure_filename
import os
from os.path import isfile, join

app = Flask(__name__)

imgPath = "Uploads/"
app.config['UPLOAD_FOLDER'] = imgPath


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



def uploaded_images():
	try:
		out = sorted(os.listdir(imgPath))
		return out
	except FileNotFoundError as e:
		return "<p>Error: Can't find "+imgPath+"</p>"

##################################################################

@app.route('/')
def homepage():

	data = {'uploaded_images':uploaded_images()}

	return render_template('homepage.html',data = data)

@app.route('/image_upload/')
def image_upload():

	return render_template('imageUpload.html')

@app.route('/uploader/',methods=['POST'])
def uploader():
	if request.method =='POST':

		#Get number of files in folder
		numFiles = len(os.listdir(imgPath))
		#this is appended to front of the file for ordering 

		file = request.files['file']
		filename = secure_filename(str(numFiles)+' '+file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		return ('File successfully uploaded<br>'
				'Folder now contains '+str(numFiles+1)+' images.<br>'
				'<a href="/">Click Here to Return to Main Page</a>')

@app.route('/reorder/',methods=['POST','GET'])
def reorder():
	if request.method=="POST":
		order = request.form.getlist('itemOrder')[0].split(",")
		
		fileList = sorted(os.listdir(imgPath))

		newList = []
		for item in order:
			newList.append(fileList[int(item)])

		for i in range(0,len(fileList)):
			os.rename(imgPath+newList[i],imgPath+str(i)+newList[i][1:])


		data = {'uploaded_images':uploaded_images()}
		return render_template('reorder.html',data=data)

	else:
		data = {'uploaded_images':uploaded_images()}
		return render_template('reorder.html',data=data)

@app.route('/delete/',methods=['POST','GET'])
def delete():
	if request.method=="POST":
		temp = request.form.getlist('toDelete')[0].split("\n")
		toDelete = []
		for i in range(0,len(temp)-1):
			toDelete.append(temp[i])
		for item in toDelete:
			flash(imgPath+item)
			os.remove(imgPath+item)
		data = {'uploaded_images':uploaded_images()}
		return render_template('delete.html',data=data)
	else:
		data = {'uploaded_images':uploaded_images()}
		return render_template('delete.html',data=data)

@app.route("/Uploads/<filename>")
def Uploads(filename):
	return send_from_directory("Uploads",filename)

@app.route("/documentation/")
def documentation():
	return render_template("documentation.html")


if __name__ == '__main__':
	app.run(debug = True)