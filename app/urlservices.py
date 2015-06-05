__author__ = 'rjr862'
import string

base_url = "http://127.0.0.1:5000/"
ticket_url = 'projects/<int:project>/tickets/<int:ticket>'
tickets_url = 'projects/<int:project>/tickets'
project_url = 'projects/<int:project>'
projects_url = 'projects/'


def get_ticket_url(project, ticket):
    result = base_url + ticket_url
    result = result.replace('<int:project>', str(project))
    result = result.replace('<int:ticket>', str(ticket))
    return result


def get_project_url(project):
    result = base_url + project_url
    result = result.replace('<int:project>', str(project))
    return result