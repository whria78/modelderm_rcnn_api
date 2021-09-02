This is the online RESTful API of the region-based CNN model (https://rcnn1.modelderm.com) used for articles published in JAMA Dermatology (http://doi.org/10.1001/jamadermatol.2019.3807) and (https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003381). The model API can be used without any restriction. The submitted images will be transferred with the IP address. Currently, the images are not stored, but all submitted images will be save after 2021, Jan. for further training of the algorithm.

# Requirement
1) Download and install python 3 (ex. anaconda version 3.8 64 bit) at https://www.anaconda.com/products/individual#Downloads


	![img](./img/download_anaconda.PNG)

	![img](./img/ana1.PNG)

	Please be sure to add the system PATH. 
	
	![img](./img/ana2.PNG)

2) Install opencv

	<pre><code>
	(windows) pip install opencv-python
	
	(linux) sudo pip install opencv-python
	</code></pre>
	
	
	![img](./img/pip_opencv.PNG)

3) Download the API file from github and extract the zip.

	![img](./img/git_download.PNG)

# How to Use 

1) There are 10 example images in the folder “/examples”. (images under the CC-BY-NC license)

	![capture_exmaple](./img/capture_example_folder.PNG)

2) When performing the test for a single image, run the following command: 

	<pre><code>
	python test.py [test_jpg file] [save_folder; default="RESULT"]
	</code></pre>

	
	![capture_exmaple](./img/run_one_file.PNG)

	Or you can also simply run “test1.bat”
	
	![capture_exmaple](./img/batch_for_win.PNG)


3) When performing the test for all images contained in a folder, run the following command: 

	<pre><code>
	python test.py [test_folder] [save_folder; default="RESULT"]
	</code></pre>
	
	
	![capture_exmaple](./img/run_folder.PNG)
	https://github.com/whria78/modelderm_rcnn_api/blob/master/test.log

	Or you can also simply run “test2.bat”

	![capture_exmaple](./img/batch_for_win.PNG)


4) The results can be found in the folder “/RESULT”. 

	![capture_exmaple](./img/capture_result_folder.PNG)
	![capture_exmaple](./img/capture_result.PNG)

5) The results are also stored in the form of “.csv” as below. They are listed in the order of “x0, y0, x1, y1, malignancy output, prediction”. The upper-left corner is 'x0, y0' and the lower-right corner is 'x1, y1'. In prediction, a hyphen (-) means that the lesion is nonspecific.

	![capture_exmaple](./img/capture_result_csv.PNG)
	https://github.com/whria78/modelderm_rcnn_api/blob/master/RESULT/result.csv


# Waiting Policy
The current test server (GPU = 1070x1, 1050tix1) requires 30 ~ 60 seconds to analyze one image and is capable of analyzing 20,000~30,000 images weekly, When there are more than three users online, users with heavier usage will have to wait until active analyses are completed. The test server uses the IP address to identify each user.  


# Contact Information
If you have any problem in using the algorithm, please contact Han Seung Seog (whria78@gmail.com).


# Citation
1) JAMA Dermatology 2019 - a model development and validation study

<pre><code>
@article{10.1001/jamadermatol.2019.3807,
    author = {Han, Seung Seog and Moon, Ik Jun and Lim, Woohyung and Suh, In Suck and Lee, Sam Yong and Na, Jung-Im and Kim, Seong Hwan and Chang, Sung Eun},
    title = "{Keratinocytic Skin Cancer Detection on the Face Using Region-Based Convolutional Neural Network}",
    journal = {JAMA Dermatology},
    year = {2020},
}
</pre></code>

2) PLOS Medicine 2020 - a retrospective cohort study

<pre><code>
@article{10.1371/journal.pmed.1003381,
  author={Han, Seung Seog and Moon, Ik Jun and Kim, Seong Hwan and Na, Jung-Im and Kim, Myoung Shin and Park, Gyeong Hun and Park, Ilwoo and Kim, Keewon and Lim, Woohyung and Lee, Ju Hee and others},
  title={Assessment of deep neural networks for the diagnosis of benign and malignant skin neoplasms in comparison with dermatologists: A retrospective validation study},
  journal={PLoS medicine},
  year={2020},
}
</pre></code>
