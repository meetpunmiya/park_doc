 <h1>park_smart</h1>
<h3>- A parking automation system which recommends them about the parking vacancies which is divided into sections via a display installed.

<p>
 According to a study done, in USA, 73 BILLION DOLLARS are lost every year just due to parking inefficiencies. There are many difficulties a driver has to face while while going through a parking space and finding a parking spot is one of them.

Features:

-driver doesn't have to find themselves a parking space, biggest hassle gone like that.

-no manual entry needed, all automated by retireving the license plate number and timestamp.

-saves both time and fuel for the incoming driver .

-requires least human resource possible as parking navigation and registry log are automated via our infrastructure.
</p>
Technical how-to:

![Optical-character-recognition-on-images-to-read-vehicle-registration-plate](https://github.com/meetpunmiya/park_doc/assets/94193229/2f264200-2799-4c40-ada5-81923ab97a02)


<h3>-using Python, OCR_detection of the incoming vehicle's numberplate and their in_time using the python time module.


-using a ML model YOLO to consantly monitor the no.of vancies in each section and displaying it to the driver.

-using OCR_detection again for the outgoing vehicle to register it's out_time.

-maintain a database integrated with the OCR_models storing each vehicle's in_time and out_time.

![Flowchart](https://github.com/meetpunmiya/park_doc/assets/94193229/fd612480-ca50-4ac6-a342-89e0e4c16760)

</h3>

<p>
 Pre-requistes:
    - basic infrastructure(camera to detect the number plate)
 technical:
    -opencv,flask
    
 
</p>








