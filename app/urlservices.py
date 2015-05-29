__author__ = 'rjr862'
import string

__base_url__ = "http://127.0.0.1:5000/"
__ticket__ = '/projects/<int:project>/tickets/<int:ticket>'
__tickets__ = '/projects/<int:project>/tickets'
__project__ = '/projects/<int:project>'
__projects__ = '/projects/'


def get_ticket_url(project, ticket):
    ticket_url = __base_url__ + __ticket__
    ticket_url = string.replace(ticket_url, '<int:project>', project)
    ticket_url = string.replace(ticket_url, '<int:ticket>', ticket)
    return ticket_url


def get_project_url(project):
    project_url = __base_url__ + __project__
    project_url = string.replace(project_url, '<int:project>', project)
    return project_url