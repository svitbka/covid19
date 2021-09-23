from django.shortcuts import render
from .scripts.generate_data import generate_data, generate_dead_statistic, parseString, scraperTable
from .models import Category, Post


def index(request):
    data1, data2, lables = generate_data(
        url='https://index.minfin.com.ua/reference/coronavirus/svg1.inc.php?indCode=1&indNum=0&indKey=belarus&months=4', ind=2, amount=100)
    deadData1, deadData2, deadLables = generate_dead_statistic(
        url='https://index.minfin.com.ua/reference/coronavirus/svg2.inc.php?indCode=1&indNum=1&indKey=belarus&months=4', ind=4, amount=100)
    all_cases_disease_belarus = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/geography/belarus/', fLeft='<strong class="gold">', fRight='</strong>')
    all_cases_disease_world = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/', fLeft='<strong class="gold">', fRight='</strong>')
    all_deaths_belarus = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/geography/belarus/', fLeft='<strong class="red">', fRight='</strong>')
    all_deaths_world = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/', fLeft='<strong class="red">', fRight='</strong>')

    categories = Category.objects.all()

    return render(request, 'covid19/index.html',
                  {'data1': data1,
                   'data2': data2,
                   'lables': lables,
                   'deadData1': deadData1,
                   'deadData2': deadData2,
                   'deadLables': deadLables,
                   'all_cases_disease_belarus': all_cases_disease_belarus,
                   'all_cases_disease_world': all_cases_disease_world,
                   'all_deaths_belarus': all_deaths_belarus,
                   'all_deaths_world': all_deaths_world,
                   'categories': categories,
                   })


def show_post(request, slug):
    post = Post.objects.filter(category__slug=slug)
    categories = Category.objects.all()
    population = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/vaccination/belarus/', fLeft='<strong class="black">', fRight='</strong>')
    number_of_vaccinated = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/vaccination/belarus/', fLeft='<strong class="teal">', fRight='</strong>')
    fully_vaccinated = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/vaccination/belarus/', fLeft='<strong class="green">', fRight='</strong>')
    total_vaccinations = scraperTable(
        url='https://index.minfin.com.ua/reference/coronavirus/vaccination/belarus/', fLeft='<strong class="blue normal">', fRight='</strong>')
    vaccination = {'fully_vaccinated': fully_vaccinated,
                   'population': population}
    int_fully_vaccinated = parseString(fully_vaccinated)
    int_total_vaccinations = parseString(population)*1000

    print(int_fully_vaccinated, int_total_vaccinations)
    prossent_fully_vaccinated = round(int_fully_vaccinated / int_total_vaccinations * 100)

    # print(int(fully_vaccinated))

    return render(request, 'covid19/single.html',
                  {'post': post,
                   'categories': categories,
                   'population': population,
                   'number_of_vaccinated': number_of_vaccinated,
                   'fully_vaccinated': fully_vaccinated,
                   'total_vaccinations': total_vaccinations,
                      'prossent_fully_vaccinated': prossent_fully_vaccinated,
                   'vaccination': vaccination,
                   })
