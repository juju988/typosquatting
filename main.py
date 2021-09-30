import asyncio
from fastapi import FastAPI, Form
import uvicorn
from datetime import datetime
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
import leven_cython
import leven_python
from get_summary import get_project_summary
from dataclasses import dataclass

templates = Jinja2Templates('templates')

api = FastAPI()

MAX_DISTANCE = 2
MAX_PYPI_REQUESTS = 30

packages = []
with open('data/data.txt') as file:
    for line in file:
        packages.append(line.strip())


@dataclass
class PyPiProject:
    name: str
    summary: str
    squatter: bool = False
    edit_distance: int = 0


def configure():
    api.mount('/static', StaticFiles(directory='static'), name='static')


@api.get('/')
async def index(request: Request, package_name=None):
    print(package_name)
    context = {'request': request}
    if package_name:
        context['requested_package'] = package_name
        context['submitted'] = False
    return templates.TemplateResponse('home/index.html', context)


def get_closest_packages_python(package_name: str, packages_list: list):
    closest_packages = []
    package_name_length = len(package_name)
    minimum_package_name_length = max(4, package_name_length - MAX_DISTANCE)
    maximum_package_name_length = min(len(max(packages_list, key=len)), package_name_length + MAX_DISTANCE)
    for p in packages_list:
        if p is not package_name:
            if (len(p) > minimum_package_name_length) and (len(p) < maximum_package_name_length):
                distance = leven_python.levenshtein(package_name, p, MAX_DISTANCE)
                if distance:
                    closest_packages.append(p)
    print(f'closest_packages: {closest_packages}')
    return closest_packages


def get_closest_packages_cython(package_name: str, packages_list: list):
    closest_packages = []
    package_name_length = len(package_name)
    minimum_package_name_length = max(4, package_name_length - MAX_DISTANCE)
    maximum_package_name_length = min(len(max(packages_list, key=len)), package_name_length + MAX_DISTANCE)
    for p in packages_list:
        if p is not package_name:
            if (len(p) > minimum_package_name_length) and (len(p) < maximum_package_name_length):
                distance = leven_cython.levenshtein(package_name, p, MAX_DISTANCE)
                if distance:
                    closest_packages.append(p)
    print(f'closest_packages: {closest_packages}')
    return closest_packages


@api.post('/', name='check_package_name', status_code=200)
async def check_nearest_neighbours(request: Request, package_name: str = Form('package_name')):
    if package_name in packages:
        # grab the loop
        loop = None
        try:
            loop = asyncio.get_running_loop()
            print("got loop!", loop)
        except RuntimeError:
            pass  # Boo, why can't I just get nothing back?

        if not loop:
            loop = asyncio.get_event_loop()

        closest_packages = get_closest_packages_cython(package_name, packages)

        # create async requests to PyPI to get summaries of the closest_packages
        tasks = []
        for p in closest_packages[:MAX_PYPI_REQUESTS]:
            tasks.append((p, loop.create_task(get_project_summary(str(p)))))
        projects = []
        for p, t in tasks:
            summary = await t
            if summary:
                project = PyPiProject(p, summary)
                projects.append(project)
                print(project)

        # run through all the projects and mark any duplicate summaries
        summaries = []
        duplicate_summaries = []
        for p in projects:
            if p.summary not in summaries:
                summaries.append(p.summary)
            else:  # we have a duplicate summary
                duplicate_summaries.append(p.summary)

        # if project summary is in duplicate_summaries mark project as a potential typosquatter
        for p in projects:
            if (p.summary in duplicate_summaries) and (p.summary != 'No project description provided'):
                p.squatter = True

        # score each package according to how different their summary is and append to package_data
        package_data = []
        requested_package = {}
        for p in projects:
            p.edit_distance = leven_cython.levenshtein(package_name, p.name, len(min(packages, key=len)))
            if p.name == package_name:
                requested_package = {'name': p.name, 'summary': p.summary}
            else:
                package_data.append({'name': p.name, 'summary': p.summary, 'squatter': p.squatter,
                                     'edit_distance': p.edit_distance})

        data = {'request': request, 'package_data': package_data, 'requested_package': requested_package}
        print(closest_packages)
    else:
        # requested_package not in the list of known PyPI packages
        data = {'request': request, 'package_data': [], 'requested_package': package_name, 'bad_request': True}
    return templates.TemplateResponse('home/index.html', data)


"""# 22 sec with ThreadPoolExecutor, or 22 minutes with ProcessPoolExecutor!
@api.post('/', name='check_package_name', status_code=200)
async def check_nearest_neighbours(request: Request, package_name: str):
    # closest_packages = []
    start_time = datetime.now()

    # print([functools.partial(levenshtein, package_name, p, 2) for p in packages])

    # maybe remove p from packages prior to this?
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # results = [executor.submit(functools.partial(levenshtein, p, package_name, 2)) for p in packages]
        #for f in concurrent.futures.as_completed(results):
        #    if f.result():
        #        print(f.result())
        results = executor.map(levenshtein, packages)

    closest_packages = []
    for result in results:
        if result:
            closest_packages.append(result)
    data = {'request': request, 'closest_packages': closest_packages}
    print(f'closest_packages: {closest_packages}')
    print(f'processing time: {datetime.now() - start_time}')
    return templates.TemplateResponse('home/index.html', data)"""

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()


