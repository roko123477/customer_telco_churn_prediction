from operator import ge
from flask import Flask,render_template, request
import numpy as np
from tensorflow import keras
from keras.models import load_model

app=Flask(__name__)
model=load_model('churn.h5')   

@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/sub",methods=["POST"])
def submit():
    if(request.method=="POST"):
        gender =(int)(request.form["gender"])
        seniorcitizen=(int)(request.form['SeniorCitizen'])
        partner=(int)(request.form['Partner'])
        dependents=(int)(request.form['Dependents'])
        tenure=(float)(request.form['tenure'])
        phoneservice=(int)(request.form['PhoneService'])
        MultipleLines=(int)(request.form['MultipleLines'])
        OnlineSecurity=(int)(request.form['OnlineSecurity'])
        OnlineBackup=(int)(request.form['OnlineBackup'])
        DeviceProtection=(int)(request.form['DeviceProtection'])
        TechSupport=(int)(request.form['TechSupport'])
        StreamingTV=(int)(request.form['StreamingTV'])
        StreamingMovies=(int)(request.form['StreamingMovies'])
        InternetService=request.form['InternetService']#1
        Contract=request.form['Contract'] #2
        PaymentMethod=request.form['PaymentMethod']#3
        PaperlessBilling=(int)(request.form['PaperlessBilling'])
        MonthlyCharges=(float)(request.form['MonthlyCharges'])
        TotalCharges=(float)(request.form['TotalCharges'])
        print([gender,partner])
        
        #1
        if(InternetService=="DSL"):
            internet=[1,0,0]
        elif(InternetService=="Fiber optic"):
            internet=[0,1,0] 
        else:
            internet=[0,0,1]    
        #2

        if(Contract=="Month-to-month"):
            cont=[1,0,0]
        elif(Contract=="One year"):
            cont=[0,1,0] 
        else:
            cont=[0,0,1]   
        #3
        if(PaymentMethod=="Bank transfer (automatic)"):
            transfer=[1,0,0,0]
        elif(Contract=="Credit card (automatic)"):
            transfer=[0,1,0,0] 
        elif(Contract=="Electronic check"):
            transfer=[0,0,1,0] 
        else:
            transfer=[0,0,0,1]  

        tenure=(tenure-1)/71
        MonthlyCharges=(MonthlyCharges-18.25)/(118.75-18.25)
        TotalCharges=(TotalCharges-18.8)/(8684.8-18.8)

        prediction=model.predict(np.array([[gender,seniorcitizen,partner,dependents,tenure,phoneservice,MultipleLines,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,PaperlessBilling,MonthlyCharges,TotalCharges,internet[0],internet[1],internet[2],cont[0],cont[1],cont[2],transfer[0],transfer[1],transfer[2],transfer[3]]]))      
        
        if(prediction[0][0]>0.5):
            value="The customer will leave the company"
        else:
            value="The customer will not leave the company"    

    return render_template("sub.html", n=value)


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)
