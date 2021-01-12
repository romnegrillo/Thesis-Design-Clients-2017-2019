import numpy as np
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

  
def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 
  
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x

 
  
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x

    print(b_0,b_1)
  
    return(b_0, b_1) 
  
def plot_regression_line(x, y, b, title): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 
  
    # predicted response vector 
    y_pred = b[0] + b[1]*x 
  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
  
    # putting labels 
    plt.xlabel('Feature Weight') 
    plt.ylabel('Estimated Swine Weight')
    plt.title(title)
  
    # function to show plot 
    plt.show() 
  
def side():

    weightList=[]
    ageList=[]
    parameterList=[]

    with open("side_record.txt","r") as f:
        datas=f.readlines()
        print(datas)

        for data in datas:
            weightList.append(float(data.split(",")[0]))
            ageList.append(data.split(",")[1])
            
            area=float(data.split(",")[2])
            maxima=float(data.split(",")[3])
            minima=float(data.split(",")[4])

            parameterList.append((area**2) + (maxima**2) + (minima**2))

    for i,j,k in zip(weightList,ageList,parameterList):
        print(i,j,k)

    weightList=np.array(weightList)
    parameterList=np.array(parameterList)

    # observations 
    x = parameterList
    y = weightList
  
    # estimating coefficients 
    b = estimate_coef(x, y)
    print("Coefficients")
    print("b0",end= " ")
    print(round(b[0],4))
    print("b1", end= " ")
    print(round(b[1]),4)
    print("End")
  
    # plotting regression line 
    plot_regression_line(x, y, b, "Side View")

def top():

    weightList=[]
    ageList=[]
    parameterList=[]

    with open("top_record.txt","r") as f:
        datas=f.readlines()

        for data in datas:
            weightList.append(float(data.split(",")[0]))
            ageList.append(data.split(",")[1])
            
            area=float(data.split(",")[2])
            maxima=float(data.split(",")[3])
            minima=float(data.split(",")[4])

            parameterList.append((area**2) + (maxima**2) + (minima**2))

    for i,j,k in zip(weightList,ageList,parameterList):
        print(i,j,k)

    weightList=np.array(weightList)
    parameterList=np.array(parameterList)

    # observations 
    x = parameterList
    y = weightList
  
    # estimating coefficients 
    b = estimate_coef(x, y)
    print("Coefficients")
    print("b0",end= " ")
    print(round(b[0],4))
    print("b1", end= " ")
    print(round(b[1]),4)
    print("End")
  
    # plotting regression line 
    plot_regression_line(x, y, b, "Top View") 
  
if __name__ == "__main__":
    print("side view")
    side()
    print("top view")
    top()




