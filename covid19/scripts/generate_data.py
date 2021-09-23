import random
from django.shortcuts import render
from numpy import linspace
from scipy.integrate import odeint
import requests
from bs4 import BeautifulSoup



def scraperTable(url, fLeft, fRight):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('td', attrs={'align': 'right'})

    for s in quotes:
        s = str(s)
        left = s.find(fLeft)
        right = s.rfind(fRight)

        if left != -1 and right != -1:
            left = s.find('>', left)
            right = s.find('<', right)
            statistic = s[left + 1 : right]
            break

    return statistic


def scraper(url, amount):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('rect')

    i = 0
    ans = []
    lables = []
    for s in quotes[-amount:]:  # choosing data from the end
        s = str(s)
        left = s.find('\'')
        right = s.rfind('\'')

        if left and right and i < amount:  # only choose amount item
            date, value = s[left + 1:right].split(' ')
            ans.append({'x': i,  'y': value})
            lables.append(str(date))
            i += 1

    return ans, lables


def normalization_data(arr):
    ans = []
    for i in range(0, len(arr)-1):
        ans.append(({'x': i,  'y': int(arr[i + 1] - arr[i])}))

    return ans


def prognosis(ind):
    # Constants
    mu = 0.011
    beta = 0.155188
    s = 0.0035
    a = 0.3125
    gamma = 0.0833

    # numerical solution using an ordinary differential equation of SEIR-D model with total mortality
    t = linspace(0, 100, num=101)
    y0 = (9349645, 20000, 10000, 0, 0)

    def differential_SIR(n_SIR, t, beta, mu, s, a, gamma):
        dS_dt = (mu * 9349645) - mu * \
            n_SIR[0] - beta * n_SIR[0] * n_SIR[2] / 9349645
        dE_dt = ((beta * n_SIR[0] * n_SIR[2] / 9349645) - (mu + a)*n_SIR[1])
        dI_dt = a*n_SIR[1] - (gamma + mu)*n_SIR[2] - s*n_SIR[2]
        dR_dt = gamma*n_SIR[2] - mu*n_SIR[3]
        dD_dt = s*n_SIR[2]
        return dS_dt, dE_dt, dI_dt, dR_dt, dD_dt

    solution = odeint(differential_SIR, y0, t, args=(beta, mu, s, a, gamma))
    solution = [[row[i] for row in solution] for i in range(5)]

    ans = normalization_data(solution[ind])

    return ans  


def generate_data(url, ind, amount):
    real_data, lables = scraper(url=url, amount=amount)
    prognosis_data = prognosis(ind)

    return [real_data, prognosis_data, lables]


def generate_dead_statistic(url, ind, amount):
    real_data, prognosis_data, lables = generate_data(url, ind, amount)
    new_prognosis_data = []
    
    for i in range(min(len(real_data), len(prognosis_data))):
        new_prognosis_data.append({'x': real_data[i]['x'], 'y': int(real_data[i]['y']) + int(prognosis_data[i]['y'])})

    return [real_data, new_prognosis_data, lables]

def parseString(st):
    newstr = ''
    
    for i in st: 
        if i >= '0' and i <= '9':
            newstr += i

    return int(newstr)

# generate_data()
